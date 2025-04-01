import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import speech_recognition as sr
import json
import datetime
import matplotlib.pyplot as plt
import google.generativeai as genai  # Google Gemini AI API
from gtts import gTTS
from playsound import playsound
from plyer import notification  # For task reminders
import threading
import time

# Set up Google Gemini AI API key (Replace with your key)
genai.configure(api_key="your_gemini_api_key")

# Load or create tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "activity": {}, "reminders": {}}

tasks_data = load_tasks()

# Save tasks
def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks_data, f, indent=4)

# AI Task Suggestion using Gemini AI
def suggest_task():
    category = simpledialog.askstring("AI Suggestion", "Enter category (Work, Personal, Health):") or "General"
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Suggest a productive task for improving {category} productivity.")
        suggestion = response.text.strip()
        messagebox.showinfo("AI Suggestion", f"Suggested Task: {suggestion}")
        text_to_speech(suggestion)
    except Exception as e:
        messagebox.showerror("Error", f"AI Suggestion Failed: {str(e)}")

# Speech-to-Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Speech Recognition", "Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand"
    except sr.RequestError:
        return "Request error"

# Text-to-Speech Function
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    filename = "output.mp3"
    tts.save(filename)
    playsound(filename)

# Add Task
def add_task():
    task = simpledialog.askstring("Add Task", "Enter your task (or press Cancel to use speech):")
    if task is None:
        task = speech_to_text()

    if task and task.lower() != "could not understand":
        category = simpledialog.askstring("Task Category", "Enter category (Work, Personal, Health, etc.):") or "General"
        reminder_time = simpledialog.askstring("Set Reminder (HH:MM 24-hour format)", "Optional: Set a daily reminder time (e.g., 18:00):")

        tasks_data["tasks"].append({"task": task, "category": category, "completed": False})
        today = str(datetime.date.today())
        tasks_data["activity"][today] = tasks_data["activity"].get(today, 0) + 1

        if reminder_time:
            tasks_data["reminders"][task] = reminder_time

        save_tasks()
        update_task_list()

# Remove Task
def remove_task():
    task = simpledialog.askstring("Remove Task", "Enter task to remove (or press Cancel to use speech):")
    if task is None:
        task = speech_to_text()

    for t in tasks_data["tasks"]:
        if t["task"].lower() == task.lower():
            tasks_data["tasks"].remove(t)
            tasks_data["reminders"].pop(task, None)
            save_tasks()
            update_task_list()
            return

    messagebox.showwarning("Task Not Found", "Task not found in the list!")

# Toggle Task Completion
def toggle_task():
    selected_task = task_listbox.get(tk.ACTIVE).split(" | ")[1]
    for t in tasks_data["tasks"]:
        if t["task"] == selected_task:
            t["completed"] = not t["completed"]
            save_tasks()
            update_task_list()
            return

# Update Task List Display
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks_data["tasks"]:
        status = "✔" if task["completed"] else "❌"
        task_listbox.insert(tk.END, f"{status} | {task['task']} | {task['category']}")

# Show Productivity Graph
def show_graph():
    dates = sorted(tasks_data["activity"].keys())
    task_counts = [tasks_data["activity"][date] for date in dates]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, task_counts, marker="o", linestyle="-", color="b")
    plt.xlabel("Date")
    plt.ylabel("Tasks Completed")
    plt.title("Weekly Productivity Graph")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# Task Reminder Notification
def send_reminders():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for task, time in tasks_data["reminders"].items():
            if now == time:
                notification.notify(
                    title="Task Reminder",
                    message=f"Reminder: {task}",
                    timeout=5
                )
        time.sleep(60)

# Start the reminder thread
reminder_thread = threading.Thread(target=send_reminders, daemon=True)
reminder_thread.start()

# ------------------ GUI Design ------------------

root = tk.Tk()
root.title("AI To-Do Tracker")
root.geometry("500x600")
root.configure(bg="#2C2F33")  # Dark mode background

# Custom Styling
button_style = {"font": ("Arial", 12, "bold"), "bg": "#7289DA", "fg": "white", "width": 30, "height": 2}
label_style = {"bg": "#2C2F33", "fg": "white", "font": ("Arial", 14, "bold")}

# Header Label
header_label = tk.Label(root, text="🚀 AI-Powered To-Do Tracker", **label_style)
header_label.pack(pady=10)

# Task List Frame
frame = tk.Frame(root, bg="#2C2F33")
frame.pack(pady=10)

# Task List
task_listbox = tk.Listbox(frame, width=50, height=10, font=("Arial", 12), bg="#23272A", fg="white", selectbackground="#7289DA")
task_listbox.pack(pady=5)

# Buttons
tk.Button(root, text="➕ Add Task", command=add_task, **button_style).pack(pady=5)
tk.Button(root, text="🗑 Remove Task", command=remove_task, **button_style).pack(pady=5)
tk.Button(root, text="✅ Toggle Complete", command=toggle_task, **button_style).pack(pady=5)
tk.Button(root, text="💡 AI Task Suggestion (Gemini AI)", command=suggest_task, **button_style).pack(pady=5)
tk.Button(root, text="📊 Show Productivity Graph", command=show_graph, **button_style).pack(pady=5)

# Load existing tasks
update_task_list()

# Run App
root.mainloop()

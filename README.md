# AI-Powered To-Do Tracker

## Overview
An AI-powered to-do tracker using Tkinter for the GUI, Google Gemini AI for task suggestions, and various Python libraries for speech recognition, reminders, and productivity tracking.

## Features
- **Speech-to-Text**: Add tasks using voice commands.
- **AI Task Suggestion**: Uses Google Gemini AI to suggest tasks.
- **Task Management**: Add, remove, and mark tasks as completed.
- **Task Reminders**: Sends notifications for scheduled tasks.
- **Productivity Graph**: Tracks daily task completion trends.

## Installation
### Prerequisites
Ensure you have Python installed (>=3.8).

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ai-todo-tracker.git
   cd ai-todo-tracker
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your Google Gemini API key in `config.py`:
   ```python
   API_KEY = "your_gemini_api_key"
   ```

## Usage
Run the application using:
```sh
python app.py
```

## Repository Structure
```
📂 ai-todo-tracker
├── 📄 app.py               # Main application script
├── 📄 config.py            # Configuration file (API keys)
├── 📄 tasks.json           # Task storage file
├── 📄 requirements.txt     # List of dependencies
├── 📄 README.md            # Project documentation
└── 📄 LICENSE              # License file
```

## Dependencies
Install dependencies from `requirements.txt`:
```sh
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit pull requests or report issues!

# Course Scheduling System

A course scheduling system designed to help students build efficient and personalized semester schedules.

## 🚀 Getting Started

This project is written in **Python** and provides a graphical user interface  using **PyQt5** for selecting courses, setting time constraints, and generating valid schedules.

To run the system, open the `App.py` file and run it (e.g., press `F5` in your IDE).

## 🧭 Project Structure

- `App.py` – Entry point for running the application.
- `SRC/` – Source code folder containing:
  - `Controller/` – Application logic controllers.
  - `ViewLayer/` – GUI components built with PyQt5.
  - `Models/` – Data structures such as Course, Lesson, etc.
  - `Services/` – Handles file I/O, validation, scheduling, prefrences and time constraints.
  - `tests/` – tests for logic and GUI.


## 🔀 Branches

- `Part 3` – Including performance optimization, user experience improvements, and dynamic scheduling features.

## 📥 Installation

Make sure you have Python installed.

Install the required dependencies:

```bash
pip install pandas openpyxl PyQt5 pytest xlrd
```

## 🔗 GitHub Links

- **Project Repository**: [Course Scheduling System GitHub](https://github.com/NoaAmram9/-Course-scheduling-system.git)
- **Version 1.0 Files**: [Download v1.0 ZIP](https://github.com/user-attachments/files/19683801/course.scheduling.1.0.zip)


## 💡 Features

- Course selection with support for lectures, exercises, labs, reinforcement, and more.
- User-defined time constraints using intuitive GUI or external file.
- Export schedule to PDF.
- Dynamic sorting and filtering of schedule results (e.g., by number of free windows or study days).

## 📌 Google Calendar Export — Setup Instructions  

This app allows you to export your timetable to **Google Calendar**.

### ✨ First-time setup
When you export to Google Calendar for the first time:
- ✅ A browser window will open asking you to log in to your Google account.
- ✅ Grant permission for the app to manage your calendar (required to create calendar events).
- ✅ The app will save a file called `token.json` so you won’t need to log in again next time.

---

### 🗂 Required file: `credentials.json`
The app requires a **Google OAuth credentials file** (`credentials.json`).  
This file identifies the app to Google.

#### How to get it?
- You may receive `credentials.json` bundled with the app (check the app folder).
- If not provided, follow these steps to create it yourself:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials).  
  2. Create a project (if you don’t have one).  
  3. Create **OAuth 2.0 Client ID** → choose **Desktop App**.  
  4. Download the JSON file → rename it to `credentials.json` → place it in the app folder.

---

### 🔑 Keep your credentials safe
- **DO NOT upload `credentials.json` or `token.json` to GitHub or any public place.**
- These files contain sensitive information.

## ✍️ Authors

Created by the SchedSquad team.

---


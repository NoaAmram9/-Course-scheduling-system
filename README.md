# 📘 Course Scheduling System (v4.0)

A Python-based application to help students and academic staff build personal and efficient semester schedules.

## 🚀 Getting Started

To run the app, open `App.py` and run it (e.g., with `F5` in your IDE).

## 🧱 Structure

- `App.py` – Entry point.
- `SRC/` – Source code:
  - `Models/` – Core data models.
  - `ViewLayer/` – PyQt5 GUI (MVC structure).
  - `Controller/` – App logic coordinators.
  - `Services/` – Scheduling, constraints, file I/O, export tools.
  - `DataBase/` – SQLite-based user/course storage.
  - `tests/` – Unit and GUI tests.

## 🧪 Installation
Make sure you have Python installed.

Install the required dependencies:

```bash
pip install pandas openpyxl PyQt5 pytest xlrd google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

## ✨ Features

- Course selection, constraints, and preferences.
- Automatic and manual schedule generation.
- PDF export and Google Calendar integration.
- SQLite-based data persistence.
- Login system for students and secretaries.
- Dark mode and modern UI.
  
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

Created by the SchedSquad team;
Noa Amram, Adi Faktorovich, Gil Berti, Avigail Gorfinkel

## 🔗 GitHub Links

- **Project Repository**: [Course Scheduling System GitHub](https://github.com/NoaAmram9/-Course-scheduling-system.git)
- **Version 1.0 Files**: [Download v1.0 ZIP](https://github.com/user-attachments/files/19683801/course.scheduling.1.0.zip)
- **Version 4.0 Files**: [Schedule_4.0.zip](https://github.com/user-attachments/files/21024458/Schedule_4.0.zip)



---


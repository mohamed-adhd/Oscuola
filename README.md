<div align="center">

# Oscuola

<p>
  <b>A Qt desktop school-management app with role-based dashboards for students, teachers and admins, backed by a FastAPI + PostgreSQL service, with AI-generated student reports.</b>
</p>

<p>
  <img alt="C++" src="https://img.shields.io/badge/C%2B%2B-17-00599c?style=for-the-badge&logo=cplusplus&logoColor=white">
  <img alt="Qt" src="https://img.shields.io/badge/Qt-6%20Widgets-41cd52?style=for-the-badge&logo=qt&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white">
  <img alt="Vercel" src="https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white">
</p>

<p>
  <img alt="Students" src="https://img.shields.io/badge/Students-Grades%20%26%20Alerts-4f46e5?style=flat-square">
  <img alt="Teachers" src="https://img.shields.io/badge/Teachers-Grades%20%26%20Absences-16a34a?style=flat-square">
  <img alt="Admins" src="https://img.shields.io/badge/Admins-Users%20%26%20Classes-d97706?style=flat-square">
  <img alt="bcrypt" src="https://img.shields.io/badge/bcrypt-Hashed%20Passwords-dc2626?style=flat-square">
  <img alt="Groq" src="https://img.shields.io/badge/Groq-AI%20Reports-f55036?style=flat-square">
  <img alt="PDF" src="https://img.shields.io/badge/PDF-Report%20Export-ef4444?style=flat-square">
</p>

<p>
  <a href="#demo"><img alt="Demo" src="https://img.shields.io/badge/Demo-Reserved-00d084?style=for-the-badge"></a>
  <a href="#screenshots"><img alt="Screenshots" src="https://img.shields.io/badge/Screenshots-Table-facc15?style=for-the-badge"></a>
  <a href="#architecture"><img alt="Architecture" src="https://img.shields.io/badge/Architecture-Explained-f43f5e?style=for-the-badge"></a>
  <a href="#why-i-built-this"><img alt="Why" src="https://img.shields.io/badge/Why-I%20Built%20This-f97316?style=for-the-badge"></a>
</p>

</div>

---

## Overview

**Oscuola** is a desktop school-management application built with **C++17** and **Qt 6 Widgets**. It talks to a **FastAPI** backend over HTTPS, which stores everything in **PostgreSQL**. Each user logs in and lands in a dashboard matching their role: **student**, **teacher** or **admin**.

Students check grades, absences, alerts and timetables, and can send requests. Teachers manage grades, mark absences, answer student requests and generate **AI-written PDF reports**. Admins manage users, classes, teacher assignments and timetables.

## Screenshots

| Screen | Preview |
| --- | --- |
| Login | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/d3f3aa81-54de-44b2-a4ba-62296d3aadcd" /> |
| Register | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/72d89be1-a31b-40b1-8a32-5bfb2b4c7985" /> |
| Student Dashboard | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/5200b076-5be9-4153-96dd-1085d751bb6c" /> |
| Student Grades | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/272ccb19-24db-449c-82de-317a29a86f0b" /> |
| Post Request | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/cbdd6290-44bd-4aa6-bb4e-a42108b50da1" /> |
| Teacher Dashboard | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/d94fbd21-7e14-45b7-baf9-3f7bda92c04d" /> |
| Teacher Grades | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/6d433a63-b3eb-41b7-8e98-c2d0edb9cac7" /> |
| Teacher Requests | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/4487708b-7ae3-4ea6-85e4-8822a5c6c768" /> |
| Teacher Reports | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/acc81257-0308-48c2-a8ac-62076c82b6e2" /> |
| Admin Users | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/730d7f92-d3ef-4f33-8ac2-21c42f9d28fa" /> |
| Admin Classes | <img width="1290" height="730" alt="image" src="https://github.com/user-attachments/assets/4792e043-1283-42f1-a245-77b1361331c3" /> |

## Core Workflow

```text
Register (student)
      |
      v
Request lands with a teacher  --->  Teacher accepts / declines
      |
      v
Account created + confirmation email
      |
      v
Login (bcrypt check, role returned)
      |
      v
Role-based dashboard
  |-- Student : grades, absences, alerts, requests, timetable
  |-- Teacher : grades, absences, requests, AI reports (PDF)
  `-- Admin   : users, classes, teachers, timetables
```

## What Oscuola Does

| Area | Details |
| --- | --- |
| Authentication | Email + password login with bcrypt-hashed passwords and role-based routing. |
| Registration | Students sign up with name, email and class (e.g. `7A3`). A teacher approves the request before the account exists. |
| Password recovery | Emails a one-time reset link. Tokens are stored as SHA-256 hashes and marked used after one reset. |
| Student dashboard | Overall score, absences and active alerts at a glance, plus a profile picture. |
| Student pages | Grades, alerts, post a request to a teacher or administration, and class timetable. |
| Teacher dashboard | Class success rates and absence overview. |
| Teacher grades | Pick a class and a student (or the whole class), edit grades in a table and save them in one click. |
| Teacher absences | Mark a student absent with a description. |
| Teacher requests | Accept or decline pending registrations in a live list. |
| AI reports | Generates a formal student report from profile and grades using Groq (`gpt-oss-20b`), then exports it to PDF. |
| Admin users | Promote to teacher, demote to student or delete users from a table. |
| Admin classes | Create classes, assign teachers and move students between classes. |
| Admin timetables | Upload a timetable image per class. |

## Architecture

| Layer | Files | Role |
| --- | --- | --- |
| Desktop client | `main.cpp`, `mainwindow.cpp/.h`, `mainwindow.ui` | One `QMainWindow` with a `QStackedWidget`: 20 pages covering auth, student, teacher and admin flows. |
| Styling | `mainwindow.ui` stylesheet | One global QSS theme, styled by object name (indigo accent, dark sidebar, white cards). |
| Client networking | `database.cpp/.h`, `libraries.h` | Wraps the API with `QNetworkAccessManager` and sends a Bearer key on every request. |
| API | `app/main.py` | FastAPI routes and Pydantic models; every route is guarded by a Bearer-key dependency. |
| Data layer | `app/database/fetch.py`, `insert.py`, `delete.py` | PostgreSQL queries through `psycopg2`, bcrypt hashing, token handling, Groq report generation and SMTP email. |
| Reset page | `app/pages/reset.html` | Page served by the API for the password-reset link. |
| Deployment | `.vercelignore` | Backend deployed on Vercel. |

## Tech Stack

| Tech | Usage |
| --- | --- |
| **C++17** | Core client logic |
| **Qt 6 (Widgets, Network, DBus)** | Desktop UI, HTTP client, PDF export (`QPdfWriter`) |
| **CMake** | Build system |
| **FastAPI + Pydantic** | REST backend and request validation |
| **PostgreSQL + psycopg2** | Users, grades, absences, requests, timetables, reports, reset tokens |
| **bcrypt + SHA-256** | Password hashing and reset-token hashing |
| **Groq API** | AI-generated student reports |
| **SMTP (Gmail)** | Welcome and password-recovery emails |
| **Vercel** | Hosting for the API |

## Running Locally

### 1. Backend

```bash
cd app
pip install fastapi uvicorn psycopg2-binary bcrypt python-dotenv groq pydantic
uvicorn main:app --reload
```

Create a `.env` file in `app/` with:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
CON_STRING=...
API_KEY=your-shared-bearer-key
GMAIL_KEY=your-gmail-app-password
GROQ_API_KEY=your-groq-key
GROK_KEY=your-groq-key
```

### 2. Desktop client

Requires Qt 6 and CMake 3.16+.

```bash
cmake -S . -B build
cmake --build build
./build/Oscuola
```

The client reads `API_KEY` from its settings, and the base URL is set in `database.cpp`. Point it at your local or deployed backend.

## Why I Built This
- this project refused to end , it took me 3 months , given that i setted hte ETA to 30 days at the start of the repo...
-  i had no reason to build ts , my uni is teaching us basic js and html while i m creating this abomination
-  originally this idea was a code snippet in C that i did as an exercice , just a simple cli student monitoring app , now it became whatever this is
-  the moment this repo went past the 1 month mark , i started hating my life everytime i commited or pushed or PRd anything , i tried so many times to finish it yet it just kept growing

## Developer Notes

> now for the notes:

* months of development: **3**
- i really enjoyed some parts , the vercel and neondb communication , the ui refinements , but ts really was an agonizing experience
- this counts as my most mature project yet , pushed a lot of new combinations and new habits , such as branch discipline , ci/cd workflows , releases and etc
- i aint doing anymore software , since i plan on going ai for the next year in uni , i finish this and packrat , and then enough software , i ll get into ai field
- fun project , 1.75/10 , never again

---

<div align="center">
  <sub>Built with C++, Qt, FastAPI, PostgreSQL, and three months of stubbornness.</sub>
</div>

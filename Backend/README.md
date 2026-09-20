# Task Manager - Full Stack

## Overview

This project is a full-stack Task Manager application built using **React, FastAPI, and PostgreSQL**.

The application provides CRUD operations for managing tasks. The React frontend communicates with the FastAPI backend using HTTP requests, and task data is stored persistently in PostgreSQL.

## Technologies Used

* React
* Vite
* JavaScript
* CSS
* Python
* FastAPI
* Uvicorn
* Pydantic
* Psycopg
* PostgreSQL
* Swagger UI

## Features

* Add a new task
* View all tasks
* Mark a task as completed
* Undo a completed task
* Delete a task
* Loading state
* Empty task list handling
* API failure handling
* Invalid input handling
* PostgreSQL data persistence

## Project Structure

```text
Authentication/
│
├── backend/
│   ├── src/
│   │   └── app/
│   │       ├── api/            # HTTP routes (auth.py, tasks.py)
│   │       ├── auth/           # security infra: tokens, password hashing, deps
│   │       ├── services/
│   │       ├── repositories/
│   │       ├── models/
│   │       ├── schemas/
│   │       ├── database.py
│   │       ├── config.py
│   │       └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── .env               # local only, not committed
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/            # fetch wrappers per resource
│   │   ├── context/         # AuthContext
│   │   ├── pages/           # LoginPage, RegisterPage, TasksPage
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── ...
│
└── README.md
Installation
Backend

Create a virtual environment:

python -m venv venv

Activate it on Windows PowerShell:

venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Database

Install and start PostgreSQL.

Create a database named:

task_manager_db

Create a .env file:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=task_manager_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password

Replace your_postgresql_password with your PostgreSQL password.

Do not commit .env to GitHub.

Running the Backend

From the backend directory:

python -m uvicorn app.main:app --reload --app-dir src

Backend:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs
Running the Frontend

Open a second terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173/
API Endpoints
Method	Endpoint	Description
GET	/tasks	Get all tasks
GET	/tasks/{task_id}	Get task by ID
POST	/tasks	Create a task
PUT	/tasks/{task_id}	Update a task
DELETE	/tasks/{task_id}	Delete a task
Application Flow
React
  ↓
HTTP Request
  ↓
FastAPI
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
  ↓
FastAPI Response
  ↓
React UI
Request Examples
Create Task

POST /tasks

{
  "title": "Learn React",
  "completed": false
}
Get Tasks

GET /tasks

[
  {
    "task_id": 1,
    "title": "Learn React",
    "completed": false
  }
]
Update Task

PUT /tasks/1

{
  "title": "Learn React",
  "completed": true
}
Delete Task

DELETE /tasks/1

The task is removed from PostgreSQL and the React UI.

UI Behavior
Incomplete task → normal text + blue Complete button
Completed task → green text + green Undo button
No strikethrough
No green task background
Delete button is red
Complete/Undo and Delete buttons have the same size
Validation and Error Handling
Empty task titles are rejected.
Invalid API requests are handled by FastAPI/Pydantic.
If a task does not exist, the API returns 404 Not Found.
If the backend is unavailable, React displays an API error message.
While loading tasks, React displays a loading message.
If there are no tasks, React displays an empty-task message.
Testing

Verify the complete flow from the React application:

Load existing tasks.
Add a new task.
Complete the task.
Confirm the text becomes green.
Confirm the Complete button becomes green and changes to Undo.
Undo the task.
Delete the task.
Refresh the page and verify that PostgreSQL data persists.
Test the empty task list.
Stop FastAPI and verify API failure handling.
Try adding an empty task and verify invalid input handling.

Conclusion:

This project is a complete full-stack Task Manager using React, FastAPI, and PostgreSQL.

It implements CRUD operations, validation, error handling, loading and empty states, PostgreSQL persistence, and complete frontend-backend integration.

React → FastAPI → Service → Repository → PostgreS
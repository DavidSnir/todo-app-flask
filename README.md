# Flask Todo App

A full-stack Todo application built with Flask, featuring a web interface and a robust RESTful API. This project is part of a DevOps course, emphasizing clean architecture, modularity (Blueprints), and persistent storage with MongoDB.

## Features
- **Task Management:** Create, update, delete, and view tasks.
- **Task Lists:** Organize tasks into different lists.
- **Subtasks:** Support for hierarchical task management.
- **Web Interface:** Interactive UI built with HTML, CSS, and JavaScript.
- **Persistent Storage:** MongoDB integration for data persistence.
- **Validation:** Robust JSON field validation for API requests.
- **Error Handling:** Centralized error management via Flask Blueprints.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB (via PyMongo)
- **Frontend:** HTML, Vanilla CSS, JavaScript
- **Testing:** Pytest
- **Environment:** Python-dotenv for configuration

## Project Structure
The project follows a modular structure within the `src/` directory:
- `app.py`: Application factory and entry point.
- `database/`: Database connection and management logic.
  - `connection.py`: MongoDB client initialization.
  - `manager.py`: Data access objects (DAOs) for Tasks and Lists.
- `models/`: Data structures and business logic.
  - `task.py`: Task model and JSON serialization.
  - `task_list.py`: Task List model.
- `routes/`: API and UI route definitions (Blueprints).
  - `tasks.py`: Endpoints for individual tasks and subtasks.
  - `task_lists.py`: Endpoints for managing task lists.
  - `errors.py`: Custom error handlers.
- `static/`: Frontend assets (CSS and JS).
- `templates/`: HTML templates for the web interface.
- `utils.py`: Shared helper functions for validation.
- `tests/`: Comprehensive unit and end-to-end tests.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd todo-app
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory and add your MongoDB connection string:
   ```env
   MONGO_CONNECTION_STRING=mongodb://localhost:27017/
   ```

5. **Run the application:**
   ```bash
   python -m src.app
   ```
   The app will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Tasks
- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Create a new task.
  - Body: `{"title": "Task title", "parent_id": "optional_id"}`
- `GET /tasks/<task_id>`: Get a specific task by ID.
- `PATCH /tasks/<task_id>`: Update a task's title or status.
  - Body: `{"title": "New title", "is_complete": true}`
- `DELETE /tasks/<task_id>`: Remove a task.
- `DELETE /tasks/<task_id>/r`: Recursively delete a task and its subtasks.

### Task Lists
- `GET /lists`: Retrieve all task lists.
- `POST /lists`: Create a new list.
  - Body: `{"title": "List Name"}`
- `GET /lists/<list_id>`: Get a specific list by ID.
- `PATCH /lists/<list_id>`: Update list title.
- `DELETE /lists/<list_id>`: Remove a list.

## Testing
The project includes unit and end-to-end tests.
To run all tests:
```bash
pytest
```
To run specific tests:
```bash
pytest tests/uni_tests/test_task_list_routes.py
```

## 🗺 Roadmap
- [x] In-memory Todo API
- [x] Error handling & Input validation
- [x] MongoDB Integration for persistent storage
- [x] Web Interface (HTML/JS)
- [x] Subtask support
- [x] Unit and E2E Tests
- [ ] Dockerization for containerized deployment
- [ ] CI/CD Pipeline integration

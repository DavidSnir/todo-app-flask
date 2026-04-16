# Flask Todo App

A simple and robust RESTful API for a Todo application, built with Flask. This project is part of a DevOps course, focusing on clean architecture, modular code (Blueprints), and API development.

## Current Status
Currently, the application uses **in-memory storage** for tasks. Integration with **MongoDB** is planned for the next phase.

## Tech Stack
- **Backend:** Flask (Python)
- **Validation:** Custom utility for JSON field validation
- **Error Handling:** Centralized error management via Flask Blueprints
- **Storage:** In-memory (Transitioning to MongoDB soon)

## Project Structure
- `app.py`: Application entry point.
- `routes.py`: Contains API endpoints for task management.
- `models.py`: Data structures and logic for task operations.
- `errors.py`: Error handler Blueprint.
- `utils.py`: Helper functions for validation.
- `tests/`: Unit and end-to-end tests.

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
   pip install -r requirments.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Tasks
- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Create a new task.
  - Body: `{"title": "Task title"}`
- `GET /tasks/<task_id>`: Get a specific task by ID.
- `PATCH /tasks/<task_id>`: Update a task's title or completion status.
  - Body: `{"title": "New title", "is_complete": true}`
- `DELETE /tasks/<task_id>`: Remove a task.

## Testing
The project includes tests located in the `tests/` directory.
To run tests (assuming you have `pytest` or a similar runner installed):
```bash
# Example command
pytest tests/uni_tests/todo_test.py
```

## 🗺 Roadmap
- [x] In-memory Todo API
- [x] Error handling & Input validation
- [ ] **MongoDB Integration** for persistent storage
- [ ] Dockerization for DevOps workflows
- [ ] CI/CD Pipeline setup

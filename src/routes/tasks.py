from flask import jsonify, request, Blueprint, render_template
from werkzeug.exceptions import NotFound, BadRequest
from src.models.task import Task
from src.utils import check_json_fields
from src.database.manager import TaskManager
from src.database.connection import get_collection

tasks_bp = Blueprint("tasks",__name__)
global task_manager
collection_name = "tasks"
task_manager = TaskManager(get_collection(collection_name))

@tasks_bp.get("/tasks/<task_id>/subtasks_page")
def subtasks_page(task_id):
    return render_template("subtasks.html", task_id=task_id)

@tasks_bp.get("/tasks")
def show_tasks():
    all_tasks_list: list[Task]  = task_manager.get_all_tasks()
    result = [task.to_json() for task in all_tasks_list]
    return jsonify({"status": "success","tasks": result})

@tasks_bp.post("/tasks")
def create_task():
    """### create task adds a task to the database\n
    needs a task title from the user in the `Task.to_json()` format"""
    
    data = request.get_json()
    
    if not data:
        raise BadRequest("Body is empty")
        
    title = data.get("title")
    parent_id = data.get("parent_id")
    
    if title is None:
        raise BadRequest("Key should be title")
    if not isinstance(title, str):
        raise BadRequest("title should be string")
    
    import uuid
    p_id = None
    if parent_id and parent_id != "None":
        try:
            p_id = uuid.UUID(parent_id)
        except ValueError:
            raise BadRequest("Invalid parent_id format")

    title = title.strip()
    if not title:
        new_task = Task(parent_id=p_id)
    else:
        new_task = Task(title, parent_id=p_id)
        
    if task_manager.add_task(new_task):
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }), 201
    else:
        return jsonify({"status": "failed", "error": "Could not add task"}), 500
        
@tasks_bp.route("/tasks/<task_id>", methods=['GET', 'PATCH', 'DELETE'])
def ask_by_id(task_id):
    result_task = task_manager.get_task_by_id(task_id)
    
    if not result_task:
        raise NotFound("Task was not found")

    # diffrent actions depends on chosen method
    if request.method == 'GET':
        return jsonify(result_task.to_json())
    
    elif request.method == 'PATCH':
        allowed_fields: list[tuple[str, type]] = [('title', str), ('is_complete', bool)]
        data = request.get_json()
        
        # check for existing body
        if not data:
            raise BadRequest("received empty body")
        
        # checks for incorrect fields and types
        is_fields_correct = check_json_fields(allowed_fileds=allowed_fields, user_data=data)
        if not is_fields_correct[0]:
            raise BadRequest(is_fields_correct[1])
        
        if 'title' in data:
            if not data["title"].strip():
                raise BadRequest("title cannot be empty or only whitespace")
            data["title"] = data["title"].strip()

        # updating the task object
        result_task.edit_task(user_data=data)
        success = task_manager.edit_task(result_task)
        
        return jsonify({
            "status": "success" if success else "failed",
            "task": result_task.to_json()
            }), 200
    
    elif request.method == 'DELETE':
        success, message = task_manager.remove_task(result_task)
        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failed", "message": message}), 400

@tasks_bp.delete("/tasks/<task_id>/r")
def recursive_delete(task_id):
    result_task = task_manager.get_task_by_id(task_id)
    if not result_task:
        raise NotFound("Task was not found")
    
    success, count = task_manager.remove_task_and_sub_tasks(result_task)
    if success:
        return jsonify({"status": "success", "deleted_count": count}), 200
    else:
        return jsonify({"status": "failed", "message": "Could not remove task and sub-tasks"}), 500
        


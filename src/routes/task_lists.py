from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest
from src.models.task_list import TaskList
from src.utils import check_json_fields
from src.database.manager import TaskListManager, TaskManager
from src.database.connection import get_collection

task_lists_bp = Blueprint("task_lists", __name__)
tasks_collection_name = "tasks"
task_list_collection_name = "lists"
task_manager = TaskManager(get_collection(tasks_collection_name))
task_list_manager = TaskListManager(get_collection(task_list_collection_name), task_manager=task_manager)

@task_lists_bp.get("/lists")
def show_lists():
    all_lists = task_list_manager.get_all_lists()
    result = [task_list.to_json() for task_list in all_lists]
    return jsonify({"status": "success", "lists": result})

@task_lists_bp.post("/lists")

def create_list():
    """needs a body {"title": name}"""
    
    data = request.get_json()
    if not data:
        raise BadRequest("Body is empty")
        
    title = data.get("title")
    if title is None:
        raise BadRequest("Key should be title")
    if not isinstance(title, str):
        raise BadRequest("title should be string")
    
    title = title.strip()
    if not title:
        new_list = TaskList()
    else:
        new_list = TaskList(title)
        
    if task_list_manager.add_list(new_list):
        return jsonify({
            "status": "created",
            "list": new_list.to_json()
        }), 201
    else:
        return jsonify({"status": "failed", "error": "Could not add list"}), 500

@task_lists_bp.route("/lists/<list_id>", methods=['GET', 'PATCH', 'DELETE'])
def list_by_id(list_id):
    result_list = task_list_manager.get_list_by_id(list_id)
    if not result_list:
        raise NotFound("List was not found")

    if request.method == 'GET':
        return jsonify(result_list.to_json())
    
    elif request.method == 'PATCH':
        allowed_fields = [('title', str)]
        data = request.get_json()
        if not data:
            raise BadRequest("received empty body")
        
        is_fields_correct = check_json_fields(allowed_fileds=allowed_fields, user_data=data)
        if not is_fields_correct[0]:
            raise BadRequest(is_fields_correct[1])
        
        if 'title' in data:
            if not data["title"].strip():
                raise BadRequest("title cannot be empty or only whitespace")
            data["title"] = data["title"].strip()

        result_list.edit_list(user_data=data)
        success = task_list_manager.edit_list(result_list)
        
        return jsonify({
            "status": "success" if success else "failed",
            "list": result_list.to_json()
            }), 200
    
    elif request.method == 'DELETE':
        success = task_list_manager.remove_list(result_list)
        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failed", "message": "Could not remove list"}), 400

@task_lists_bp.delete("/lists/<list_id>/r")
def recursive_delete(list_id):
    result_list = task_list_manager.get_list_by_id(list_id)
    if not result_list:
        raise NotFound("List was not found")
    
    success, count = task_list_manager.delete_list_and_sub_task(result_list)
    if success:
        return jsonify({"status": "success", "deleted_tasks_count": count}), 200
    else:
        return jsonify({"status": "failed", "message": "Could not remove list and its tasks"}), 500

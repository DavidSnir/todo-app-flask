from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest
import src.models.task as task
from src.utils import check_json_fields

tasks_bp = Blueprint("tasks",__name__)

@tasks_bp.get("/tasks")
def show_tasks():
    result = task.get_all_tasks()
    return jsonify(result)

@tasks_bp.post("/tasks")
def create_task():
    """### create task adds a task to the tasks list\n
    needs a task title from the user in this format
    `{"title": "choses title"}`, or leave empty, in that case the title would be the defult untitled title"""
    
    data = request.get_json()
    if data == {}:
        raise BadRequest("Body is empty")
    title = data.get("title")
    if title is None:
        raise BadRequest("Key should be title")
    if not isinstance(title,str):
        raise BadRequest("title should be string")
    elif title == "":
        new_task = task.create_task()
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }),201
    elif title[0] == " ":
        raise BadRequest("first character cant be ' '")
    elif title:
        new_task = task.create_task(title)
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }),201
        
@tasks_bp.route("/tasks/<task_id>",methods= ['GET','PATCH','DELETE'])
def show_task_by_id(task_id):
    
    # check if task id entered correctly
    if not(type(task_id) == str):
        raise BadRequest("only string after /tasks")
    
    result_task = task.get_task_by_id(task_id=task_id)
    
    if not result_task:
        raise NotFound("Task was not found")

    # diffrent actions depends on chosen method
    if request.method == 'GET':
        return jsonify(result_task.to_json())
    
    elif request.method == 'PATCH':
        allowed_fileds: list[tuple[str, type]] = [('title',str), ('is_complete', bool)]
        data = request.get_json()
        
        # check for existing body
        if data == {}:
            raise NotFound("recived empty body")
        
        # checks for incorect fields and types
        is_fields_corect = check_json_fields(allowed_fileds=allowed_fileds,user_data=data)
        if not is_fields_corect[0]:
            raise BadRequest(is_fields_corect[1])
        # updating the task object
        result_task = task.edit_task(task=result_task, user_data=data)
        return jsonify({
            "status": "success",
            "task": result_task.to_json()
            }),200
    
    elif request.method == 'DELETE':
        task.tasks_list.remove(result_task)
        return jsonify({"status": "success"}),200
        


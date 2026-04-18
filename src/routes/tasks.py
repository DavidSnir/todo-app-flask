from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest
from src.models.task import Task
from src.utils import check_json_fields
from src.database.manager import TaskManager
from src.database.connection import database as db

tasks_bp = Blueprint("tasks",__name__)
task_manager = TaskManager(db.tasks)

@tasks_bp.get("/tasks")
def show_tasks():
    global task_manager
    all_tasks_list: list[Task]  = task_manager.get_all_tasks()
    result = [task.to_json() for task in all_tasks_list]
    return jsonify({"status": "success","tasks": result})

@tasks_bp.post("/tasks")
def create_task():
    """### create task adds a task to the database\n
    needs a task title from the user in the `Task.to_json()` format"""
    
    data = request.get_json()
    
    if data == {}:
        raise BadRequest("Body is empty")
    title = data.get("title")
    if title is None:
        raise BadRequest("Key should be title")
    if not isinstance(title,str):
        raise BadRequest("title should be string")
    elif title == "":
        new_task = Task()
        task_manager.add_task(new_task)
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }),201
    elif title[0] == " ":
        raise BadRequest("first character cant be ' '")
    elif title:
        new_task = Task(title)
        task_manager.add_task(new_task)
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }),201
        
@tasks_bp.route("/tasks/<task_id>",methods= ['GET','PATCH','DELETE'])
def ask_by_id(task_id):
    
    # check if task id entered correctly
    if not(type(task_id) == str):
        raise BadRequest("only string after /tasks")
    
    result_task = task_manager.get_task_by_id(task_id)
    
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
        elif data["title"]=="":
            raise NotFound("title cant be empty")
        elif data["title"][0] == " ":
            raise NotFound("title cant begin with ' '")
        # updating the task object
        result_task.edit_task(user_data=data)
        task_manager.edit_task(result_task)
        return jsonify({
            "status": "success",
            "task": result_task.to_json()
            }),200
    
    elif request.method == 'DELETE':
        task.tasks_list.remove(result_task)
        return jsonify({"status": "success"}),200
        


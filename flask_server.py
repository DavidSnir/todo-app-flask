from flask import Flask, jsonify, request
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from hardcoded_task_list import Task_list
from models import Task
from utils import check_json_fields

app = Flask(__name__)

@app.errorhandler(BadRequest)
def bad_request(e):
    return jsonify({"error": str(e)}),400

@app.errorhandler(NotFound)
def bad_request(e):
    return jsonify({"error": str(e)}),404

@app.get("/tasks")
def show_tasks():
    result: list = []
    for task in Task_list:
        result.append(task.to_json())
    return jsonify(result)

@app.post("/tasks")
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
    elif title:
        new_task = Task(title=title)
        Task_list.append(new_task)
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }),201
    else:
        new_task = Task()
        Task_list.append(new_task)
        return jsonify({
            "status": "created",
            "task": new_task.to_json()
        }),201
        
@app.route("/tasks/<task_id>",methods= ['GET','PATCH','DELETE'])
def show_task_by_id(task_id):
    
    # check if task id entered correctly
    if not(type(task_id) == str):
        raise BadRequest("only string after /tasks")
    result_task: Task = None
    
    # searches fot the right task
    # TODO: change Task_list var to dict for faster searching
    for task in Task_list:
        if task_id == task.id:
            result_task = task
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
        
        # updating the task object
        for key, value in data.items():
            setattr(result_task,key,value)
        return jsonify(result_task.to_json()),200
    
    elif request.method == 'DELETE':
        Task_list.remove(result_task)
        return jsonify({"status": "success"}),200
        

if __name__ == "__main__":
    app.run(debug=True)
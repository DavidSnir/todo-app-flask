from flask import Flask, jsonify, request
from hardcoded_task_list import Task_list
from models import Task

app = Flask(__name__)

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
    `{"tiitle": "choses title"}`, or leave empty, in that case the title would be the defult untitled title"""
    data = request.get_json()
    title = data.get("title")
    if not type(title) == str:
        return jsonify({"error": "title should be string"}), 400
    elif title:
        new_task = Task(title=title)
        Task_list.append(new_task)
        return jsonify({
            "status": "created",
            "title": title
        }),201
    else:
        new_task = Task()
        Task_list.append(new_task)
        return jsonify({
            "status": "created",
            "title": "untitled"
        }),201
        
        

@app.route("/tasks/<task_id>",methods= ['GET','PATCH','DELETE'])
def show_task_by_id(task_id):
    if not(str(task_id).isdigit() and str(task_id).isascii()):
        return jsonify({"error": "only numbers after /tasks"}), 400
    result_task: Task
    for task in Task_list:
        if int(task_id) == task.id:
            result_task = task
    if not result_task:
        return jsonify({"error": "Not Found"}),404
    elif request.method == 'GET':
        return jsonify(result_task.to_json())
    elif request.method == 'PATCH':
        allowed_fileds = ['title', 'is_complete']
        data = request.get_json()
        for item in data.items():
            if not item[0] in allowed_fileds:
                   return jsonify({"error": "can only chnage title, is_complete"})
        for key, value in data.items():
            setattr(result_task,key,value)
        return jsonify(result_task.to_json()),201
    elif request.method == 'DELETE':
        Task_list.remove(result_task)
        return jsonify({"status": "success"}),201
        


app.run(debug=True)
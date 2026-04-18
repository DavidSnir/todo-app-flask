import pytest
from flask import jsonify
from src.app import create_app
from src.models.task import Task

id="306aee1c-2f9c-427d-822a-3ea0cc15b6c9"

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_all_tasks(client):
    response = client.get('/tasks')
    data = response.get_json()
    print(data)
    tasks_list = [Task.from_dict(task) for task in list(data["tasks"])]
    for task in tasks_list:
        print(task.to_json())
    assert response
    
def test_get_task_by_id(client):
    response = client.get(f"/tasks/{id}")
    data = response.get_json()
    print(data)
    assert response
    
def test_create_task(client):    
    
    task_name_empty = {"title":""}
    task_name_space = {"title":"   "}
    task_name_wrong_key = {"titl":""}
    task_name_regular = {"title":"Created Task"}
    
    response = client.post('/tasks',json=task_name_empty)
    data = response.get_json()
    task = Task.from_dict(data['task'])
    assert task.title == "untitled"
    
    response = client.post('/tasks',json=task_name_space)
    data = response.get_json()
    assert data["error"]
    
    response = client.post('/tasks',json=task_name_wrong_key)
    data = response.get_json()
    assert data["error"]
    
    response = client.post('/tasks',json=task_name_regular)
    data = response.get_json()
    task = Task.from_dict(data['task'])
    assert task.title == "Created Task"
    
def test_edit_task(client):
    task_edits:list[(dict,bool)] = [
    ({"title":""},False),
    ({"title":"   "},False),
    ({"titl":"edited"},False),
    ({"title":"edited"},True),
    ({"title":"edited","is_complete":123},False),
    ({"title":"edited","is_complete":True},True),
    ({"title":"edited","is_completee":True},False),

    ]
    for dict, test in task_edits:
        print(dict)
        response = client.patch(f"/tasks/{id}",json=dict)
        data = response.get_json()
        if test:
            assert data["status"]
        else:
            assert data["error"]
 
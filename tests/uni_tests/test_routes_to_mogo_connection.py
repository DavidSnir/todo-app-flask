import pytest
from src.app import create_app
from src.models.task import Task

@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_task(client):
    response = client.post('/tasks', json={"title": "Test Task"})
    data = response.get_json()
    task_id = data['task']['_id']
    yield data['task']
    client.delete(f"/tasks/{task_id}")

def test_get_all_tasks(client, test_task):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert any(task['_id'] == test_task['_id'] for task in data["tasks"])
    
def test_get_task_by_id(client, test_task):
    response = client.get(f"/tasks/{test_task['_id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["_id"] == test_task["_id"]
    assert data["title"] == test_task["title"]
    
def test_create_task(client):    
    response = client.post('/tasks', json={"title": "Created Task"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"]["title"] == "Created Task"
    
    response = client.post('/tasks', json={"title": ""})
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"]["title"] == "untitled"
    
    response = client.post('/tasks', json={"title": "   "})
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"]["title"] == "untitled"
    
    response = client.post('/tasks', json={"wrong_key": "val"})
    assert response.status_code == 400
    
    response = client.post('/tasks', json={})
    assert response.status_code == 400
    
def test_edit_task(client, test_task):
    task_id = test_task['_id']
    
    response = client.patch(f"/tasks/{task_id}", json={"title": "Edited Title", "is_complete": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["task"]["title"] == "Edited Title"
    assert data["task"]["is_complete"] is True
    
    response = client.patch(f"/tasks/{task_id}", json={"invalid_field": "val"})
    assert response.status_code == 400
    
    response = client.patch(f"/tasks/{task_id}", json={})
    assert response.status_code == 400
    
    response = client.patch(f"/tasks/{task_id}", json={"title": ""})
    assert response.status_code == 400

def test_delete_task(client):
    create_response = client.post('/tasks', json={"title": "Delete Me"})
    task_id = create_response.get_json()['task']['_id']
    
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["status"] == "success"
    
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_recursive_delete(client):
    parent_resp = client.post('/tasks', json={"title": "Parent Task"})
    parent_id = parent_resp.get_json()['task']['_id']
    
    from src.routes.tasks import task_manager
    parent_task_obj = task_manager.get_task_by_id(parent_id)
    sub_task_obj = parent_task_obj.create_sub_task(title="Sub Task")
    task_manager.add_task(sub_task_obj)
    sub_id = str(sub_task_obj._id)
    
    assert task_manager.get_task_by_id(sub_id) is not None
    
    rec_del_resp = client.delete(f"/tasks/{parent_id}/r")
    assert rec_del_resp.status_code == 200
    data = rec_del_resp.get_json()
    assert data["status"] == "success"
    assert data["deleted_count"] >= 2
    
    assert client.get(f"/tasks/{parent_id}").status_code == 404
    assert client.get(f"/tasks/{sub_id}").status_code == 404
 
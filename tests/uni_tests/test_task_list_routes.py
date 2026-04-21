import pytest
from src.app import create_app
from src.models.task_list import TaskList
from src.models.task import Task
from src.database.connection import get_collection
from src.database.manager import TaskManager
import uuid

@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def task_manager():
    # Since create_app() is already called in client fixture (module scope),
    # the database is already initialized.
    return TaskManager(get_collection("tasks"))

@pytest.fixture
def test_list(client):
    response = client.post('/lists', json={"title": "Test List"})
    data = response.get_json()
    list_id = data['list']['_id']
    yield data['list']
    client.delete(f"/lists/{list_id}")

def test_get_all_lists(client, test_list):
    response = client.get('/lists')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert any(lst['_id'] == test_list['_id'] for lst in data["lists"])

def test_get_list_by_id(client, test_list):
     
    response = client.get(f"/lists/{test_list['_id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["_id"] == test_list["_id"]
    assert data["title"] == test_list["title"]

def test_create_list(client):
    response = client.post('/lists', json={"title": "New List"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["list"]["title"] == "New List"
    
    # Test default title
    response = client.post('/lists', json={"title": ""})
    assert response.status_code == 201
    data = response.get_json()
    assert data["list"]["title"] == "untitled"
    
    # Test invalid inputs
    assert client.post('/lists', json={}).status_code == 400
    assert client.post('/lists', json={"wrong_key": "val"}).status_code == 400

def test_edit_list(client, test_list):
    list_id = test_list['_id']
    response = client.patch(f"/lists/{list_id}", json={"title": "Updated List Title"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["list"]["title"] == "Updated List Title"
    
    # Test invalid field
    assert client.patch(f"/lists/{list_id}", json={"is_complete": True}).status_code == 400
    # Test empty title
    assert client.patch(f"/lists/{list_id}", json={"title": ""}).status_code == 400

def test_delete_list(client, task_manager):
    # Create a list and a task inside it
    list_resp = client.post('/lists', json={"title": "Delete List Test"})
    list_id = list_resp.get_json()['list']['_id']
    
    # Manually add a task with this list_id as parent_id
    task = Task(title="Task in list", parent_id=uuid.UUID(list_id))
    task_manager.add_task(task)
    task_id = str(task._id)
    
    # Delete the list (non-recursive)
    response = client.delete(f"/lists/{list_id}")
    assert response.status_code == 200
    assert response.get_json()["status"] == "success"
    
    # Check list is gone
    assert client.get(f"/lists/{list_id}").status_code == 404
    
    # Check task still exists and its parent_id is "None"
    task_resp = client.get(f"/tasks/{task_id}")
    assert task_resp.status_code == 200
    assert task_resp.get_json()["parent_id"] == "None"
    
    # Cleanup task
    client.delete(f"/tasks/{task_id}")

def test_recursive_delete_list(client, task_manager):
    # Create a list
    list_resp = client.post('/lists', json={"title": "Recursive Delete List Test"})
    list_id = list_resp.get_json()['list']['_id']
    
    # Add a task and a sub-task
    task = Task(title="Task in list", parent_id=uuid.UUID(list_id))
    task_manager.add_task(task)
    task_id = str(task._id)
    
    sub_task = task.create_sub_task(title="Sub-task of task in list")
    task_manager.add_task(sub_task)
    sub_task_id = str(sub_task._id)
    
    # Recursive delete
    response = client.delete(f"/lists/{list_id}/r")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["deleted_tasks_count"] >= 2
    
    # Check everything is gone
    assert client.get(f"/lists/{list_id}").status_code == 404
    assert client.get(f"/tasks/{task_id}").status_code == 404
    assert client.get(f"/tasks/{sub_task_id}").status_code == 404

import pytest
from src.app import create_app
from src.database.connection import get_collection
from src.database.manager import TaskManager
from src.models.task import Task

@pytest.fixture
def task_manager():
    # app initialization is needed to ensure init_db is called if it was doing something context-specific,
    # but here get_collection is independent. Still, we use create_app to stay consistent with user request.
    app = create_app()
    app.config["TESTING"] = True
    return TaskManager(get_collection("tasks"))

def test_create_task(task_manager):
    new_task = Task()

    task_manager.add_task(new_task)
    assert task_manager.collection is not None
    print("create task done\n")

def test_get_tasks(task_manager):
    all_tasks: list[Task] = task_manager.get_all_tasks()
    for task in all_tasks:
        print(task.to_json())
    assert all_tasks is not None
    print("get all tasks done\n")

def test_get_task_by_id(task_manager):
    new_task = Task("get task by id test")

    # give short id
    get_task = task_manager.get_task_by_id("wrongId")
    assert get_task is None
    
    task_manager.add_task(new_task)
    get_task = task_manager.get_task_by_id(str(new_task._id))
    print(get_task.to_json())
    assert get_task is not None
    print("get task by id done\n")

def test_get_tasks_children(task_manager):
    
    parent_task = Task("Parent Task")
    
    for i in range(1,10):
        child_task = parent_task.create_sub_task(f"Child Task {i}")
        task_manager.add_task(child_task)
    sub_tasks = task_manager.get_sub_tasks(parent_task)
    for task in sub_tasks:
        print(task.to_json())
    assert sub_tasks is not None
    print("get sub tasks done\n")

def test_edit_task(task_manager):
    task = Task("to be edited")

    task_manager.add_task(task)
    edit_data = {"title": "edited task"}
    
    task.edit_task(edit_data)
    result = task_manager.edit_task(task)
    assert result

    print("edit task done\n")

def test_remove_task(task_manager):
    will_be_removed_task = Task("this task is doomed")
    
    if task_manager.add_task(will_be_removed_task):
        result: tuple = task_manager.remove_task(will_be_removed_task)
        assert result[0], result[1]
    
    #remove none existense task
    result: tuple = task_manager.remove_task(will_be_removed_task)
    print(result[1])
    assert not result[0]
    
    a_sub_task = will_be_removed_task.create_sub_task("a sub task")
    if task_manager.add_task(will_be_removed_task):
        if task_manager.add_task(a_sub_task):
            result: tuple = task_manager.remove_task(will_be_removed_task)
            print(result[1]) 
            assert not result[0]

def test_remove_task_and_sub_tasks(task_manager):
    will_be_removed_task = Task("this task is doomed")
    
    if task_manager.add_task(will_be_removed_task):
        result: tuple = task_manager.remove_task_and_sub_tasks(will_be_removed_task)
        assert result[0], result[1]
    
    #remove none existense task
    result: tuple = task_manager.remove_task_and_sub_tasks(will_be_removed_task)
    print(result[1])
    assert not result[0]
    
    for i in range(1,11):
        a_sub_task = will_be_removed_task.create_sub_task(f"a sub task {i}")
        task_manager.add_task(a_sub_task)
        for j in range(1,4):
            a_sub_sub_task = a_sub_task.create_sub_task(f"sub task {j} of sub task {i}")
            task_manager.add_task(a_sub_sub_task)
        
    if task_manager.add_task(will_be_removed_task):
        result: tuple = task_manager.remove_task_and_sub_tasks(will_be_removed_task)
        print(f"there were a totla of {result[1]} tasks removed") 
        assert result[0]

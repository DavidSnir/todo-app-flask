import pytest
from src.models.task import Task
from src.database.connection import database as db
from src.database.manager import TaskManager

def test_create_task():
    task_manager = TaskManager(db.tasks)
    new_task = Task()

    task_manager.add_task(new_task)
    assert task_manager.collection is not None
    print("create task done\n")

def test_get_tasks():
    task_manager = TaskManager(db.tasks)

    all_tasks: list[Task] = task_manager.get_all_tasks()
    for task in all_tasks:
        print(task.to_json())
    assert all_tasks is not None
    print("get all tasks done\n")

def test_get_task_by_id():
    new_task = Task("get task by id test")
    task_manager = TaskManager(db.tasks)

    task_manager.add_task(new_task)
    get_task = task_manager.get_task_by_id(str(new_task._id))
    print(get_task.to_json())
    assert get_task is not None
    print("get task by id done\n")

def test_get_tasks_children():
    
    parent_task = Task("Parent Task")
    task_manager = TaskManager(db.tasks)
    
    for i in range(1,10):
        child_task = parent_task.create_sub_task(f"Child Task {i}")
        task_manager.add_task(child_task)
    sub_tasks = task_manager.get_sub_tasks(parent_task)
    for task in sub_tasks:
        print(task.to_json())
    assert sub_tasks is not None
    print("get sub tasks done\n")

def test_edit_task():
    task = Task("to be edited")
    task_manager = TaskManager(db.tasks)

    task_manager.add_task(task)
    edit_data = {"title": "edited task"}
    
    task.edit_task(edit_data)
    result = task_manager.edit_task(task)
    assert result

    print("edit task done\n")

def test_remove_task():
    will_be_removed_task = Task("this task is doomed")
    manager = TaskManager(db.tasks)
    
    if manager.add_task(will_be_removed_task):
        result: tuple = manager.remove_task(will_be_removed_task)
        assert result[0], result[1]
    
    #remove none existense task
    result: tuple = manager.remove_task(will_be_removed_task)
    print(result[1])
    assert not result[0]
    
    a_sub_task = will_be_removed_task.create_sub_task("a sub task")
    if manager.add_task(will_be_removed_task):
        if manager.add_task(a_sub_task):
            result: tuple = manager.remove_task(will_be_removed_task)
            print(result[1]) 
            assert not result[0]

def test_remove_task_and_sub_tasks():
    will_be_removed_task = Task("this task is doomed")
    manager = TaskManager(db.tasks)
    
    if manager.add_task(will_be_removed_task):
        result: tuple = manager.remove_task_and_sub_tasks(will_be_removed_task)
        assert result[0], result[1]
    
    #remove none existense task
    result: tuple = manager.remove_task_and_sub_tasks(will_be_removed_task)
    print(result[1])
    assert not result[0]
    
    for i in range(1,11):
        a_sub_task = will_be_removed_task.create_sub_task(f"a sub task {i}")
        manager.add_task(a_sub_task)
        for j in range(1,4):
            a_sub_sub_task = a_sub_task.create_sub_task(f"sub task {j} of sub task {i}")
            manager.add_task(a_sub_sub_task)
        
    if manager.add_task(will_be_removed_task):
        result: tuple = manager.remove_task_and_sub_tasks(will_be_removed_task)
        print(f"there were a totla of {result[1]} tasks removed") 
        assert result[0]
            


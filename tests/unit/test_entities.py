import pytest
from app.domain.entities import Task

def test_task_creation():
    task = Task(title="Test task")
    assert task.title == "Test task"
    assert task.completed is False

def test_task_with_completed():
    task = Task(title="Test", completed=True)
    assert task.completed is True

@pytest.mark.parametrize("invalid_title", ["", None])
def test_invalid_titles(invalid_title):
    with pytest.raises(ValueError):
        Task(title=invalid_title)
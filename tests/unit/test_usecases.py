import pytest
from unittest.mock import Mock, create_autospec
from app.domain.entities import Task
from app.domain.repositories import TaskRepository
from app.usecases.task_usecases import TaskUseCases

class TestTaskUseCases:
    @pytest.fixture
    def mock_repo(self):
        # Usando create_autospec para garantir que implementa todos os métodos
        return create_autospec(TaskRepository)

    @pytest.fixture
    def sample_task(self):
        return Task(id=1, title="Sample task", description="Test", completed=False)

    # Testes para create_task
    def test_create_task_success(self, mock_repo):
        usecase = TaskUseCases(mock_repo)
        task_data = {
            "title": "Valid task", 
            "description": "Test description"
        }
        
        # Cria a task válida primeiro
        task = Task(**task_data)
        created_task = Task(id=1, **task_data)
        mock_repo.create.return_value = created_task
        
        result = usecase.create_task(task)
        
        mock_repo.create.assert_called_once_with(task)
        assert result.id == 1
        assert result.title == "Valid task"
        assert result.description == "Test description"

    def test_create_task_invalid_data(self, mock_repo):
        usecase = TaskUseCases(mock_repo)
        
        # Testa com dados inválidos (deve falhar na criação da Task)
        with pytest.raises(ValueError) as exc_info:
            Task(title="", description="Should fail")  # Título vazio
            
        assert "Title cannot be empty" in str(exc_info.value)
        mock_repo.create.assert_not_called()

    # Testes para get_task_by_id
    def test_get_task_found(self, mock_repo, sample_task):
        mock_repo.get_by_id.return_value = sample_task
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.get_task_by_id(1)
        
        mock_repo.get_by_id.assert_called_once_with(1)
        assert result == sample_task

    def test_get_task_not_found(self, mock_repo):
        mock_repo.get_by_id.return_value = None
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.get_task_by_id(99)
        
        mock_repo.get_by_id.assert_called_once_with(99)
        assert result is None

    # Testes para update_task
    def test_update_task_success(self, mock_repo, sample_task):
        updated_data = {
            "title": "Updated",
            "description": "New desc",
            "completed": True
        }
        updated_task = Task(id=1, **updated_data)
        
        mock_repo.update.return_value = updated_task
        mock_repo.get_by_id.return_value = sample_task
        
        usecase = TaskUseCases(mock_repo)
        result = usecase.update_task(1, updated_task)
        
        mock_repo.update.assert_called_once_with(1, updated_task)
        assert result == updated_task

    def test_update_task_not_found(self, mock_repo):
        mock_repo.get_by_id.return_value = None
        usecase = TaskUseCases(mock_repo)
        task_to_update = Task(id=99, title="Should fail")
        
        result = usecase.update_task(99, task_to_update)
        
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(99)
        mock_repo.update.assert_not_called()

    # Testes para delete_task
    def test_delete_task_success(self, mock_repo):
        mock_repo.delete.return_value = True
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.delete_task(1)
        
        mock_repo.delete.assert_called_once_with(1)
        assert result is True

    def test_delete_task_not_found(self, mock_repo):
        mock_repo.delete.return_value = False
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.delete_task(99)
        
        mock_repo.delete.assert_called_once_with(99)
        assert result is False

    # Testes para list_tasks
    def test_list_tasks_empty(self, mock_repo):
        mock_repo.list_all.return_value = []
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.list_tasks()
        
        mock_repo.list_all.assert_called_once()
        assert result == []

    def test_list_tasks_with_items(self, mock_repo, sample_task):
        mock_repo.list_all.return_value = [sample_task]
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.list_tasks()
        
        mock_repo.list_all.assert_called_once()
        assert len(result) == 1
        assert result[0] == sample_task
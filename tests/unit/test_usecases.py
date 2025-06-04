import pytest
from unittest.mock import Mock
from app.domain.entities import Task
from app.usecases.task_usecases import TaskUseCases

class TestTaskUseCases:
    @pytest.fixture
    def mock_repo(self):
        return Mock()

    @pytest.fixture
    def sample_task(self):
        return Task(id=1, title="Sample task", description="Test", completed=False)

    # Testes para create_task
    def test_create_task_success(self, mock_repo):
        usecase = TaskUseCases(mock_repo)
        task = Task(title="Valid task")
        
        result = usecase.create_task(task)
        
        mock_repo.create.assert_called_once_with(task)
        assert result == task

    def test_create_task_empty_title(self, mock_repo):
        usecase = TaskUseCases(mock_repo)
        with pytest.raises(ValueError, match="Title cannot be empty"):
            usecase.create_task(Task(title=""))

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
        updated_task = Task(id=1, title="Updated", completed=True)
        mock_repo.update.return_value = updated_task
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.update_task(1, updated_task)
        
        mock_repo.update.assert_called_once_with(1, updated_task)
        assert result == updated_task

    def test_update_task_not_found(self, mock_repo, sample_task):
        mock_repo.update.return_value = None
        usecase = TaskUseCases(mock_repo)
        
        result = usecase.update_task(99, sample_task)
        
        mock_repo.update.assert_called_once_with(99, sample_task)
        assert result is None

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

    # Teste para verificação de chamadas do repositório
    def test_repository_methods_called(self, mock_repo):
        usecase = TaskUseCases(mock_repo)
        
        # Chamar todos os métodos
        usecase.create_task(Task(title="Test"))
        usecase.get_task_by_id(1)
        usecase.update_task(1, Task(title="Updated"))
        usecase.delete_task(1)
        usecase.list_tasks()
        
        # Verificar se todos os métodos do repositório foram chamados
        assert mock_repo.create.called
        assert mock_repo.get_by_id.called
        assert mock_repo.update.called
        assert mock_repo.delete.called
        assert mock_repo.list_all.called
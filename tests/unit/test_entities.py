import pytest
from app.domain.entities import Task


@pytest.mark.parametrize("invalid_title, expected_error", [
    ("", "Title cannot be empty or contain only whitespace"),  # Vazio após trim
    ("   ", "Title cannot be empty or contain only whitespace"),  # Só espaços
    ("\t\n", "Title cannot be empty or contain only whitespace"),  # Espaços invisíveis
    (None, "Title cannot be None"),  # None não é permitido
    (123, "Title must be a string")  # Tipo errado
])
def test_invalid_titles(invalid_title, expected_error):
    with pytest.raises(ValueError) as exc_info:
        Task(title=invalid_title, description="Test description")

    assert expected_error in str(exc_info.value), \
        f"Expected error '{expected_error}' not found in '{str(exc_info.value)}'"


def test_title_validations():
    """Testa casos válidos e transformações"""

    # Criação com título válido
    task1 = Task(title="Valid", description="Test")
    assert task1.title == "Valid"

    # Testa remoção de espaços no título
    task2 = Task(title="  Trim me  ", description="Test")
    assert task2.title == "Trim me"

    # Testa título válido com caracteres normais
    task3 = Task(title="Something", description="Test")
    assert task3.title == "Something"

    # Testa descrição opcional
    task4 = Task(title="Test without description")
    assert task4.description is None

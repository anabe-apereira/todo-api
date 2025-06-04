import pytest
from app.domain.entities import Task

@pytest.mark.parametrize("invalid_title, expected_error", [
    ("", "Title cannot be empty"),
    ("   ", "Title cannot be empty or contain only whitespace"),
    ("\t\n", "Title cannot be empty or contain only whitespace"),
    (None, "Title cannot be None"),
    (123, "Title must be a string")
])
def test_invalid_titles(invalid_title, expected_error):
    with pytest.raises(ValueError) as exc_info:
        Task(title=invalid_title, description="Test description")
    assert expected_error in str(exc_info.value)

def test_title_validations():
    # Testa casos válidos
    assert Task(title="Valid", description="Test").title == "Valid"
    assert Task(title="  Trim me  ", description="Test").title == "Trim me"
    
    # Testa casos inválidos
    with pytest.raises(ValueError) as exc_info:
        Task(title="", description="Test")
    assert "Title cannot be empty" in str(exc_info.value)
    
    with pytest.raises(ValueError) as exc_info:
        Task(title=None, description="Test")
    assert "Title cannot be None" in str(exc_info.value)
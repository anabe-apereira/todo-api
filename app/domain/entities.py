from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any


class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., description="Title must be a non-empty string")
    description: Optional[str] = None
    completed: bool = False

    @field_validator('title', mode='before')
    def validate_title_type(cls, v: Any) -> str:
        """Validação do tipo antes das outras validações"""
        if v is None:
            raise ValueError("Title cannot be None")
        if not isinstance(v, str):
            raise ValueError("Title must be a string")
        return v

    @field_validator('title')
    def validate_title_content(cls, v: str) -> str:
        """Validação do conteúdo e mínimo de caracteres"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or contain only whitespace")
        return stripped

    model_config = {
        "from_attributes": True,
        "extra": "forbid"
    }

from pydantic import BaseModel, Field, validator
from typing import Optional, Any

class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=1000, 
                      description="Title must be a non-empty string")
    description: Optional[str] = None
    completed: bool = False

    @validator('title', pre=True)
    def validate_title_pre(cls, v: Any) -> str:
        """Validação do tipo antes das outras validações"""
        if v is None:
            raise ValueError("Title cannot be None")
        if not isinstance(v, str):
            raise ValueError("Title must be a string")
        return v

    @validator('title')
    def validate_title_content(cls, v: str) -> str:
        """Validação do conteúdo após verificação do tipo"""
        if not v.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")
        return v.strip()

    class Config:
        orm_mode = True
        extra = "forbid" 
        error_msg_templates = {
            "value_error.any_str.min_length": "Title cannot be empty",
            "value_error.str.min_length": "Title cannot be empty",
        }
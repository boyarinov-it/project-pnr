from pydantic import BaseModel


class ValidationIssue(BaseModel):
    level: str
    code: str
    message: str


class ProjectValidationResult(BaseModel):
    project_id: int
    is_valid: bool
    issues: list[ValidationIssue]

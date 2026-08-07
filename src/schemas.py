from pydantic import BaseModel, Field, field_validator


class ScanRequest(BaseModel):
    log_path: str
    threshold: int = Field(3, ge=1, le=100)

    @field_validator("log_path")
    @classmethod
    def path_must_be_in_data_folder(cls, v: str) -> str:
        if not v.startswith("data/"):
            raise ValueError("log_path must be inside the data/ folder")
        return v


class PlanRequest(BaseModel):
    threats: list
    budget: int = Field(..., ge=1, le=1000)

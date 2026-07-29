from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEvent:
    ip: str
    timestamp: str
    method: str
    path: str
    status: int
    user_agent: str

@dataclass
class Alert:
    ip: str
    reason: str
    count: int
    severity: str
    at: str

from pydantic import BaseModel, field_validator
from typing import Literal 
from pydantic.networks import IPvAnyAddress    

class LogEventModel(BaseModel):
    ip: IPvAnyAddress
    timestamp: str
    method: str
    path: str
    status: int
    user_agent: str

    @field_validator("status")
    @classmethod
    def status_must_be_valid(cls, v: int) -> int:
        if v < 100 or v > 599:
            raise ValueError(f"Invalid status code: {v}")
        return v

class AlertModel(BaseModel):
    ip: IPvAnyAddress
    reason: str
    count: int
    severity: Literal["low", "medium", "high", "critical"]
    at: str    
from pydantic import BaseModel
from datetime import date

class CycleBase(BaseModel):
    name: str
    start_date: date

class CycleCreate(CycleBase):
    """Schema for creating a new cycle entry."""
    pass

class CycleResponse(CycleBase):
    """Schema for returning cycle data."""
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional


class FarmerContext(BaseModel):
    farmer_name: Optional[str] = None
    crop: str
    growth_stage: Optional[str] = None
    planned_activity: Optional[str] = None
    location: str


class Notification(BaseModel):
    type: str
    priority: str
    title: str
    message: str
    action: str
    reason: str
    crop: str
    activity: Optional[str] = None


class AdvisoryResponse(BaseModel):
    location: str
    crop: str
    notifications: list[Notification]
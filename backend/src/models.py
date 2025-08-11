from pydantic import BaseModel
from typing import Optional

class Recommendation(BaseModel):
    title: str
    artist: str
    genre: str
    link: str

class RecommendationResponse(BaseModel):
    recommendation: Recommendation

class IdeaData(BaseModel):
    idea: str

class TokenStatus(BaseModel):
    has_manual_token: bool
    auto_generation_enabled: bool
    last_refresh: Optional[str] = None
    next_refresh: Optional[str] = None

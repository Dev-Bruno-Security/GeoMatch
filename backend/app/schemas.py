from pydantic import BaseModel
from typing import Optional, List, Any


class AddressIn(BaseModel):
    address: str


class ProviderResultOut(BaseModel):
    provider_name: str
    matched_address: str
    cep: Optional[str] = None
    score: float
    extra_metadata: Optional[Any] = None
    classification: Optional[str] = None


class AddressOut(BaseModel):
    id: int
    raw_address: str
    normalized_address: str
    cep: Optional[str] = None
    status: Optional[str] = None
    winner_provider: Optional[str] = None
    best_score: Optional[float] = None
    results: List[ProviderResultOut]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    raw_address = Column(String, index=True)
    normalized_address = Column(String, index=True)
    cep = Column(String, index=True, nullable=True)
    status = Column(String, default="processed")
    created_at = Column(DateTime, default=datetime.utcnow)

    provider_results = relationship("ProviderResult", back_populates="address")


class ProviderResult(Base):
    __tablename__ = "provider_results"
    id = Column(Integer, primary_key=True, index=True)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    provider_name = Column(String, index=True)
    matched_address = Column(String)
    cep = Column(String, nullable=True)
    score = Column(Float)
    extra_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    address = relationship("Address", back_populates="provider_results")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

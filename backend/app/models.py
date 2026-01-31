from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    filename = Column(Text, nullable=False)
    original_file_url = Column(Text)
    processed_file_url = Column(Text)
    helmet_detected = Column(Text)
    number_plate_detected = Column(Text)
    plate_number = Column(Text)

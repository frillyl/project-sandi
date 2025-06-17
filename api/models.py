from sqlalchemy import Column, Integer, Text
from database import Base

class HasilOCR(Base):
    __tablename__ = 'arsips'
    
    id = Column(Integer, primary_key=True, index=True)
    judul = Column(Text)
    hasil_ocr = Column(Text)
    summary = Column(Text, nullable=True)
    summary_abstractive = Column(Text, nullable=True)
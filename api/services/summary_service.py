from database import SessionLocal
from models import HasilOCR
from summarizer import summarize_text
from fastapi import HTTPException

def summarize_by_id(id: int):
    db = SessionLocal()
    hasil = db.query(HasilOCR).filter(HasilOCR.id == id).first()
    if not hasil:
        raise HTTPException(status_code=404, detail="Data OCR Tidak Ditemukan")
    
    if hasil.summary:
        return {"id": id, "summary": hasil.summary}
    
    summary = summarize_text(hasil.hasil_ocr)
    hasil.summary = summary
    db.commit()
    return {"id": id, "summary": summary}

def split_into_chunks(text, max_tokens=512):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])

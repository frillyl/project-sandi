from database import SessionLocal
from models import HasilOCR
from summarizer import summarize_text
from services.ollama_service import abstractive_summary
from services.huggingface_service import mistral_abstractive_summary
from services.huggingface_service import summarize_with_indobart
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

def summarize_by_id_abstractive(id: int):
    db = SessionLocal()
    hasil = db.query(HasilOCR).filter(HasilOCR.id == id).first()
    if not hasil:
        raise HTTPException(status_code=404, detail="Data OCR Tidak Ditemukan")
    
    if hasil.summary_abstractive:
        return {"id": id, "summary_abstractive": hasil.summary_abstractive}
    
    summary = abstractive_summary(hasil.hasil_ocr)
    hasil.summary_abstractive = summary
    db.commit()
    return {"id": id, "summary_abstractive": summary}

def summarize_with_huggingface(id: int):
    db = SessionLocal()
    hasil = db.query(HasilOCR).filter(HasilOCR.id == id).first()
    if not hasil:
        raise HTTPException(status_code=404, detail="Data OCR Tidak Ditemukan")

    if hasil.summary_abstractive:
        return {"id": id, "summary_abstractive": hasil.summary_abstractive}

    # Buat prompt untuk LLM
    prompt = f"[INST] Buat ringkasan singkat, jelas, dan mudah dipahami dari dokumen berikut:\n\n{hasil.hasil_ocr} [/INST]"

    try:
        summary = mistral_abstractive_summary(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    hasil.summary_abstractive = summary
    db.commit()
    return {"id": id, "summary_abstractive": summary}

def summarize_with_indobart_service(id: int):
    db = SessionLocal()
    hasil = db.query(HasilOCR).filter(HasilOCR.id == id).first()
    if not hasil:
        raise HTTPException(status_code=404, detail="Data OCR Tidak Ditemukan")

    if hasil.summary_abstractive:
        return {"id": id, "summary_abstractive": hasil.summary_abstractive}

    # Batasi panjang teks input (maks. 1024 kata)
    cleaned_text = " ".join(hasil.hasil_ocr.split()[:1024])

    try:
        summary = summarize_with_indobart(cleaned_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    hasil.summary_abstractive = summary
    db.commit()
    return {"id": id, "summary_abstractive": summary}
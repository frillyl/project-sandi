from fastapi import APIRouter
from services.summary_service import summarize_by_id
from services.summary_service import summarize_by_id_abstractive
from services.summary_service import summarize_with_huggingface
from services.summary_service import summarize_with_indobart_service

router = APIRouter()

@router.get("/summarize/{id}")
def get_summary(id: int):
    return summarize_by_id(id)

@router.get("/summarize_abstractive/{id}")
def get_abstractive_summary(id: int):
    return summarize_by_id_abstractive(id)

@router.get("/summarize_hf/{id}")
def get_summary_hf(id: int):
    return summarize_with_huggingface(id)

@router.get("/summarize_indobart/{id}")
def get_summary_indobart(id: int):
    return summarize_with_indobart_service(id)

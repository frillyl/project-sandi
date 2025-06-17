from fastapi import APIRouter
from services.summary_service import summarize_by_id

router = APIRouter()

@router.get("/summarize/{id}")
def get_summary(id: int):
    return summarize_by_id(id)
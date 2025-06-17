from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.recommender import get_recommendations

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)

@router.get("/{doc_id}")
def recommend_documents(doc_id: int, db: Session = Depends(get_db)):
    result = get_recommendations(db, doc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan atau tidak ada rekomendasi.")
    return {
        "id": doc_id,
        "recommendations": result
    }

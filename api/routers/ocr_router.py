from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.ocr_service import perform_ocr

router = APIRouter()

@router.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        return await perform_ocr(file)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from database import SessionLocal
from models import User, Document, Correction
from schemas import CorrectionCreate
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/corrections", tags=["Corrections"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_correction(
    correction: CorrectionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_correction = Correction(
        document_id=correction.document_id,
        original_text=correction.original_text,
        suggested_text=correction.suggested_text,
    )
    db.add(new_correction)
    db.commit()
    db.refresh(new_correction)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Corrections created successfully.",
        },
    )


@router.get("")
def get_corrections(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # Fetch corrections related to the current user
    corrections = (
        db.query(Correction, Document)
        .join(Document, Document.id == Correction.document_id)
        .filter(
            Document.user_id == current_user
        )  # Ensure the current user is related to the document
        .all()
    )
    
    # Serialize the corrections
    serialized_corrections = [
        {
            "id": str(correction.id),
            "document_id": str(correction.document_id),
            "original_text": correction.original_text,
            "suggested_text": correction.suggested_text,
        }
        for correction, document in corrections
    ]

    return JSONResponse(
        status_code=200,
        content={
            "message": "Corrections retrieved successfully.",
            "data": serialized_corrections,
        },
    )

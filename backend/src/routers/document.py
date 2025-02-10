from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Document, User
from schemas import DocumentCreate
from auth import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_doc = Document(
        user_id=current_user,
        content=doc.content,
        errors=doc.errors,
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Document created successfully",
            "data": {"document_id": str(new_doc.id)},
        },
    )


@router.get("/{doc_id}")
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if (
        not doc
        or doc.user_id
        != db.query(User).filter(User.username == current_user).first().id
    ):
        raise HTTPException(
            status_code=404, detail="Document not found or unauthorized"
        )
    return doc


@router.get("")
def get_documents(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # Fetch documents related to the current user
    documents = db.query(Document).filter(Document.user_id == current_user).all()

    # Serialize the documents
    serialized_documents = [
        {
            "id": str(doc.id),
            "user_id": str(doc.user_id),
            "content": doc.content,
            "errors": doc.errors,
            "timestamp": doc.timestamp.isoformat() if doc.timestamp else None,
        }
        for doc in documents
    ]

    return JSONResponse(
        status_code=200,
        content={
            "message": "Get list documents successfully.",
            "data": serialized_documents,
        },
    )

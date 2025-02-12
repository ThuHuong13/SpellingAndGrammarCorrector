from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from auth import get_current_user
from nlp import nlp
from schemas import Checker

router = APIRouter(prefix="/checker", tags=["Checker"])


@router.post("/spell")
async def spell_check(content: Checker, current_user: str = Depends(get_current_user)):
    correction = nlp.correct_spelling(content.content)
    correction_highlighted = nlp.get_highlighted_text(content.content, correction)
    correction_edits = nlp.get_edits(content.content, correction)
    content = {
        "message": "Spell check successful",
        "data": {
            "correction": correction,
            "correction_highlighted": correction_highlighted,
            "correction_edits": correction_edits,
        },
    }
    print(content)
    return JSONResponse(
        status_code=200,
        content=content,
    )


@router.post("/grammar")
async def grammar_check(
    content: Checker, current_user: str = Depends(get_current_user)
):
    correction = nlp.correct_grammar(content.content)
    correction_highlighted = nlp.get_highlighted_text(content.content, correction)
    correction_edits = nlp.get_edits(content.content, correction)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Grammar check successful",
            "data": {
                "correction": correction,
                "correction_highlighted": correction_highlighted,
                "correction_edits": correction_edits,
            },
        },
    )

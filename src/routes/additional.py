from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import additional as repository_additional

router = APIRouter(prefix='/add', tags=["additional"])


@router.get("/birthdays")
async def read_birthday(
        db: Session = Depends(get_db)
):

    contacts = await repository_additional.read_birthday(db)

    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contacts


@router.get("/search")
async def search_by_phrase(
        phrase: str,
        db: Session = Depends(get_db)
):

    contacts = await repository_additional.search_by_phrase(phrase, db)

    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

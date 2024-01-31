from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, extract
from datetime import datetime, timedelta
import calendar

from src.database.db import get_db
from src.database.models import Contact


async def read_birthday(db: Session = Depends(get_db)):
    today = datetime.now().date()
    last_day_in_month = calendar.monthrange(today.year, today.month)[1]
    end_date = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        or_(
            and_(
                extract("month", Contact.date_of_birth) == today.month,
                extract("day", Contact.date_of_birth) >= today.day,
                or_(
                    extract("day", Contact.date_of_birth) <= end_date.day,
                    extract("day", Contact.date_of_birth) <= last_day_in_month
                ),
            ),
            and_(
                extract("month", Contact.date_of_birth) == (today + timedelta(days=7)).month,
                extract("day", Contact.date_of_birth) <= (end_date - timedelta(days=7)).day
            )
        )
    ).all()

    return contacts


async def search_by_phrase(phrase: str, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(
        or_(
            Contact.name.like(f"%{phrase}%"),
            Contact.last_name.like(f"%{phrase}%"),
            Contact.email.like(f"%{phrase}%")
        )
    ).all()

    return contacts

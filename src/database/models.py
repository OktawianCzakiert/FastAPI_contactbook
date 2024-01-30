from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone_no = Column(String(50))
    date_of_birth = Column(Date)
    description = Column(String(250))

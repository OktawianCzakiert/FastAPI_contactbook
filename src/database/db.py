from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import os


# username = os.getenv("Postgres_username")
# password = os.getenv("Postgres_password")
# db_name = os.getenv("Postgres_db_name")
# print(username, password, db_name)

# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@localhost:5432/{db_name}"

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/fastapi_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

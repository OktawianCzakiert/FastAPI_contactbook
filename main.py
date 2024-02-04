from fastapi import FastAPI


from src.routes import contacts, additional, auth

app = FastAPI()

app.include_router(contacts.router, prefix='')
app.include_router(additional.router, prefix='')
app.include_router(auth.router, prefix='')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

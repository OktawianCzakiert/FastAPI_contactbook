"""
This module contains a FastAPI application with various routers and middleware configurations.
It defines routes for contacts, additional features, authentication, and user management.
The application utilizes Redis for rate limiting using FastAPI Limiter.
"""

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter


from src.routes import contacts, additional, auth, users
from src.conf.config import settings


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix='')
app.include_router(additional.router, prefix='')
app.include_router(auth.router, prefix='')
app.include_router(users.router, prefix='')


@app.on_event("startup")
async def startup():
    """
    Perform startup operations for the FastAPI application.
    Connects to Redis server defined in settings for rate limiting initialization.
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root():
    """
    Root endpoint of the FastAPI application.
    Implements rate limiting with a limit of 2 requests per 5 seconds.
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=3000, reload=True)

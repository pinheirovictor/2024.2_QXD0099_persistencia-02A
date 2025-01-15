from fastapi import FastAPI
from models import Base
from databse import engine
from crud import router
import logging
from fastapi import Request
import time

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

logging.basicConfig(level=logging.INFO)
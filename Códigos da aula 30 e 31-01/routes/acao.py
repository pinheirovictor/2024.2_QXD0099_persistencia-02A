from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config import db
from schemas import Aluno
from typing import List
from typing import Dict, Any

router = APIRouter()

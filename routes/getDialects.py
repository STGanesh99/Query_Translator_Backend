from fastapi import FastAPI, Request, Response, APIRouter
from sqlglot.dialects.dialect import Dialect as Dialect, Dialects as Dialects
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlglot import parse_one, transpile, errors, expressions as exp, ErrorLevel
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import build_scope
from sqlglot.optimizer import optimize

dialect_router = APIRouter()

@dialect_router.get("/dialects", tags=["Fetch Dialects"])
async def get_dialects():
    return {"dialects": list(Dialects.__members__.keys())}

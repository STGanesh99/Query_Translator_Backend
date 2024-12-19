from fastapi import FastAPI, Request, Response, APIRouter
from sqlglot.dialects.dialect import Dialect as Dialect, Dialects as Dialects
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlglot import parse_one, transpile, errors, expressions as exp, ErrorLevel
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import build_scope
from sqlglot.optimizer import optimize
from models.requestModels import FetchInfo


analyze_router = APIRouter()

@analyze_router.post("/fetchinfo", tags=["Analyze Query"])
async def fetch_info(request: Request, response: Response, iqf:FetchInfo):

    output_query = ''
    columns = []
    tables = []

    if (iqf.analyze):
        columns = set()
        tables = set()
        ast = parse_one(iqf.inputQuery, read=iqf.inputDialect.lower(), dialect=iqf.inputDialect.lower())
        qualfied_ast = qualify(ast)
        for column in qualfied_ast.find_all(exp.Column):
            columns.add(str(column).replace('"', ''))

        root = build_scope(ast)
        for scope in root.traverse():

            for alias, (node, source) in scope.selected_sources.items():
                if isinstance(source, exp.Table):
                    tables.add(str(source).replace('"', ''))

    
    if (iqf.optimize):
        output_query = optimize(parse_one(iqf.inputQuery, read=iqf.inputDialect.lower(), dialect=iqf.inputDialect.lower())).sql().lower()
    
    return {"outputQuery": output_query, "selectedColumns": list(columns), "selectedTables": list(tables)}
    
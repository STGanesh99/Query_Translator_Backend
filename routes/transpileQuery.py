from fastapi import FastAPI, Request, Response, APIRouter
from sqlglot.dialects.dialect import Dialect as Dialect, Dialects as Dialects
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlglot import parse_one, transpile, errors, expressions as exp, ErrorLevel
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import build_scope
from sqlglot.optimizer import optimize
from models.requestModels import InputQueryInfo

transpile_router = APIRouter()

@transpile_router.post("/transpile", tags=["Transpile Query"])
async def transpile_input(request: Request, response: Response, iqf:InputQueryInfo):
    try:

   
        input_query = iqf.inputQuery
        output_query = transpile(input_query, read=iqf.inputDialect.lower(), write=iqf.outputDialect.lower(), identity=False, unsupported_level=ErrorLevel.RAISE)[0]
        columns = set()
        tables = set()
        ast = parse_one(input_query, read=iqf.inputDialect.lower(), dialect=iqf.outputDialect.lower())
        qualfied_ast = qualify(ast)
        for column in qualfied_ast.find_all(exp.Column):
            columns.add(str(column).replace('"', ''))
        
        # for table in qualfied_ast.find_all(exp.Table):
        #     tables.add(str(table).replace('"', ''))
        root = build_scope(ast)
        for scope in root.traverse():

            for alias, (node, source) in scope.selected_sources.items():
                if isinstance(source, exp.Table):
                    tables.add(str(source).replace('"', ''))
        
        if (iqf.optimize):
            output_query = optimize(parse_one(sql=output_query,read=iqf.outputDialect.lower(),dialect=iqf.outputDialect.lower())).sql().lower()
        
        return {"outputQuery": output_query, "selectedColumns": list(columns), "selectedTables": list(tables)}
    except errors.UnsupportedError as e:
        response.status_code = 500
        return {"error": f"{e}"}
    except Exception as e:
        response.status_code = 500
        return {"error": "Please check the Input Query for errors"}

from fastapi import FastAPI, Request, Response
from sqlglot.dialects.dialect import Dialect as Dialect, Dialects as Dialects
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlglot import parse_one, transpile, errors, expressions as exp, ErrorLevel
from sqlglot.optimizer.qualify import qualify
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust port as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputQueryInfo(BaseModel):
    inputQuery: str
    inputDialect: str
    outputDialect: str

@app.get("/dialects")
async def get_dialects():
    return {"dialects": list(Dialects.__members__.keys())}

@app.post("/transpile")
async def transpile_input(request: Request, response: Response, iqf:InputQueryInfo):
    try:
        output_query = transpile(iqf.inputQuery, read=iqf.inputDialect.lower(), write=iqf.outputDialect.lower(), identify=True, unsupported_level=ErrorLevel.RAISE)[0]
        columns = set()

        ast = parse_one(iqf.inputQuery)
        
        for column in qualify(ast).find_all(exp.Column):
            columns.add(str(column).replace('"', ''))
        

        return {"outputQuery": output_query, "selectedColumns": list(columns)}
    except Exception as e:
        response.status_code = 500
        return {"error": "Please check the Input Query for errors"}



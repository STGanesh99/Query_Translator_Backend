from fastapi import FastAPI
from sqlglot.dialects.dialect import Dialect as Dialect, Dialects as Dialects
from fastapi.middleware.cors import CORSMiddleware
from routes.getDialects import dialect_router
from routes.analyzeQuery import analyze_router
from routes.transpileQuery import transpile_router

tags_metadata = [
    {
        "name": "Fetch Dialects",
        "description": "Fetch possible dialects from the server",
    },
    {
        "name": "Transpile Query",
        "description": "Transpile the query from input dialect to output dialect",
    },
    {
        "name": "Analyze Query",
        "description": "Intelligently analyze the query"
    }
]

app = FastAPI(
    title="SQL Transpiler",
    description="Single tool for making query transpiling and analysis, easy !",
    summary="SQL Transpiler microservice is written in python using FAST API Framework",
    version="0.0.1",
    contact={
        "name": "Thillai Ganesh S",
        "email": "sthillai@athenahealth.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust port as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transpile_router)
app.include_router(analyze_router)
app.include_router(dialect_router)


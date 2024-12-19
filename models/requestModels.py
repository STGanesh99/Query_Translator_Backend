from pydantic import BaseModel

class InputQueryInfo(BaseModel):
    inputQuery: str
    inputDialect: str
    outputDialect: str
    optimize: bool

class FetchInfo(BaseModel):
    inputDialect: str
    inputQuery: str
    analyze: bool
    optimize: bool
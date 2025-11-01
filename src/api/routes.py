from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.workflow.graph import process_query

router = APIRouter(prefix="/api/v1", tags=["agent"])

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    query_type: str
    analysis: dict
    vega_spec: dict
    data_count: int

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """Process user query through multi-agent workflow"""
    try:
        result = await process_query(request.query)
        
        if not result.get("vega_spec"):
            raise HTTPException(status_code=500, detail="Failed to generate visualization")
        
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "SciSciNet Agent API"}


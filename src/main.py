from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from src.api.routes import router

load_dotenv()

app = FastAPI(
    title="SciSciNet Agent API",
    description="Multi-agent LLM framework for automated data analysis and visualization",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "ok",
        "message": "SciSciNet Agent Backend API",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import InningsSummaryResponse, ErrorResponse
from services import get_innings_summary

app = FastAPI(
    title="Khel AI Innings Summary API",
    version="1.0.0",
    description="API for detailed innings-level analytics."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Innings Summary API is live", "docs": "/docs"}

@app.get(
    "/api/innings/{innings_id}/summary/",
    response_model=InningsSummaryResponse,
    responses={404: {"model": ErrorResponse}},
)
def read_innings_summary(innings_id: int):
    result = get_innings_summary(innings_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Innings data not found")
    return result
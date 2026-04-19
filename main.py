from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import InningsSummaryInput, InningsSummaryResponse, ErrorResponse
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


@app.post(
    "/api/innings/summary/",
    response_model=InningsSummaryResponse,
    responses={500: {"model": ErrorResponse}},
)
def read_innings_summary(input_data: InningsSummaryInput):
    try:
        return get_innings_summary(input_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

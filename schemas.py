# schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field

class BatterStat(BaseModel):
    name: str
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float

class BowlerStat(BaseModel):
    name: str
    overs: str
    runs: int
    wickets: int
    economy: float

class InningsSummaryResponse(BaseModel):
    innings_id: int
    batting_team: str
    bowling_team: str
    total_runs: int
    wickets: int
    legal_balls: int
    overs: str
    run_rate: float
    batters: List[BatterStat]
    bowlers: List[BowlerStat]
    top_batter: str
    top_bowler: str
    recent_balls: List[str]

class ErrorResponse(BaseModel):
    detail: str
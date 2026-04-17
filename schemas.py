from typing import List, Optional
from pydantic import BaseModel

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

class OverSummary(BaseModel):
    over_number: int
    bowler: str
    runs: int
    wickets: int
    ball_labels: List[str]

class InningsSummaryResponse(BaseModel):
    innings_id: int
    batting_team: str
    total_runs: int
    wickets: int
    overs: str
    batters: List[BatterStat]
    bowlers: List[BowlerStat]
    over_by_over: List[OverSummary]
    recent_balls: List[str]

class ErrorResponse(BaseModel):
    detail: str
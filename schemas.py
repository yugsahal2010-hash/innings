from typing import List, Optional
from pydantic import BaseModel


class BallEvent(BaseModel):
    striker: str
    bowler: str
    runs_off_bat: int
    extras: int
    is_legal_delivery: bool
    wicket_fell: bool


class InningsSummaryInput(BaseModel):
    innings_id: int
    batting_team: str
    ball_events: List[BallEvent]


class TopBatter(BaseModel):
    name: str
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float


class TopBowler(BaseModel):
    name: str
    overs: str
    runs: int
    wickets: int
    economy: float


class InningsSummaryResponse(BaseModel):
    innings_id: int
    batting_team: str
    total_runs: int
    wickets: int
    overs: str
    run_rate: float
    top_batter: Optional[TopBatter]
    top_bowler: Optional[TopBowler]
    recent_balls: List[str]


class ErrorResponse(BaseModel):
    detail: str

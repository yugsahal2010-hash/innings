from typing import List, Optional
from pydantic import BaseModel


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


class BatterInfo(BaseModel):
    name: str


class BowlerInfo(BaseModel):
    name: str


class InningsSummaryInput(BaseModel):
    innings_id: int
    batting_team: str
    total_runs: int
    wickets: int
    overs: str
    top_batter: TopBatter
    top_bowler: TopBowler
    recent_balls: List[str]
    all_batters: List[BatterInfo]   # 11 batters
    all_bowlers: List[BowlerInfo]   # 11 bowlers


class InningsSummaryResponse(BaseModel):
    innings_id: int
    batting_team: str
    total_runs: int
    wickets: int
    overs: str
    run_rate: float
    top_batter: TopBatter
    top_bowler: TopBowler
    recent_balls: List[str]


class ErrorResponse(BaseModel):
    detail: str

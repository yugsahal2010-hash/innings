from typing import Dict, Any


def _overs_to_decimal(overs_str: str) -> float:
    try:
        parts = overs_str.split(".")
        full = int(parts[0])
        balls = int(parts[1]) if len(parts) > 1 else 0
        return full + (balls / 6)
    except (ValueError, IndexError):
        return 0.0


def get_innings_summary(data: Dict[str, Any]) -> dict:
    overs_decimal = _overs_to_decimal(data["overs"])
    run_rate = round(data["total_runs"] / overs_decimal, 2) if overs_decimal > 0 else 0.0

    return {
        "innings_id": data["innings_id"],
        "batting_team": data["batting_team"],
        "total_runs": data["total_runs"],
        "wickets": data["wickets"],
        "overs": data["overs"],
        "run_rate": run_rate,
        "top_batter": data["top_batter"],
        "top_bowler": data["top_bowler"],
        "recent_balls": data["recent_balls"],
    }

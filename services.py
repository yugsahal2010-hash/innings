from typing import Optional

MOCK_BALL_EVENTS = [
    {"striker": "Virat Kohli", "bowler": "Shaheen Afridi", "runs_off_bat": 0, "extras": 1, "extra_type": "wide", "is_legal_delivery": False, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Virat Kohli", "bowler": "Shaheen Afridi", "runs_off_bat": 4, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Virat Kohli", "bowler": "Shaheen Afridi", "runs_off_bat": 0, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": True, "wicket_type": "bowled"},
    {"striker": "Rohit Sharma", "bowler": "Shaheen Afridi", "runs_off_bat": 1, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
    {"striker": "Rohit Sharma", "bowler": "Naseem Shah", "runs_off_bat": 6, "extras": 0, "extra_type": "", "is_legal_delivery": True, "wicket_fell": False, "wicket_type": ""},
]

def format_overs(legal_balls: int) -> str:
    return f"{legal_balls // 6}.{legal_balls % 6}"

def get_innings_summary(innings_id: int) -> Optional[dict]:
    if innings_id != 1: return None
    
    events = MOCK_BALL_EVENTS
    total_runs = sum(e["runs_off_bat"] + e["extras"] for e in events)
    wickets = sum(1 for e in events if e["wicket_fell"] and e["wicket_type"] not in {"run_out", "retired_out"})
    legal_balls = sum(1 for e in events if e["is_legal_delivery"])
    
    # Batting Analytics
    batter_map = {}
    for e in events:
        s = e["striker"]
        if s not in batter_map: batter_map[s] = {"name": s, "runs": 0, "balls": 0, "fours": 0, "sixes": 0}
        batter_map[s]["runs"] += e["runs_off_bat"]
        if e["is_legal_delivery"]: batter_map[s]["balls"] += 1
        if e["runs_off_bat"] == 4: batter_map[s]["fours"] += 1
        if e["runs_off_bat"] == 6: batter_map[s]["sixes"] += 1

    batters_list = []
    for b in batter_map.values():
        sr = round((b["runs"] / b["balls"]) * 100, 2) if b["balls"] > 0 else 0.0
        batters_list.append({**b, "strike_rate": sr})

    # Bowling Analytics
    bowler_map = {}
    for e in events:
        b = e["bowler"]
        if b not in bowler_map: bowler_map[b] = {"name": b, "runs": 0, "legal_balls": 0, "wickets": 0}
        bowler_map[b]["runs"] += (e["runs_off_bat"] + (e["extras"] if e["extra_type"] in ["wide", "no_ball"] else 0))
        if e["is_legal_delivery"]: bowler_map[b]["legal_balls"] += 1
        if e["wicket_fell"] and e["wicket_type"] not in {"run_out", "retired_out"}: bowler_map[b]["wickets"] += 1

    bowlers_list = []
    for bw in bowler_map.values():
        econ = round(bw["runs"] / (bw["legal_balls"] / 6), 2) if bw["legal_balls"] > 0 else 0.0
        bowlers_list.append({"name": bw["name"], "overs": format_overs(bw["legal_balls"]), "runs": bw["runs"], "wickets": bw["wickets"], "economy": econ})

    rr = round(total_runs / (legal_balls / 6), 2) if legal_balls > 0 else 0.0
    
    return {
        "innings_id": innings_id,
        "batting_team": "India",
        "bowling_team": "Pakistan",
        "total_runs": total_runs,
        "wickets": wickets,
        "legal_balls": legal_balls,
        "overs": format_overs(legal_balls),
        "run_rate": rr,
        "batters": batters_list,
        "bowlers": bowlers_list,
        "top_batter": max(batters_list, key=lambda x: x["runs"])["name"] if batters_list else "N/A",
        "top_bowler": max(bowlers_list, key=lambda x: x["wickets"])["name"] if bowlers_list else "N/A",
        "recent_balls": [str(e["runs_off_bat"]) if not e["wicket_fell"] else "W" for e in events[-6:]]
    }
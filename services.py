rom typing import Dict, Any, Optional


def get_innings_summary(data: Dict[str, Any]) -> dict:
    events = data["ball_events"]

    # --- Batter Stats ---
    b_map = {}
    for e in events:
        name = e["striker"]
        if name not in b_map:
            b_map[name] = {"runs": 0, "balls": 0, "4s": 0, "6s": 0}
        b_map[name]["runs"] += e["runs_off_bat"]
        b_map[name]["balls"] += 1
        if e["runs_off_bat"] == 4: b_map[name]["4s"] += 1
        if e["runs_off_bat"] == 6: b_map[name]["6s"] += 1

    top_batter = None
    if b_map:
        tb_name = max(b_map, key=lambda x: b_map[x]["runs"])
        tb = b_map[tb_name]
        sr = round((tb["runs"] / tb["balls"]) * 100, 2) if tb["balls"] > 0 else 0.0
        top_batter = {"name": tb_name, "runs": tb["runs"], "balls": tb["balls"],
                      "fours": tb["4s"], "sixes": tb["6s"], "strike_rate": sr}

    # --- Bowler Stats ---
    bw_map = {}
    for e in events:
        name = e["bowler"]
        if name not in bw_map:
            bw_map[name] = {"runs": 0, "balls": 0, "wickets": 0}
        bw_map[name]["runs"] += (e["runs_off_bat"] + e["extras"])
        bw_map[name]["balls"] += 1
        if e["wicket_fell"]: bw_map[name]["wickets"] += 1

    top_bowler = None
    if bw_map:
        tb_name = max(bw_map, key=lambda x: bw_map[x]["wickets"])
        bw = bw_map[tb_name]
        econ = round(bw["runs"] / (bw["balls"] / 6), 2) if bw["balls"] > 0 else 0.0
        top_bowler = {"name": tb_name, "overs": f"{bw['balls']//6}.{bw['balls']%6}",
                      "runs": bw["runs"], "wickets": bw["wickets"], "economy": econ}

    # --- Totals ---
    total_r = sum(e["runs_off_bat"] + e["extras"] for e in events)
    total_w = sum(1 for e in events if e["wicket_fell"])
    legal_balls = sum(1 for e in events if e["is_legal_delivery"])
    overs_str = f"{legal_balls // 6}.{legal_balls % 6}"
    overs_decimal = (legal_balls // 6) + (legal_balls % 6) / 6
    run_rate = round(total_r / overs_decimal, 2) if overs_decimal > 0 else 0.0

    recent_balls = [str(e["runs_off_bat"]) if not e["wicket_fell"] else "W" for e in events[-6:]]

    return {
        "innings_id": data["innings_id"],
        "batting_team": data["batting_team"],
        "total_runs": total_r,
        "wickets": total_w,
        "overs": overs_str,
        "run_rate": run_rate,
        "top_batter": top_batter,
        "top_bowler": top_bowler,
        "recent_balls": recent_balls,
    }

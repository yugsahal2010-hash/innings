from typing import Optional

def generate_full_20_overs():
    events = []
    batters = ["Virat Kohli", "Rohit Sharma", "Suryakumar Yadav", "Hardik Pandya", "Rishabh Pant"]
    bowlers = ["Shaheen Afridi", "Naseem Shah", "Haris Rauf", "Shadab Khan"]
    curr_s, curr_ns = 0, 1
    
    for over in range(20):
        bowler_name = bowlers[over % len(bowlers)]
        for ball in range(1, 7):
            runs = [0, 1, 0, 4, 1, 6][(over + ball) % 6]
            is_wkt = True if (over > 18 and ball == 6) else False
            events.append({
                "striker": batters[curr_s % len(batters)],
                "bowler": bowler_name,
                "runs_off_bat": runs,
                "extras": 0,
                "extra_type": "",
                "is_legal_delivery": True,
                "wicket_fell": is_wkt,
                "wicket_type": "caught" if is_wkt else ""
            })
            if is_wkt: curr_s += 1
            elif runs % 2 != 0: curr_s, curr_ns = curr_ns, curr_s
    return events

# Pre-load the data
FULL_DATA = generate_full_20_overs()

def get_innings_summary(innings_id: int) -> Optional[dict]:
    if innings_id != 1: return None
    events = FULL_DATA
    
    # --- 1. Calculate Batter Stats ---
    b_map = {}
    for e in events:
        name = e["striker"]
        if name not in b_map:
            b_map[name] = {"runs": 0, "balls": 0, "4s": 0, "6s": 0}
        b_map[name]["runs"] += e["runs_off_bat"]
        b_map[name]["balls"] += 1
        if e["runs_off_bat"] == 4: b_map[name]["4s"] += 1
        if e["runs_off_bat"] == 6: b_map[name]["6s"] += 1

    batters_list = []
    for name, stat in b_map.items():
        sr = round((stat["runs"] / stat["balls"]) * 100, 2) if stat["balls"] > 0 else 0.0
        batters_list.append({
            "name": name, "runs": stat["runs"], "balls": stat["balls"],
            "fours": stat["4s"], "sixes": stat["6s"], "strike_rate": sr
        })

    # --- 2. Calculate Bowler Stats ---
    bw_map = {}
    for e in events:
        name = e["bowler"]
        if name not in bw_map:
            bw_map[name] = {"runs": 0, "balls": 0, "wickets": 0}
        bw_map[name]["runs"] += (e["runs_off_bat"] + e["extras"])
        bw_map[name]["balls"] += 1
        if e["wicket_fell"]: bw_map[name]["wickets"] += 1

    bowlers_list = []
    for name, stat in bw_map.items():
        econ = round(stat["runs"] / (stat["balls"] / 6), 2) if stat["balls"] > 0 else 0.0
        bowlers_list.append({
            "name": name, "overs": f"{stat['balls']//6}.{stat['balls']%6}",
            "runs": stat["runs"], "wickets": stat["wickets"], "economy": econ
        })

    # --- 3. Calculate Over-by-Over ---
    over_by_over = []
    temp_events = []
    o_num = 1
    for e in events:
        temp_events.append(e)
        if len(temp_events) == 6:
            over_by_over.append({
                "over_number": o_num,
                "bowler": temp_events[0]["bowler"],
                "runs": sum(x["runs_off_bat"] + x["extras"] for x in temp_events),
                "wickets": sum(1 for x in temp_events if x["wicket_fell"]),
                "ball_labels": [str(x["runs_off_bat"]) if not x["wicket_fell"] else "W" for x in temp_events]
            })
            temp_events, o_num = [], o_num + 1

    # --- 4. Final Verification and Return ---
    # Total calculations
    total_r = sum(e["runs_off_bat"] + e["extras"] for e in events)
    total_w = sum(1 for e in events if e["wicket_fell"])

    return {
        "innings_id": innings_id,
        "batting_team": "India",
        "total_runs": total_r,
        "wickets": total_w,
        "overs": "20.0",
        "batters": batters_list,
        "bowlers": bowlers_list,
        "over_by_over": over_by_over,
        "recent_balls": [str(e["runs_off_bat"]) if not e["wicket_fell"] else "W" for e in events[-6:]]
    }
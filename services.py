from typing import Optional

# --- Generation Logic for a Full 20 Over Demo ---
def generate_full_20_overs():
    events = []
    batters = ["Virat Kohli", "Rohit Sharma", "Suryakumar Yadav", "Hardik Pandya", "Rishabh Pant"]
    bowlers = ["Shaheen Afridi", "Naseem Shah", "Haris Rauf", "Shadab Khan"]
    
    current_striker_idx = 0
    current_non_striker_idx = 1
    
    for over in range(20):
        bowler = bowlers[over % len(bowlers)]
        for ball in range(1, 7):
            # Simulate realistic runs (0s, 1s, 4s, 6s)
            runs = [0, 0, 1, 1, 2, 4, 6][(over + ball) % 7]
            is_wicket = True if (over > 15 and ball == 6) else False # Wickets in death overs
            
            striker = batters[current_striker_idx % len(batters)]
            non_striker = batters[current_non_striker_idx % len(batters)]
            
            event = {
                "striker": striker,
                "non_striker": non_striker,
                "bowler": bowler,
                "runs_off_bat": runs,
                "extras": 0,
                "extra_type": "",
                "is_legal_delivery": True,
                "wicket_fell": is_wicket,
                "wicket_type": "caught" if is_wicket else ""
            }
            events.append(event)
            
            if is_wicket:
                current_striker_idx += 1 # Next batter comes in
            elif runs % 2 != 0:
                current_striker_idx, current_non_striker_idx = current_non_striker_idx, current_striker_idx
                
    return events

FULL_20_OVER_DATA = generate_full_20_overs()

# --- Calculation Logic ---

def get_innings_summary(innings_id: int) -> Optional[dict]:
    if innings_id != 1: return None
    events = FULL_20_OVER_DATA
    
    total_runs = sum(e["runs_off_bat"] + e["extras"] for e in events)
    total_wickets = sum(1 for e in events if e["wicket_fell"])
    legal_balls = sum(1 for e in events if e["is_legal_delivery"])
    
    # Player Analytics
    batter_stats = {}
    bowler_stats = {}

    for e in events:
        # Batter Math
        s = e["striker"]
        if s not in batter_stats:
            batter_stats[s] = {"name": s, "runs": 0, "balls": 0, "dots": 0, "4s": 0, "6s": 0}
        
        batter_stats[s]["runs"] += e["runs_off_bat"]
        if e["is_legal_delivery"]: batter_stats[s]["balls"] += 1
        if e["runs_off_bat"] == 0 and e["extra_type"] == "": batter_stats[s]["dots"] += 1
        if e["runs_off_bat"] == 4: batter_stats[s]["4s"] += 1
        if e["runs_off_bat"] == 6: batter_stats[s]["6s"] += 1

        # Bowler Math
        b = e["bowler"]
        if b not in bowler_stats:
            bowler_stats[b] = {"name": b, "runs": 0, "balls": 0, "wickets": 0, "dots": 0}
        
        bowler_stats[b]["runs"] += (e["runs_off_bat"] + e["extras"])
        if e["is_legal_delivery"]: bowler_stats[b]["balls"] += 1
        if e["runs_off_bat"] == 0 and e["extras"] == 0: bowler_stats[b]["dots"] += 1
        if e["wicket_fell"]: bowler_stats[b]["wickets"] += 1

    # Formatting Lists
    final_batters = [
        {
            "name": k, "runs": v["runs"], "balls": v["balls"], "dot_balls": v["dots"],
            "fours": v["4s"], "sixes": v["6s"],
            "strike_rate": round((v["runs"]/v["balls"])*100, 2) if v["balls"] > 0 else 0
        } for k, v in batter_stats.items()
    ]

    final_bowlers = [
        {
            "name": k, "overs": f"{v['balls']//6}.{v['balls']%6}", "runs": v["runs"],
            "wickets": v["wickets"], "dot_balls": v["dots"],
            "economy": round(v["runs"]/(v["balls"]/6), 2) if v["balls"] > 0 else 0
        } for k, v in bowler_stats.items()
    ]

    return {
        "innings_id": innings_id,
        "batting_team": "India",
        "total_runs": total_runs,
        "wickets": total_wickets,
        "overs": f"{legal_balls // 6}.{legal_balls % 6}",
        "run_rate": round(total_runs / (legal_balls / 6), 2),
        "batters": final_batters,
        "bowlers": final_bowlers,
        "recent_balls": [str(e["runs_off_bat"]) if not e["wicket_fell"] else "W" for e in events[-6:]]
    }
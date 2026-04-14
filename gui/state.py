import os
from config import DEFAULT_PROFILE, PROFILES_DIR

state = {
    "running":         False,
    "connected":       False,
    "profile":         DEFAULT_PROFILE,
    "mode":            "virtual",
    "pressed":         set(),
    "logs":            [],
    "last_log":        None,
    "mapper":          None,
    "router":          None,
    "axis_lx":         0.0,
    "axis_ly":         0.0,
    "axis_rx":         0.0,
    "axis_ry":         0.0,
    "trigger_l":       0.0,
    "trigger_r":       0.0,
    "input_count":     0,
    "latency_ms":      0.0,
    "controller_name": "---",
}

def get_profiles():
    return [f[:-5] for f in os.listdir(PROFILES_DIR) if f.endswith(".json")]

def add_log(msg, level="INFO"):
    if state["last_log"] == (level, msg):
        return
    state["last_log"] = (level, msg)
    from gui.theme import C_CYAN, C_GREEN, C_PINK, C_ORANGE, C_TEXT
    colors = {"INFO":C_CYAN,"ACTION":C_GREEN,"ERROR":C_PINK,"WARN":C_ORANGE}
    state["logs"].append((level, msg, colors.get(level, C_TEXT)))
    if len(state["logs"]) > 100:
        state["logs"].pop(0)

import dearpygui.dearpygui as dpg
import math
from gui.theme import BTN_COLORS, C_CYAN, C_MUTED, C_GREEN, C_ORANGE, C_TEXT, C_BG2, C_BG3, C_BORDER, C_PINK, C_PURPLE
from gui.state import state

BUTTONS = ["SOUTH","EAST","WEST","NORTH","L1","R1","L2","R2","SELECT","START"]
JOY_SIZE = 100
JOY_R    = 42
JOY_DOT  = 8

def build():
    with dpg.child_window(width=280, height=840, border=True):
        # Header
        _section("MANETTE")
        dpg.add_text("---", tag="ctrl_name", color=C_MUTED)
        dpg.add_spacer(height=10)

        # Face buttons - layout en croix
        _section("FACE")
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_button(label="TRI", tag="btn_NORTH", width=42, height=36)
        dpg.add_spacer(height=2)
        with dpg.group(horizontal=True):
            dpg.add_button(label="CAR", tag="btn_WEST", width=42, height=36)
            dpg.add_spacer(width=50)
            dpg.add_button(label="RON", tag="btn_EAST", width=42, height=36)
        dpg.add_spacer(height=2)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_button(label="CRX", tag="btn_SOUTH", width=42, height=36)

        dpg.add_spacer(height=10)

        # Bumpers
        _section("BUMPERS / TRIGGERS")
        with dpg.group(horizontal=True):
            dpg.add_button(label="L1", tag="btn_L1", width=80, height=26)
            dpg.add_spacer(width=4)
            dpg.add_button(label="R1", tag="btn_R1", width=80, height=26)
        dpg.add_spacer(height=6)

        # Triggers avec barres
        with dpg.group(horizontal=True):
            dpg.add_text("L2", color=C_ORANGE)
            dpg.add_spacer(width=4)
            dpg.add_button(label="  ", tag="btn_L2", width=30, height=16)
        dpg.add_progress_bar(tag="bar_L2", default_value=0.0,
                              width=170, height=10)
        dpg.add_spacer(height=4)
        with dpg.group(horizontal=True):
            dpg.add_text("R2", color=C_ORANGE)
            dpg.add_spacer(width=4)
            dpg.add_button(label="  ", tag="btn_R2", width=30, height=16)
        dpg.add_progress_bar(tag="bar_R2", default_value=0.0,
                              width=170, height=10)

        dpg.add_spacer(height=10)

        # Joysticks graphiques
        _section("JOYSTICKS")
        cx, cy = JOY_SIZE//2, JOY_SIZE//2
        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("L", color=C_MUTED)
                with dpg.drawlist(width=JOY_SIZE, height=JOY_SIZE):
                    # Fond
                    dpg.draw_circle((cx,cy), JOY_R,
                        color=(35,55,110,255), fill=(12,19,45,255))
                    # Cercle deadzone
                    dpg.draw_circle((cx,cy), int(JOY_R*0.2),
                        color=(50,80,150,100))
                    # Croix guide
                    dpg.draw_line((cx-JOY_R,cy),(cx+JOY_R,cy),
                        color=(35,55,110,160))
                    dpg.draw_line((cx,cy-JOY_R),(cx,cy+JOY_R),
                        color=(35,55,110,160))
                    # Point
                    dpg.draw_circle((cx,cy), JOY_DOT,
                        color=(0,200,255,255), fill=(0,200,255,220),
                        tag="joy_L_dot")
            dpg.add_spacer(width=6)
            with dpg.group():
                dpg.add_text("R", color=C_MUTED)
                with dpg.drawlist(width=JOY_SIZE, height=JOY_SIZE):
                    dpg.draw_circle((cx,cy), JOY_R,
                        color=(35,55,110,255), fill=(12,19,45,255))
                    dpg.draw_circle((cx,cy), int(JOY_R*0.2),
                        color=(50,80,150,100))
                    dpg.draw_line((cx-JOY_R,cy),(cx+JOY_R,cy),
                        color=(35,55,110,160))
                    dpg.draw_line((cx,cy-JOY_R),(cx,cy+JOY_R),
                        color=(35,55,110,160))
                    dpg.draw_circle((cx,cy), JOY_DOT,
                        color=(180,120,255,255), fill=(180,120,255,220),
                        tag="joy_R_dot")

        dpg.add_spacer(height=10)

        # Systeme
        _section("SYSTEME")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Share",   tag="btn_SELECT", width=80, height=24)
            dpg.add_spacer(width=4)
            dpg.add_button(label="Options", tag="btn_START",  width=80, height=24)

        dpg.add_spacer(height=10)

        # Stats
        _section("STATS")
        with dpg.table(header_row=False, borders_innerV=False,
                       borders_outerH=False, borders_outerV=False):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=80)
            dpg.add_table_column()
            with dpg.table_row():
                dpg.add_text("Inputs",   color=C_MUTED)
                dpg.add_text("0", tag="stat_inputs", color=C_TEXT)
            with dpg.table_row():
                dpg.add_text("Latence",  color=C_MUTED)
                dpg.add_text("---", tag="stat_latency", color=C_TEXT)

    _apply_btn_themes()

def _section(label):
    dpg.add_text(label, color=(0,200,255,180))
    dpg.add_separator()
    dpg.add_spacer(height=4)

def _apply_btn_themes():
    from gui.theme import get_btn_theme
    for btn in BUTTONS:
        if dpg.does_item_exist(f"btn_{btn}"):
            t = get_btn_theme(btn, False)
            if t: dpg.bind_item_theme(f"btn_{btn}", t)

def update():
    from gui.theme import get_btn_theme
    for btn in BUTTONS:
        if dpg.does_item_exist(f"btn_{btn}"):
            t = get_btn_theme(btn, btn in state["pressed"])
            if t: dpg.bind_item_theme(f"btn_{btn}", t)

    _move_dot("joy_L_dot", state["axis_lx"], state["axis_ly"],
              (0,200,255,255), (0,200,255,220))
    _move_dot("joy_R_dot", state["axis_rx"], state["axis_ry"],
              (180,120,255,255), (180,120,255,220))

    dpg.set_value("bar_L2", max(0.0, min(1.0, state["trigger_l"])))
    dpg.set_value("bar_R2", max(0.0, min(1.0, state["trigger_r"])))
    dpg.set_value("ctrl_name", state["controller_name"])
    dpg.set_value("stat_inputs",  str(state["input_count"]))
    lat = state["latency_ms"]
    dpg.set_value("stat_latency", f"{lat:.1f}ms" if lat > 0 else "---")

def _move_dot(tag, vx, vy, col, fill):
    cx, cy = JOY_SIZE//2, JOY_SIZE//2
    l = math.sqrt(vx**2 + vy**2)
    if l > 1.0: vx, vy = vx/l, vy/l
    px = int(cx + vx*(JOY_R - JOY_DOT - 3))
    py = int(cy + vy*(JOY_R - JOY_DOT - 3))
    if dpg.does_item_exist(tag):
        dpg.configure_item(tag, center=(px,py), color=col, fill=fill)

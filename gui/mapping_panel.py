import dearpygui.dearpygui as dpg
import json, os
from gui.theme import BTN_COLORS, C_CYAN, C_MUTED, C_TEXT, C_ORANGE, C_BG3
from gui.state import state

def build():
    with dpg.child_window(width=600, height=840, border=True):
        _section("MAPPING BOUTONS")
        with dpg.table(tag="mapping_table", header_row=True,
                       borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True,
                       row_background=True, scrollY=True,
                       height=260):
            dpg.add_table_column(label="Bouton", width_fixed=True,
                                 init_width_or_weight=80)
            dpg.add_table_column(label="Type",   width_fixed=True,
                                 init_width_or_weight=60)
            dpg.add_table_column(label="Action")
        refresh_buttons()

        dpg.add_spacer(height=14)
        _section("AXES ANALOGIQUES")
        with dpg.table(tag="axes_table", header_row=True,
                       borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True,
                       row_background=True, scrollY=True,
                       height=200):
            dpg.add_table_column(label="Axe",  width_fixed=True,
                                 init_width_or_weight=90)
            dpg.add_table_column(label="Type", width_fixed=True,
                                 init_width_or_weight=90)
            dpg.add_table_column(label="Config")
        refresh_axes()

        dpg.add_spacer(height=14)
        _section("PROFIL ACTIF")
        from gui.state import get_profiles
        dpg.add_combo(get_profiles(), default_value=state["profile"],
                      tag="profile_combo", width=580,
                      callback=_on_profile)

        dpg.add_spacer(height=10)
        _section("MODE DE SORTIE")
        dpg.add_radio_button(
            ["Manette virtuelle", "Clavier / souris"],
            tag="mode_radio",
            default_value="Manette virtuelle",
            horizontal=True,
            callback=_on_mode,
        )

        dpg.add_spacer(height=14)
        dpg.add_button(label="  DEMARRER  ", tag="start_btn",
                       width=580, height=42, callback=_on_start)
        from gui.theme import get_start_theme
        t = get_start_theme(False)
        if t: dpg.bind_item_theme("start_btn", t)

def _section(label):
    dpg.add_text(label, color=(0,200,255,180))
    dpg.add_separator()
    dpg.add_spacer(height=4)

def _load_profile():
    from config import PROFILES_DIR
    path = os.path.join(PROFILES_DIR, f"{state['profile']}.json")
    try:
        with open(path) as f: return json.load(f)
    except: return {}

def refresh_buttons():
    for c in (dpg.get_item_children("mapping_table", slot=1) or []):
        dpg.delete_item(c)
    for btn, action in _load_profile().get("buttons", {}).items():
        with dpg.table_row(parent="mapping_table"):
            dpg.add_text(btn,                     color=BTN_COLORS.get(btn, C_TEXT))
            dpg.add_text(action.get("type",  ""), color=C_MUTED)
            dpg.add_text(action.get("value", ""), color=C_TEXT)

def refresh_axes():
    for c in (dpg.get_item_children("axes_table", slot=1) or []):
        dpg.delete_item(c)
    for axis, action in _load_profile().get("axes", {}).items():
        t = action.get("type", "")
        cfg = (f"{action.get('neg')} / {action.get('pos')}"
               if t == "key_pair" else
               f"souris {action.get('axis')} x{action.get('sensitivity')}"
               if t == "mouse_move" else "")
        with dpg.table_row(parent="axes_table"):
            dpg.add_text(axis, color=C_CYAN)
            dpg.add_text(t,    color=C_MUTED)
            dpg.add_text(cfg,  color=C_TEXT)

def refresh_all():
    refresh_buttons()
    refresh_axes()

def _on_profile(s, v):
    state["profile"]  = v
    state["last_log"] = None
    if state["mapper"]:
        from config import PROFILES_DIR
        state["mapper"].reload(os.path.join(PROFILES_DIR, f"{v}.json"))
    refresh_all()
    from gui.state import add_log
    add_log(f"Profil : {v}", "INFO")

def _on_mode(s, v):
    mode = "virtual" if v == "Manette virtuelle" else "keyboard"
    state["mode"]     = mode
    state["last_log"] = None
    if state["router"]: state["router"].set_mode(mode)
    from gui.state import add_log
    add_log(f"Mode : {mode}", "INFO")

def _on_start(s, v):
    from gui.theme import get_start_theme
    from gui.state import add_log
    import gui.engine_thread as engine
    if not state["running"]:
        engine.start(state["profile"], state["mode"])
        dpg.set_item_label("start_btn", "  ARRETER  ")
        t = get_start_theme(True)
        if t: dpg.bind_item_theme("start_btn", t)
        add_log("Moteur demarre", "INFO")
    else:
        state["running"]  = False
        state["connected"]= False
        dpg.set_item_label("start_btn", "  DEMARRER  ")
        t = get_start_theme(False)
        if t: dpg.bind_item_theme("start_btn", t)
        add_log("Moteur arrete", "WARN")

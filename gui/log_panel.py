import dearpygui.dearpygui as dpg
from gui.theme import C_CYAN, C_MUTED, C_BG2
from gui.state import state

_last_shown = None

def build():
    with dpg.child_window(width=660, height=840, border=True):
        dpg.add_text("TERMINAL", color=(0,200,255,180))
        dpg.add_separator()
        dpg.add_spacer(height=4)
        with dpg.child_window(tag="log_window", height=790,
                              border=False, horizontal_scrollbar=False):
            dpg.add_text("En attente...", color=C_MUTED, tag="log_placeholder")

def update():
    global _last_shown
    if not state["logs"]: return
    last = state["logs"][-1]
    if last == _last_shown: return
    _last_shown = last
    if dpg.does_item_exist("log_placeholder"):
        dpg.delete_item("log_placeholder")
    children = dpg.get_item_children("log_window", slot=1)
    if children and len(children) > 60:
        dpg.delete_item(children[0])
    level, msg, color = last
    dpg.add_text(f"[{level}] {msg}", color=color, parent="log_window")
    state["logs"].clear()

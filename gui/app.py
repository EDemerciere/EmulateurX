import dearpygui.dearpygui as dpg
from gui.theme          import apply_global_theme, C_GREEN, C_PINK, C_MUTED, C_TEXT, C_CYAN
from gui.state          import state
from gui.controller_view import build as build_ctrl, update as update_ctrl
from gui.mapping_panel   import build as build_map
from gui.log_panel       import build as build_log, update as update_log

def main():
    dpg.create_context()
    dpg.create_viewport(
        title="CtrlRemap - NSI",
        width=1600, height=920,
        min_width=1600, min_height=920,
    )
    dpg.setup_dearpygui()
    apply_global_theme()
    _build_ui()
    dpg.set_primary_window("main_window", True)
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        _update_ui()
        dpg.render_dearpygui_frame()
    state["running"] = False
    if state["router"]: state["router"].reset()
    dpg.destroy_context()

def _build_ui():
    with dpg.window(tag="main_window", no_title_bar=True,
                    no_move=True, no_resize=True, no_scrollbar=True):

        # ── Topbar ──────────────────────────────────────────────────────
        with dpg.group(horizontal=True):
            dpg.add_text("CTRL",          color=C_TEXT)
            dpg.add_text("REMAP",         color=C_GREEN)
            dpg.add_text(" | NSI Terminale | Controller Remapper Universel",
                         color=C_MUTED)
            dpg.add_spacer(width=20)
            dpg.add_text("*", tag="status_dot",  color=C_PINK)
            dpg.add_text("Deconnectee",   tag="status_text", color=C_MUTED)
        dpg.add_separator()
        dpg.add_spacer(height=8)

        # ── 3 colonnes ──────────────────────────────────────────────────
        with dpg.group(horizontal=True):
            build_ctrl()
            dpg.add_spacer(width=6)
            build_map()
            dpg.add_spacer(width=6)
            build_log()

def _update_ui():
    if state["connected"]:
        dpg.set_value("status_dot",  "*")
        dpg.configure_item("status_dot",  color=C_GREEN)
        dpg.set_value("status_text", "Connectee")
        dpg.configure_item("status_text", color=C_GREEN)
    else:
        dpg.set_value("status_dot",  "*")
        dpg.configure_item("status_dot",  color=C_PINK)
        dpg.set_value("status_text", "Deconnectee")
        dpg.configure_item("status_text", color=C_MUTED)
    update_ctrl()
    update_log()

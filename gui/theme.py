import dearpygui.dearpygui as dpg

# Palette bleu nuit + neon
C_BG      = (8,   13,  35)
C_BG2     = (12,  19,  45)
C_BG3     = (18,  27,  60)
C_BG4     = (24,  36,  75)
C_BORDER  = (35,  55, 110)
C_BORDER2 = (50,  80, 150)
C_GREEN   = (0,   255, 130)
C_CYAN    = (0,   200, 255)
C_PURPLE  = (180, 120, 255)
C_ORANGE  = (255, 145,  50)
C_PINK    = (255,  55, 140)
C_MUTED   = (85,  110, 165)
C_TEXT    = (215, 228, 255)
C_DIM     = (50,   65, 100)

BTN_COLORS = {
    "SOUTH": C_GREEN,  "EAST":   C_PINK,
    "WEST":  C_CYAN,   "NORTH":  C_PURPLE,
    "L1":    C_MUTED,  "R1":     C_MUTED,
    "L2":    C_ORANGE, "R2":     C_ORANGE,
    "SELECT":C_DIM,    "START":  C_DIM,
}

_btn_themes   = {}
_start_themes = {}

def apply_global_theme():
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,        C_BG)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,         C_BG2)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,         C_BG3)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,  C_BG4)
            dpg.add_theme_color(dpg.mvThemeCol_Button,          C_BG3)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,   C_BG4)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,    C_BORDER2)
            dpg.add_theme_color(dpg.mvThemeCol_Header,          C_BG3)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,   C_BG4)
            dpg.add_theme_color(dpg.mvThemeCol_Text,            C_TEXT)
            dpg.add_theme_color(dpg.mvThemeCol_Border,          C_BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg,         C_BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,   C_BG3)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg,         C_BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,   C_BG3)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg,      C_BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt,   C_BG3)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, C_BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, C_BORDER2)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,     C_BG)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,   C_BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,       C_GREEN)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab,      C_CYAN)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding,   0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,    4)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,    4)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,      8, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,   12, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,     8,  5)
            dpg.add_theme_style(dpg.mvStyleVar_IndentSpacing,   12)
    dpg.bind_theme(t)
    _build_btn_themes()
    _build_start_themes()

def _build_btn_themes():
    for btn, color in BTN_COLORS.items():
        dim = tuple(int(c * 0.18) for c in color)
        glow = tuple(min(255, int(c * 1.1)) for c in color)
        for pressed in (False, True):
            with dpg.theme() as t:
                with dpg.theme_component(dpg.mvButton):
                    dpg.add_theme_color(dpg.mvThemeCol_Button,
                        glow if pressed else dim)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                        glow)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                        color)
                    dpg.add_theme_color(dpg.mvThemeCol_Text,
                        (5, 5, 15) if pressed else color)
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            _btn_themes[(btn, pressed)] = t

def _build_start_themes():
    configs = {
        "start": ((0, 50, 25),    (0, 90, 45),   C_GREEN),
        "stop":  ((50, 10, 20),   (90, 18, 35),  C_PINK),
    }
    for key, (bg, hov, txt) in configs.items():
        with dpg.theme() as t:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button,        bg)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hov)
                dpg.add_theme_color(dpg.mvThemeCol_Text,          txt)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
        _start_themes[key] = t

def get_btn_theme(btn, pressed):
    return _btn_themes.get((btn, bool(pressed)))

def get_start_theme(running):
    return _start_themes.get("stop" if running else "start")

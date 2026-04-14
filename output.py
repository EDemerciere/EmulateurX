# output.py — simulation clavier/souris via pynput
# Utilisé en mode "keyboard" par OutputRouter.
# Sur Windows : API SendInput. Sur Linux : XTest. Sur macOS : Accessibility API.

from pynput.keyboard import Controller as KB, Key
from pynput.mouse    import Controller as Mouse, Button
import pygame

kb    = KB()
mouse = Mouse()

KEY_MAP = {
    "space":     Key.space,
    "shift":     Key.shift,
    "ctrl":      Key.ctrl,
    "alt":       Key.alt,
    "tab":       Key.tab,
    "escape":    Key.esc,
    "enter":     Key.enter,
    "backspace": Key.backspace,
    "up":        Key.up,
    "down":      Key.down,
    "left":      Key.left,
    "right":     Key.right,
    "f1": Key.f1, "f2": Key.f2, "f3": Key.f3,
    "f4": Key.f4, "f5": Key.f5, "f6": Key.f6,
}

class Output:
    def execute(self, action: dict, event_type: int):
        """Simule un bouton numérique (press ou release)."""
        pressed = (event_type == pygame.JOYBUTTONDOWN)
        t = action.get("type")
        v = action.get("value")

        if t == "key":
            key = KEY_MAP.get(v, v)
            kb.press(key) if pressed else kb.release(key)

        elif t == "mouse":
            btn = Button.left if v == "left" else Button.right
            mouse.press(btn) if pressed else mouse.release(btn)

    def execute_axis(self, axis_name: str, action: dict, value: float):
        """Simule un axe analogique (key_pair ou mouse_move)."""
        t = action.get("type")

        if t == "key_pair":
            neg = action.get("neg")
            pos = action.get("pos")
            thr = action.get("threshold", 0.5)
            if value < -thr:
                kb.press(neg);   kb.release(pos)
            elif value > thr:
                kb.press(pos);   kb.release(neg)
            else:
                kb.release(neg); kb.release(pos)

        elif t == "mouse_move":
            sens  = action.get("sensitivity", 8)
            axis  = action.get("axis", "x")
            delta = int(value * sens)
            dx = delta if axis == "x" else 0
            dy = delta if axis == "y" else 0
            mouse.move(dx, dy)

# core/virtual_controller.py — manette Xbox 360 virtuelle via ViGEmBus
# Crée une vraie manette reconnue nativement par les jeux XInput.
# Prérequis : pip install vgamepad + driver ViGEmBus installé sur Windows.

import vgamepad as vg

class VirtualController:
    def __init__(self):
        self.pad = vg.VX360Gamepad()
        print("Manette virtuelle Xbox 360 créée.")

    def press(self, button_name: str):
        """Appuie sur un bouton de la manette virtuelle."""
        btn = self._map(button_name)
        if btn:
            self.pad.press_button(button=btn)
            self.pad.update()   # obligatoire — envoie l'état au driver

    def release(self, button_name: str):
        """Relâche un bouton de la manette virtuelle."""
        btn = self._map(button_name)
        if btn:
            self.pad.release_button(button=btn)
            self.pad.update()

    def move_axis(self, axis_name: str, value: float):
        """
        Déplace un axe analogique.
        value : float entre -1.0 et +1.0 → int entre -32767 et +32767
        """
        v = int(value * 32767)
        if   axis_name == "AXIS_LX": self.pad.left_joystick(x_value=v, y_value=0)
        elif axis_name == "AXIS_LY": self.pad.left_joystick(x_value=0, y_value=v)
        elif axis_name == "AXIS_RX": self.pad.right_joystick(x_value=v, y_value=0)
        elif axis_name == "AXIS_RY": self.pad.right_joystick(x_value=0, y_value=v)
        elif axis_name == "TRIGGER_L": self.pad.left_trigger(value=int((value+1)/2*255))
        elif axis_name == "TRIGGER_R": self.pad.right_trigger(value=int((value+1)/2*255))
        self.pad.update()

    def reset(self):
        """Remet tous les boutons et axes à zéro."""
        self.pad.reset()
        self.pad.update()

    def _map(self, name: str):
        """Convertit un nom universel en constante XUSB_BUTTON."""
        return {
            "SOUTH":  vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            "EAST":   vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            "WEST":   vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            "NORTH":  vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            "L1":     vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            "R1":     vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            "SELECT": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            "START":  vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            "HOME":   vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
        }.get(name)

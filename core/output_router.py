# core/output_router.py — aiguillage clavier/souris ↔ manette virtuelle
# Design Pattern Strategy : deux backends derrière la même interface.
# set_mode() permet de basculer à chaud sans redémarrer.

import pygame
from output import Output
from core.virtual_controller import VirtualController

class OutputRouter:
    def __init__(self, mode: str = "virtual"):
        """
        mode : "virtual"  → manette Xbox 360 virtuelle (recommandé pour Sekiro)
               "keyboard" → simulation clavier/souris classique
        """
        self.mode   = mode
        self.kb_out = Output()
        self.vpad   = VirtualController()  # toujours créé (lazy possible si besoin)

    def execute(self, input_name: str, action: dict, event_type: int):
        """Exécute une action bouton vers le backend actif."""
        pressed = (event_type == pygame.JOYBUTTONDOWN)

        if self.mode == "virtual":
            if pressed: self.vpad.press(input_name)
            else:       self.vpad.release(input_name)
        else:
            self.kb_out.execute(action, event_type)

    def execute_axis(self, axis_name: str, action: dict, value: float):
        """Exécute une action axe vers le backend actif."""
        if self.mode == "virtual":
            self.vpad.move_axis(axis_name, value)
        else:
            self.kb_out.execute_axis(axis_name, action, value)

    def set_mode(self, mode: str):
        """Bascule entre 'virtual' et 'keyboard' à chaud."""
        self.mode = mode
        print(f"Mode : {mode}")

    def reset(self):
        """Remet la manette virtuelle à zéro (appelé à l'arrêt)."""
        self.vpad.reset()

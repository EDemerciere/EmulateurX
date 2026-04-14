# normalizer.py — abstraction hardware
# Convertit les indices bruts pygame en noms universels (SOUTH, EAST, L1...)
# Convention SOUTH/EAST/WEST/NORTH = position géographique (Unity/Steam Input).

BUTTON_MAP = {
    0:  "SOUTH",    # A Xbox  / Croix PS
    1:  "EAST",     # B Xbox  / Rond PS
    2:  "WEST",     # X Xbox  / Carré PS
    3:  "NORTH",    # Y Xbox  / Triangle PS
    4:  "L1",       # LB Xbox / L1 PS
    5:  "R1",       # RB Xbox / R1 PS
    6:  "L2",       # LT Xbox / L2 PS (numérique)
    7:  "R2",       # RT Xbox / R2 PS (numérique)
    8:  "SELECT",   # View Xbox / Share PS
    9:  "START",    # Menu Xbox / Options PS
    10: "HOME",     # Guide Xbox / PS PS
}

AXIS_MAP = {
    0: "AXIS_LX",    # Joystick gauche, horizontal
    1: "AXIS_LY",    # Joystick gauche, vertical
    2: "AXIS_RX",    # Joystick droit, horizontal
    3: "AXIS_RY",    # Joystick droit, vertical
    4: "TRIGGER_L",  # Gâchette gauche (analogique)
    5: "TRIGGER_R",  # Gâchette droite (analogique)
}

DEADZONE = 0.18  # filtre les micro-dérives hardware

def normalize(event):
    """
    Convertit un Event pygame en nom universel.
    - Bouton → str   ("SOUTH")
    - Axe    → tuple (("AXIS_LX", 0.73))
    - Autre  → None  (ignoré)
    """
    import pygame

    if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
        return BUTTON_MAP.get(event.button)

    if event.type == pygame.JOYAXISMOTION:
        name = AXIS_MAP.get(event.axis)
        val  = event.value
        if name and abs(val) > DEADZONE:
            return (name, val)

    return None

# detector.py — détection manette + reconnexion à chaud
# Seule couche qui connaît pygame. Les autres modules reçoivent des Event.

import pygame

def init_controller():
    """Initialise pygame et retourne la première manette détectée."""
    if not pygame.get_init():
        pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        raise RuntimeError("Aucune manette détectée")

    return _make_joystick()

def wait_for_controller():
    """
    Attend une manette indéfiniment.
    Utilisé pour la reconnexion à chaud ou le démarrage sans manette.
    Ignore la manette virtuelle créée par vgamepad.
    """
    from logger import log
    log.info("En attente d'une manette physique...")

    while True:
        pygame.joystick.quit()
        pygame.joystick.init()

        # Cherche une manette qui n'est pas la virtuelle
        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            joy.init()
            name = joy.get_name()
            # Ignore la manette virtuelle ViGEm
            if "ViGEm" not in name and "Virtual" not in name:
                log.info(f"Manette connectée : {name}")
                log.info(f"  Boutons : {joy.get_numbuttons()}")
                log.info(f"  Axes    : {joy.get_numaxes()}")
                return joy
            joy.quit()

        pygame.time.wait(1000)

def get_events():
    """Vide et retourne la file d'événements pygame (FIFO)."""
    pygame.event.pump()
    return pygame.event.get()

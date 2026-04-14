# main.py — v4 complète
# Pipeline : manette physique → normalisation → manette virtuelle Xbox 360
#
# Lancement : python main.py
# Prérequis  : pip install pygame pynput vgamepad customtkinter
#              + driver ViGEmBus installé

import time
import os
import pygame

from config          import DEFAULT_PROFILE, PROFILES_DIR, POLL_RATE_MS
from logger          import log
from detector        import wait_for_controller, get_events
from normalizer      import normalize
from mapper          import Mapper
from core.output_router import OutputRouter

def main():
    # Initialiser pygame AVANT de créer la manette virtuelle
    # (sinon pygame détecte la manette virtuelle comme manette physique)
    pygame.init()
    pygame.joystick.init()

    profile_path = os.path.join(PROFILES_DIR, f"{DEFAULT_PROFILE}.json")
    mapper = Mapper(profile_path)
    router = OutputRouter(mode="virtual")

    log.info("Remapper v4 actif — manette virtuelle Xbox 360")
    log.info(f"Profil : {DEFAULT_PROFILE}")
    log.info("Ctrl+C pour quitter")

    # Boucle de résilience : redémarre après chaque erreur
    while True:
        try:
            joy = wait_for_controller()

            while True:
                for ev in get_events():
                    result = normalize(ev)
                    if result is None:
                        continue

                    if isinstance(result, str):
                        name   = result
                        action = mapper.get(name)
                        router.execute(name, action or {}, ev.type)

                    elif isinstance(result, tuple):
                        name, value = result
                        action = mapper.get_axis(name)
                        if action:
                            router.execute_axis(name, action, value)

                pygame.time.wait(POLL_RATE_MS)

        except KeyboardInterrupt:
            log.info("Arrêt demandé (Ctrl+C)")
            router.reset()
            pygame.quit()
            break
        except Exception as e:
            log.error(f"Erreur : {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()

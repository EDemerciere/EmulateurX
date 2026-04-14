# config.py — configuration centralisée (single source of truth)
# Modifier ce fichier suffit — pas besoin de chercher dans tout le code.

import os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")

# Profil chargé au démarrage
DEFAULT_PROFILE = "sekiro"

# Paramètres hardware
DEADZONE          = 0.18   # seuil deadzone joystick
MOUSE_SENSITIVITY = 10     # pixels/frame pour mouse_move (mode clavier)
POLL_RATE_MS      = 8      # délai boucle principale (~120 Hz)

# Logging
# "DEBUG"   → voir tous les inputs reçus
# "INFO"    → voir les actions exécutées
# "WARNING" → silence quasi-total
LOG_LEVEL = "INFO"

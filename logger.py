# logger.py — système de logs centralisé
# Remplace les print() sauvages. 5 niveaux : DEBUG < INFO < WARNING < ERROR < CRITICAL

import logging
from config import LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    datefmt="%H:%M:%S"
)

log = logging.getLogger("remapper")

def log_input(name, value=None):
    if value is not None:
        log.debug(f"INPUT   {name:<12} = {value:+.3f}")
    else:
        log.debug(f"INPUT   {name}")

def log_action(name, action):
    log.info(f"ACTION  {name:<12} → {action.get('type')}:{action.get('value')}")

# CtrlRemap — Remappeur universel de manette

> Projet NSI Terminale · Python 3.12 · Windows 10/11

Pipeline Python complet qui détecte n'importe quelle manette (PS4, PS5, Xbox, générique), normalise ses inputs, et les redirige vers une **manette Xbox 360 virtuelle** reconnue nativement par tous les jeux PC via XInput.

---

## Pourquoi ce projet ?

En jouant à **Sekiro: Shadows Die Twice** avec une manette PS4, les boutons ne correspondaient pas aux actions et les gâchettes analogiques ne fonctionnaient pas. Sekiro détecte directement la manette physique en mode XInput et ignore les inputs clavier/souris simulés.

La solution : créer une manette Xbox 360 virtuelle au niveau de l'OS via **ViGEmBus**. Le jeu la perçoit comme un vrai périphérique hardware.

---

## Pipeline

```
Manette physique
      ↓
detector.py       ← pygame — lit les événements bruts
      ↓
normalizer.py     ← 0 → "SOUTH", axe → ("AXIS_LX", 0.73)
      ↓
mapper.py         ← lit le profil JSON actif
      ↓
output_router.py  ← aiguille vers manette virtuelle ou clavier/souris
      ↓
virtual_controller.py  ← vgamepad / ViGEmBus
      ↓
Jeu PC (XInput natif)
```

---

## Installation

### Prérequis

- Python 3.11+
- Windows 10 ou 11
- Driver [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases) installé

### Dépendances Python

```bash
pip install pygame pynput vgamepad dearpygui
```

### Lancement

```bash
# Interface graphique (recommandé)
python gui.py

# Sans interface, terminal seulement
python main.py
```

> **Important** : brancher la manette **avant** de lancer le script. Le programme attend automatiquement une manette physique et ignore la manette virtuelle créée par ViGEmBus.

---

## Structure du projet

```
controller_remapper/
├── main.py              # point d'entrée (sans GUI)
├── gui.py               # lanceur interface graphique
├── config.py            # configuration centralisée (single source of truth)
├── logger.py            # système de logs (module logging stdlib)
├── detector.py          # détection manette + reconnexion à chaud
├── normalizer.py        # normalisation inputs universels (SOUTH/EAST/L1...)
├── mapper.py            # chargement profil JSON
├── output.py            # simulation clavier/souris (mode keyboard)
├── requirements.txt
├── core/
│   ├── virtual_controller.py  # manette Xbox 360 virtuelle via ViGEmBus
│   └── output_router.py       # pattern Strategy : keyboard ↔ virtual
├── gui/
│   ├── app.py                 # fenêtre principale + boucle Dear PyGui
│   ├── controller_view.py     # boutons + joysticks graphiques + barres gâchettes
│   ├── mapping_panel.py       # tableaux mapping + profil + contrôles
│   ├── log_panel.py           # terminal de logs
│   ├── engine_thread.py       # thread daemon moteur pygame
│   ├── state.py               # état global partagé
│   └── theme.py               # couleurs, thèmes cachés Dear PyGui
└── profiles/
    ├── default.json           # mapping générique
    └── sekiro.json            # mapping Sekiro: Shadows Die Twice
```

---

## Profil JSON — Sekiro

```json
{
  "profile": "sekiro",
  "buttons": {
    "SOUTH":  { "type": "key",   "value": "space"  },
    "EAST":   { "type": "key",   "value": "e"      },
    "WEST":   { "type": "key",   "value": "r"      },
    "NORTH":  { "type": "key",   "value": "ctrl"   },
    "L1":     { "type": "key",   "value": "f"      },
    "R1":     { "type": "key",   "value": "shift"  },
    "R2":     { "type": "mouse", "value": "left"   },
    "L2":     { "type": "mouse", "value": "right"  }
  },
  "axes": {
    "AXIS_LX": { "type": "key_pair",   "neg": "q", "pos": "d", "threshold": 0.45 },
    "AXIS_LY": { "type": "key_pair",   "neg": "z", "pos": "s", "threshold": 0.45 },
    "AXIS_RX": { "type": "mouse_move", "axis": "x", "sensitivity": 12 },
    "AXIS_RY": { "type": "mouse_move", "axis": "y", "sensitivity": 12 }
  }
}
```

Pour ajouter un profil pour un nouveau jeu : créer `profiles/mon_jeu.json` et changer `DEFAULT_PROFILE` dans `config.py`.

---

## Versions

| Version | Contenu | Fichiers |
|---------|---------|----------|
| v0 · MVP | Boutons → clavier/souris | main.py, detector.py, normalizer.py, mapper.py, output.py |
| v1 · Axes | Axes analogiques + deadzone + profils multiples | normalizer.py, output.py, sekiro.json |
| v2 · Robustesse | Reconnexion à chaud + logs + config centralisée | config.py, logger.py, detector.py |
| v3 · GUI | Interface Dear PyGui dashboard gaming | gui/ (7 fichiers) |
| v4 · Virtuelle | Manette Xbox 360 virtuelle via ViGEmBus | core/ (2 fichiers) |

---

## Concepts NSI couverts

- **Event loop** — boucle infinie traitant les événements FIFO pygame
- **Dictionnaire Python O(1)** — BUTTON_MAP, AXIS_MAP
- **Abstraction** — normalizer.py masque les indices hardware
- **Sérialisation JSON** — profils de mapping
- **Classes et instances** — Mapper, Output, VirtualController
- **Threading** — moteur pygame en thread daemon séparé de la GUI
- **Design Pattern Strategy** — OutputRouter (clavier ↔ manette virtuelle)
- **Deadzone — abs()** — filtre symétrique du bruit hardware
- **Single source of truth** — config.py
- **Driver kernel** — ViGEmBus, HID, XInput

---

## Problèmes connus

- **Steam intercepte certains boutons** (notamment le bouton Guide/PS) même avec la manette virtuelle. Désactiver Steam Input dans Paramètres → Manette pour ce jeu.
- **Easy Anti-Cheat** bloque les manettes virtuelles dans certains jeux compétitifs. Utiliser le mode clavier/souris dans ce cas.
- **Dear PyGui** ne supporte pas les caractères UTF-8 étendus (accents, symboles △○□✕) sur Windows — remplacés par TRI/RON/CAR/CRX.

---

## Dépendances

| Librairie | Version | Rôle |
|-----------|---------|------|
| pygame | ≥ 2.5 | Détection manette, lecture events |
| pynput | ≥ 1.7 | Simulation clavier/souris |
| vgamepad | ≥ 0.1 | Manette Xbox 360 virtuelle |
| dearpygui | ≥ 1.x | Interface graphique |
| json | stdlib | Chargement profils |
| logging | stdlib | Système de logs |
| threading | stdlib | Thread daemon moteur |
| os | stdlib | Chemins absolus portables |

---

*Projet NSI Terminale — Remappeur universel de manette pour jeux PC*

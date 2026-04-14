# Controller Remapper Universel — v4

Remappeur universel de manette pour PC. Détecte n'importe quelle manette,
crée une manette Xbox 360 virtuelle via ViGEmBus, et translate les inputs
en temps réel. Compatible avec tous les jeux XInput (Sekiro, Dark Souls...).

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
virtual_controller.py ← vgamepad / ViGEmBus
      ↓
Jeu PC (XInput natif)
```

## Installation

```bash
pip install pygame pynput vgamepad customtkinter
```

Installer aussi le driver ViGEmBus :
https://github.com/nefarius/ViGEmBus/releases

## Lancement

```bash
python main.py
```

## Changer de profil

Dans `config.py`, modifier `DEFAULT_PROFILE = "sekiro"` par le nom du profil voulu.

## Ajouter un profil

Créer `profiles/mon_jeu.json` en suivant le format de `default.json`.

## Structure

```
controller_remapper/
├── main.py              # point d'entrée
├── config.py            # configuration centralisée
├── logger.py            # système de logs
├── detector.py          # détection manette + reconnexion
├── normalizer.py        # normalisation inputs universels
├── mapper.py            # chargement profil JSON
├── output.py            # simulation clavier/souris (mode keyboard)
├── requirements.txt
├── core/
│   ├── virtual_controller.py  # manette Xbox virtuelle
│   └── output_router.py       # aiguillage keyboard ↔ virtual
└── profiles/
    ├── default.json
    └── sekiro.json
```

## Versions

| Version | Contenu |
|---|---|
| v0 | Boutons → clavier |
| v1 | Axes analogiques + deadzone + profils |
| v2 | Reconnexion à chaud + logs + config centralisée |
| v4 | Manette virtuelle XInput via ViGEmBus |

## Projet NSI Terminale

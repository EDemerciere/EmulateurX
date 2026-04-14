# mapper.py — chargement profil JSON + association input → action
# Responsabilité unique : lire la config et retourner l'action associée.

import json

class Mapper:
    def __init__(self, profile_path: str):
        """Charge le profil JSON en mémoire."""
        with open(profile_path, "r", encoding="utf-8") as f:
            self.profile = json.load(f)
        print(f"Profil chargé : {self.profile.get('profile', '?')}")

    def get(self, input_name: str) -> dict | None:
        """Retourne l'action associée à un bouton universel."""
        return self.profile.get("buttons", {}).get(input_name)

    def get_axis(self, axis_name: str) -> dict | None:
        """Retourne l'action associée à un axe analogique."""
        return self.profile.get("axes", {}).get(axis_name)

    def reload(self, profile_path: str):
        """Recharge le profil à chaud sans recréer l'objet."""
        with open(profile_path, "r", encoding="utf-8") as f:
            self.profile = json.load(f)
        print(f"Profil rechargé : {self.profile.get('profile', '?')}")

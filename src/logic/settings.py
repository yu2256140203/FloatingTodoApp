import json
import os

class SettingsManager:
    DEFAULT_SETTINGS = {
        "opacity": 0.9,
        "theme_color": "#6c5ce7"
    }

    def __init__(self, filepath="settings.json"):
        self.filepath = filepath
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.settings.update(data)
            except:
                pass 
        return self.settings

    def save_settings(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        return self.settings.get(key, self.DEFAULT_SETTINGS.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

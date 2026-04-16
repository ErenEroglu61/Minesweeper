import json


class SettingsManager:
    def __init__(self):
        self.file = "settings.json"

        # default values
        self.sound_enabled = True
        self.music_enabled = True
        self.font_size = 12

        self.load()

    def load(self):
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
                self.sound_enabled = data.get("sound", True)
                self.music_enabled = data.get("music", True)
                self.font_size = data.get("font", 12)
        except:
            pass

    def save(self):
        data = {
            "sound": self.sound_enabled,
            "music": self.music_enabled,
            "font": self.font_size
        }

        with open(self.file, "w") as f:
            json.dump(data, f)
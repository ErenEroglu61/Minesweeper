from PyQt5.QtMultimedia import QSoundEffect, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class SoundManager:
    def __init__(self):
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("audio/click.wav"))

        self.explosion_sound = QSoundEffect()
        self.explosion_sound.setSource(QUrl.fromLocalFile("audio/explosion.wav"))

        # 🎵 Background music
        self.music = QMediaPlayer()
        self.music.setMedia(QMediaContent(QUrl.fromLocalFile("audio/background.mp3")))
        self.music.setVolume(30)

    def play_click(self):
        self.click_sound.play()

    def play_explosion(self):
        self.explosion_sound.play()

    def play_music(self):
        self.music.play()

    def stop_music(self):
        self.music.stop()
#threads.py

import time
from PyQt5 import QtCore
import pylast

class ScrobbleThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int, str)
    finished = QtCore.pyqtSignal(str)

    def __init__(self, network, artista, musica, quantidade):
        super().__init__()
        self.network = network
        self.artista = artista
        self.musica = musica
        self.quantidade = quantidade
        self.paused = False
        self.running = True

    def run(self):
        timestamp = int(time.time())
        try:
            track = self.network.get_track(self.artista, self.musica)
            album = track.get_album()
            album_title = album.get_title() if album else None

            for i in range(self.quantidade):
                if not self.running:
                    self.finished.emit("Scrobble cancelado.")
                    return
                while self.paused:
                    time.sleep(0.1)

                scrobble_timestamp = timestamp + i
                self.network.scrobble(
                    artist=self.artista,
                    title=self.musica,
                    album=album_title,
                    timestamp=scrobble_timestamp
                )
                progress_percent = int((i + 1) / self.quantidade * 100)
                self.progress.emit(
                    progress_percent,
                    f"{i + 1}/{self.quantidade} registrado para '{self.musica}' de {self.artista}"
                )
                time.sleep(1)
            self.finished.emit("Scrobbles concluídos com sucesso!")
        except pylast.WSError as e:
            self.finished.emit(f"Erro ao fazer scrobble: {e}")
        except Exception as e:
            self.finished.emit(f"Ocorreu um erro inesperado: {e}")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False

class ScrobbleThreadAlbum(QtCore.QThread):
    progress = QtCore.pyqtSignal(int, str)
    finished = QtCore.pyqtSignal(str)

    def __init__(self, network, artista, album, quantidade):
        super().__init__()
        self.network = network
        self.artista = artista
        self.album = album
        self.quantidade = quantidade
        self.paused = False
        self.running = True

    def run(self):
        timestamp = int(time.time())
        try:
            album_obj = self.network.get_album(self.artista, self.album)
            tracks = album_obj.get_tracks()
            if not tracks:
                self.finished.emit("Álbum não encontrado ou sem faixas disponíveis.")
                return

            num_tracks = len(tracks)
            scrobbles_per_track = self.quantidade // num_tracks
            extra_scrobbles = self.quantidade % num_tracks

            scrobble_counts = [scrobbles_per_track] * num_tracks
            for i in range(extra_scrobbles):
                scrobble_counts[i] += 1

            scrobble_num = 0
            for count, track in zip(scrobble_counts, tracks):
                track_title = track.get_title()
                for _ in range(count):
                    if not self.running:
                        self.finished.emit("Scrobble cancelado.")
                        return
                    while self.paused:
                        time.sleep(0.1)

                    scrobble_timestamp = timestamp + scrobble_num
                    self.network.scrobble(
                        artist=self.artista,
                        title=track_title,
                        album=self.album,
                        timestamp=scrobble_timestamp
                    )
                    scrobble_num += 1
                    progress_percent = int((scrobble_num) / self.quantidade * 100)
                    self.progress.emit(
                        progress_percent,
                        f"{scrobble_num}/{self.quantidade} registrado para '{track_title}' de {self.artista}"
                    )
                    time.sleep(1)
            self.finished.emit("Scrobbles concluídos com sucesso!")
        except pylast.WSError as e:
            self.finished.emit(f"Erro ao fazer scrobble: {e}")
        except Exception as e:
            self.finished.emit(f"Ocorreu um erro inesperado: {e}")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False
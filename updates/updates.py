# updates.py

from PyQt5.QtCore import QThread, pyqtSignal
from utils.utils import check_for_updates, update_application

class UpdateChecker(QThread):
    update_found = pyqtSignal(bool, str)

    def run(self):
        has_update, latest_version = check_for_updates()
        self.update_found.emit(has_update, latest_version)

class UpdateDownloader(QThread):
    download_complete = pyqtSignal()
    download_failed = pyqtSignal(str)  # Sinal para falha no download

    def run(self):
        success = update_application()
        if success:
            self.download_complete.emit()
        else:
            self.download_failed.emit("Erro ao baixar a atualização. Por favor, tente novamente mais tarde.")
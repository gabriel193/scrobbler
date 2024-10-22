# updates.py

from PyQt5.QtCore import QThread, pyqtSignal
from utils import check_for_updates, update_application

class UpdateChecker(QThread):
    update_found = pyqtSignal(bool, str)

    def run(self):
        has_update, latest_version = check_for_updates()
        self.update_found.emit(has_update, latest_version)

class UpdateDownloader(QThread):
    download_complete = pyqtSignal()

    def run(self):
        update_application()
        self.download_complete.emit()

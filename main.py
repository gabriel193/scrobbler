# main.py

import sys
from PyQt5 import QtWidgets
from app import ScrobblerApp

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ScrobblerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

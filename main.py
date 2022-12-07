from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
                             QCheckBox, QFormLayout, QLineEdit, QHBoxLayout, QWidget, QTextBrowser, QGridLayout,
                             QTextEdit)
import sys
from PyQt5.uic.properties import QtGui
import lamport
import maths
from random import randint
from sender import SenderWindow
from recipient import RecipientWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    recipient = RecipientWindow()
    sender = SenderWindow()
    recipient.pass_window(sender)
    sender.pass_window(recipient)
    recipient.show()
    sender.show()
    app.exec()
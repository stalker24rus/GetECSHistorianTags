from PyQt5 import QtGui, QtWidgets
from sources.sql import check_text


class MyCustomPlainText(QtWidgets.QPlainTextEdit):
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if check_text(event.mimeData().text()):
            if self.toPlainText() != '':
                self.setPlainText(self.toPlainText() + ', ' + event.mimeData().text())
            else:
                self.setPlainText(event.mimeData().text())
            self.moveCursor(QtGui.QTextCursor.End)

"""
class ChangeMethodsDnDTagList:  # (QtWidgets.QPlainTextEdit)
    def __init__(self, obj):
        # super().__init__()
        self.obj = obj  # will be type = BeforeQtWidgets.QPlainTextEdit
        self.obj.dragEnterEvent = self.dragEnterEvent
        self.obj.dropEvent = self.dropEvent
        self.obj.dragMoveEvent = self.dragEnterEvent

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if check_text(event.mimeData().text()):
            if self.obj is not None:
                if self.obj.toPlainText() != '':
                    self.obj.setPlainText(self.obj.toPlainText() + ', ' + event.mimeData().text())
                else:
                    self.obj.setPlainText(event.mimeData().text())
                self.obj.moveCursor(QtGui.QTextCursor.End)
"""

""""
def change_dnd_method(obj):
    def dragEnterEvent(event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(event):
        if check_text(event.mimeData().text()):
            if obj is not None:
                if obj.toPlainText() != '':
                    obj.setPlainText(obj.toPlainText() + ', ' + event.mimeData().text())
                else:
                    obj.setPlainText(event.mimeData().text())
                obj.moveCursor(QtGui.QTextCursor.End)
    obj.dragEnterEvent = dragEnterEvent
    obj.dropEvent = dropEvent
    obj.dragMoveEvent = dragEnterEvent
"""
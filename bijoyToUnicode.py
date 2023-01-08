# -*- coding:utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QTextEdit, QTextBrowser)
from PyQt5.QtGui import QPainter, QColor 
from PyQt5.QtCore import QSize, QRect

# class LineNumberArea(QWidget):
#     def __init__(self, editor):
#         super().__init__(editor)
#         self.editor = editor

#     def sizeHint(self):
#         return QSize(self.editor.lineNumberAreaWidth(), 0)

#     def paintEvent(self, event):
#         self.editor.lineNumberAreaPaintEvent(event)

# class TextEditor(QTextEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.lineNumberArea = LineNumberArea(self)

#         self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
#         self.updateRequest.connect(self.updateLineNumberArea)
#         self.cursorPositionChanged.connect(self.highlightCurrentLine)

#         self.updateLineNumberAreaWidth(0)
#         self.highlightCurrentLine()

#     def lineNumberAreaWidth(self):
#         digits = 1
#         count = max(1, self.blockCount())
#         while count >= 10:
#             count /= 10
#             digits += 1
#         space = 3 + self.fontMetrics().width('9') * digits
#         return space

#     def updateLineNumberAreaWidth(self, _):
#         self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

#     def updateLineNumberArea(self, rect, dy):
#         if dy:
#             self.lineNumberArea.scroll(0, dy)
#         else:
#             self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
#         if rect.contains(self.viewport().rect()):
#             self.updateLineNumberAreaWidth(0)

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         cr = self.contentsRect()
#         self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

#     def lineNumberAreaPaintEvent(self, event):
#         painter = QPainter(self.lineNumberArea)
#         painter.fillRect(event.rect(), Qt.lightGray)
#         block = self.firstVisibleBlock()
#         blockNumber = block.blockNumber()
#         top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
#         bottom = top + self.blockBoundingRect(block).height()
#         while block.isValid() and top <= event.rect().bottom():
#             if block.isVisible() and bottom >= event.rect().top():
#                 number = str(blockNumber + 1)
#                 painter.setPen(Qt.black)
#                 painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
#                                  Qt.AlignRight, number)
#             block = block.next()
#             top = bottom
#             bottom = top + self.blockBoundingRect(block).height()
#             blockNumber += 1

# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.text_edit = TextEditor(self)
#         self.setCentralWidget(self.text_edit)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

import string

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget

class BanglaTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Bangla alphabet characters
        self.bangla_alphabet = "অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ"

        # Connect to the cellChanged signal
        self.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        # Get the current item in the cell
        item = self.item(row, column)

        # Check if the item's text is a Bangla alphabet character
        if item.text() not in self.bangla_alphabet:
            # If the text is not a Bangla alphabet character, set the text to an empty string
            item.setText("")

if __name__ == "__main__":
    app = QApplication([])

    table_widget = BanglaTableWidget()

    # Set the number of rows and columns in the table widget
    table_widget.setRowCount(5)
    table_widget.setColumnCount(5)

    # Add some items to the table widget
    for i in range(5):
        for j in range(5):
            item = QTableWidgetItem("Item ({}, {})".format(i, j))
            table_widget.setItem(i, j, item)

    table_widget.show()

    app.exec_()


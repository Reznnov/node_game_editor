from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from examples.calc_conf import *
from nodeeditor.utils import dumpException



class QDMDragListbox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # init
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyItems()


    def addMyItems(self):
        self.addMyItem("Input", "icons/fi-tr-caret-circle-right.svg", OP_NODE_INPUT)
        self.addMyItem("Output", "icons/fi-tr-code-commit.svg", OP_NODE_OUTPUT)
        self.addMyItem("Scene", "icons/add.svg", OP_NODE_ADD)
        self.addMyItem("Choice Scene", "icons/fi-tr-code-fork.svg", OP_NODE_SUB)
        self.addMyItem("Script", "icons/fi-tr-file-code.svg", OP_NODE_MUL)
        self.addMyItem("Object", "icons/fi-tr-photo-film-music.svg", OP_NODE_DIV)

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self) # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kwargs):
        # print("ListBox::startDrag")

        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            # print("dragging item <%d>" % op_code, item)

            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

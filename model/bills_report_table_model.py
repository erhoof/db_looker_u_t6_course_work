

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt

class BillsReportTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._col = ('ID','Название', 'Кол-во', 'Сумма', 'НДС')

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if len(self._data):
            return len(self._data[0])
        return 0

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._col[col]
        return None
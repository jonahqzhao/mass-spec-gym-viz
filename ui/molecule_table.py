from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableView


class MoleculeTableModel(QAbstractTableModel):
    HEADERS = [
        "Formula",
        "Parent Mass",
        "Class1",
        "Class2",
        "Class3",
        "Class4",
        "# Spectra",
        "Elements",
    ]

    def __init__(self, store):
        super().__init__()

        self.store = store

        self.store.molecules_changed.connect(self.refresh)

    def refresh(self):
        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return len(self.store.filtered_molecules)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return None

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return None

        molecule = self.store.filtered_molecules[index.row()]

        values = [
            molecule.formula,
            round(molecule.parent_mass, 4),
            molecule.class1,
            molecule.class2,
            molecule.class3,
            molecule.class4,
            molecule.spectrum_count,
            "".join(sorted(molecule.elements)),
        ]

        return values[index.column()]


class MoleculeTable(QTableView):
    def __init__(self, store):
        super().__init__()

        self.setModel(MoleculeTableModel(store))

        self.setSortingEnabled(True)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)
        self.verticalHeader().setVisible(False)
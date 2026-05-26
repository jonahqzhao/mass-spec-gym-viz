from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)


class MoleculeFiltersPanel(QWidget):
    def __init__(self, store):
        super().__init__()

        self.store = store

        layout = QVBoxLayout(self)

        class_box = QGroupBox("Classes")
        class_layout = QFormLayout(class_box)

        self.class1 = QComboBox()
        self.class2 = QComboBox()
        self.class3 = QComboBox()
        self.class4 = QComboBox()

        self.populate_dropdown(self.class1, "class1")
        self.populate_dropdown(self.class2, "class2")
        self.populate_dropdown(self.class3, "class3")
        self.populate_dropdown(self.class4, "class4")

        class_layout.addRow("Class1", self.class1)
        class_layout.addRow("Class2", self.class2)
        class_layout.addRow("Class3", self.class3)
        class_layout.addRow("Class4", self.class4)

        layout.addWidget(class_box)

        mass_box = QGroupBox("Parent Mass")
        mass_layout = QFormLayout(mass_box)

        self.mass_min = QDoubleSpinBox()
        self.mass_max = QDoubleSpinBox()

        self.mass_min.setRange(0, 5000)
        self.mass_max.setRange(0, 5000)

        self.mass_max.setValue(5000)

        mass_layout.addRow("Min", self.mass_min)
        mass_layout.addRow("Max", self.mass_max)

        layout.addWidget(mass_box)

        elements_box = QGroupBox("Elements")
        elements_layout = QVBoxLayout(elements_box)

        self.c_box = QCheckBox("C")
        self.h_box = QCheckBox("H")
        self.n_box = QCheckBox("N")
        self.o_box = QCheckBox("O")
        self.p_box = QCheckBox("P")
        self.s_box = QCheckBox("S")

        self.only_exact = QCheckBox("Only these elements")

        elements_layout.addWidget(self.c_box)
        elements_layout.addWidget(self.h_box)
        elements_layout.addWidget(self.n_box)
        elements_layout.addWidget(self.o_box)
        elements_layout.addWidget(self.p_box)
        elements_layout.addWidget(self.s_box)
        elements_layout.addWidget(self.only_exact)

        layout.addWidget(elements_box)

        self.apply_button = QPushButton("Apply Filters")
        self.clear_button = QPushButton("Clear Filters")

        layout.addWidget(self.apply_button)
        layout.addWidget(self.clear_button)
        layout.addStretch()

        self.apply_button.clicked.connect(self.apply_filters)
        self.clear_button.clicked.connect(self.clear_filters)

        self.results_label = QLabel()
        layout.addWidget(self.results_label)
        self.update_results_label()
        self.store.molecules_changed.connect(self.update_results_label)

    def populate_dropdown(self, dropdown, attr):
        dropdown.addItem("Any")

        values = sorted({
            getattr(m, attr)
            for m in self.store.all_molecules
            if getattr(m, attr)
        })

        dropdown.addItems(values)

    def apply_filters(self):
        f = self.store.filter

        f.class1 = self.value_or_none(self.class1)
        f.class2 = self.value_or_none(self.class2)
        f.class3 = self.value_or_none(self.class3)
        f.class4 = self.value_or_none(self.class4)

        f.parent_mass_min = self.mass_min.value()
        f.parent_mass_max = self.mass_max.value()

        required = set()

        if self.c_box.isChecked():
            required.add("C")

        if self.h_box.isChecked():
            required.add("H")

        if self.n_box.isChecked():
            required.add("N")

        if self.o_box.isChecked():
            required.add("O")

        if self.p_box.isChecked():
            required.add("P")

        if self.s_box.isChecked():
            required.add("S")

        f.required_elements = required
        f.exact_elements = self.only_exact.isChecked()

        self.store.apply_filters()

    def clear_filters(self):
        self.class1.setCurrentIndex(0)
        self.class2.setCurrentIndex(0)
        self.class3.setCurrentIndex(0)
        self.class4.setCurrentIndex(0)

        self.mass_min.setValue(0)
        self.mass_max.setValue(5000)

        for box in [
            self.c_box,
            self.h_box,
            self.n_box,
            self.o_box,
            self.p_box,
            self.s_box,
            self.only_exact,
        ]:
            box.setChecked(False)

        self.apply_filters()

    def update_results_label(self):
        shown = len(self.store.filtered_molecules)

        total = len(self.store.all_molecules)

        self.results_label.setText(
            f"Showing {shown} / {total} molecules"
        )

    @staticmethod
    def value_or_none(dropdown):
        value = dropdown.currentText()

        if value == "Any":
            return None

        return value
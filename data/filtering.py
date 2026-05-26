class MoleculeFilter:
    def __init__(self):
        self.class1 = None
        self.class2 = None
        self.class3 = None

        self.parent_mass_min = 0
        self.parent_mass_max = 5000

        self.required_elements = set()
        self.exact_elements = False

    def matches(self, molecule):
        if self.class1 and molecule.class1 != self.class1:
            return False

        if self.class2 and molecule.class2 != self.class2:
            return False

        if self.class3 and molecule.class3 != self.class3:
            return False
        
        if self.class4 and molecule.class4 != self.class4:
            return False

        if molecule.parent_mass < self.parent_mass_min:
            return False

        if molecule.parent_mass > self.parent_mass_max:
            return False

        molecule_elements = set(molecule.elements)

        if not self.required_elements.issubset(molecule_elements):
            return False

        if self.exact_elements:
            if molecule_elements != self.required_elements:
                return False

        return True
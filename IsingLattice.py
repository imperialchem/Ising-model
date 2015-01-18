import numpy as np

class IsingLattice:

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.lattice = np.random.choice([-1,1], size=(n_rows, n_cols))

    def energy(self):
        "Return the total energy of the current lattice configuration."
        energy = 0.0
        return energy

    def magnetisation(self):
        "Return the total magnetisation of the current lattice configuration."
        magnetisation = 0.0
        return magnetisation

    def montecarlostep(self, T):
        pass

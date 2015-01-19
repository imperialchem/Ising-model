import numpy as np

class IsingLattice:
    self.E = 0.0
    self.E2 = 0.0
    self.M = 0.0
    self.M2 = 0.0

    self.n_cycles = 0

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.lattice = np.random.choice([-1,1], size=(n_rows, n_cols))

    def energy(self):
        "Return the total energy of the current lattice configuration."
        energy = 0.0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                bottom_neighbor = i+1
                right_neighbor = j+1
                if bottom_neighbor >= self.n_rows:
                    bottom_neighbor = 0
                if right_neighbor >= self.n_cols:
                    right_neighbor = 0
                energy -= self.lattice[i,j]*self.lattice[i,right_neighbor]
                energy -= self.lattice[i,j]*self.lattice[bottom_neighbor,j]
        return energy

    def magnetisation(self):
        "Return the total magnetisation of the current lattice configuration."
        magnetisation = 0.0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                magnetisation += self.lattice[i,j]
        return magnetisation

    def montecarlostep(self, T):
        # complete this function so that it performs a single Monte Carlo step
        # the function should end by calculating and returning both the energy and magnetisation:

        return energy, magnetisation
        
    def statistics(self):
        # complete this function so that it calculates the correct values for the averages of E, E*E (E2), M, M*M (M2), and returns them
        aveE = 0.0
        aveE2 = 0.0
        aveM = 0.0
        aveM2 = 0.0

        return aveE, aveE2, aveM, aveM2

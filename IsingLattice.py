import numpy as np

class IsingLattice:

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.lattice = np.random.choice([-1, 1], size=(n_rows, n_cols))
        #Running sums
        self.E_tally = self.energy()
        self.E2_tally = self.E**2
        self.M_tally = self.magnetisation()
        self.M2_tally = self.M**2
        self.n_steps = 0

    def energy(self):
        """Return the total energy of the current lattice configuration."""
        energy = 0.0
        return energy

    def magnetisation(self):
        """Return the total magnetisation of the current lattice configuration."""
        magnetisation = 0.0
        return magnetisation

    def montecarlostep(self, temp):
        """A single Monte-Carlo trial move. Attempts to flip a random spin.
        Returns a tuple with the energy and magnetisation of the new configuration.
        """
        # complete this function so that it performs a single Monte Carlo step
        energy = self.energy()
        # the following two lines will select the coordinates of the random spin for you
        random_i = np.random.choice(range(0, self.n_rows))
        random_j = np.random.choice(range(0, self.n_cols))
        # the following line will choose for you a random number in the range [0,1)
        random_number = np.random.random()
        ...

    def statistics(self):
        """Returns a tuple with the averaged values of energy, energy squared,
        magnetisation, magnetisation squared, and the current step, in this order.
        """
        # complete this function so that it calculates the correct values for the averages of E, E*E (E2), M, M*M (M2), and returns them with Nsteps
        ...

    def delta_energy(self, i, j):
        """Return the change in energy if the spin at (i,j) were to be flipped."""
        # Optional
        ...

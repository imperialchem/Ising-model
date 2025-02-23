from IsingLattice import IsingLattice
from matplotlib import pyplot as plt
import numpy as np

n_rows = 8
n_cols = 8
il = IsingLattice(n_rows, n_cols)
il.lattice = np.ones((n_rows, n_cols))

# recalculate the energy after changing the lattice
il.energy()
il.magnetisation()

spins = n_rows * n_cols
runtime = 100000
times = range(runtime)
temps = np.arange(1.5, 3.5, 0.1)
energies = []
magnetisations = []
energysq = []
magnetisationsq = []
for t in temps:
    for i in times:
        if i % 1000 == 0:
            print(t, i)
        energy, magnetisation = il.montecarlostep(t)
    aveE, aveE2, aveM, aveM2, n_steps = il.statistics()
    energies.append(aveE)
    energysq.append(aveE2)
    magnetisations.append(aveM)
    magnetisationsq.append(aveM2)
    # reset the IL object for the next cycle
    il.E = 0.0
    il.E2 = 0.0
    il.M = 0.0
    il.M2 = 0.0
    il.n_steps = 0
fig = plt.figure()
enerax = fig.add_subplot(2, 1, 1)
enerax.set_ylabel("Energy per spin")
enerax.set_xlabel("Temperature")
enerax.set_ylim((-2.1, 0.1))
magax = fig.add_subplot(2, 1, 2)
magax.set_ylabel("Magnetisation per spin")
magax.set_xlabel("Temperature")
magax.set_ylim((-1.1, 1.1))
enerax.plot(temps, np.array(energies) / spins)
magax.plot(temps, np.array(magnetisations) / spins)
plt.show()

final_data = np.column_stack(
    (temps, energies, energysq, magnetisations, magnetisationsq)
)
np.savetxt(f"{n_rows}x{n_cols}.dat", final_data)

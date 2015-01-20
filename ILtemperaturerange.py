from IsingLattice import *
from matplotlib import pylab as pl
import numpy as np

n_rows = 8
n_cols = 8
il = IsingLattice(n_rows, n_cols)
il.lattice = np.ones((n_rows, n_cols))
spins = n_rows*n_cols
runtime = 50000
times = range(runtime)
temps = np.arange(2.0, 3.0, 0.1)
energies = []
magnetisations = []
energy_errs = []
mag_errs = []
for t in temps:
    for i in times:
        if i % 100 == 0:
            print(t, i)
        energy, magnetisation = il.montecarlostep(t)
    aveE, aveE2, aveM, aveM2, n_cycles = il.statistics()
    print("<E> = ", aveE, "+-", np.sqrt((aveE2-aveE*aveE)/n_cycles))
    print("<M> = ", aveM, "+-", np.sqrt((aveM2-aveM*aveM)/n_cycles))
    energies.append(aveE/spins)
    energy_errs.append(np.sqrt((aveE2-aveE*aveE)/n_cycles/spins))
    mag_errs.append(np.sqrt((aveM2-aveM*aveM)/n_cycles/spins))
    magnetisations.append(aveM/spins)
    #reset the IL object for the next cycle
    il.E = 0.0
    il.E2 = 0.0
    il.M = 0.0
    il.M2 = 0.0
    il.n_cycles = 0
fig = pl.figure()
enerax = fig.add_subplot(2,1,1)
enerax.set_ylabel("Energy per spin")
enerax.set_xlabel("Temperature")
enerax.set_ylim([-2.1, 2.1])
magax = fig.add_subplot(2,1,2)
magax.set_ylabel("Magnetisation per spin")
magax.set_xlabel("Temperature")
magax.set_ylim([-1.1, 1.1])
enerax.errorbar(temps, energies, yerr=energy_errs)
magax.errorbar(temps, magnetisations, yerr=mag_errs)
print energies, magnetisations
pl.show()

final_data = np.column_stack((temps, energies, energy_errs, magnetisations, mag_errs))
np.savetxt("8x8.dat", final_data)

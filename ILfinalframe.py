from IsingLattice import *
from matplotlib import pylab as pl
from matplotlib import animation
import sys
from time import *
import numpy as np

il = IsingLattice(8,8)
spins = 8*8
runtime = 100000
times = range(runtime)
temps = np.arange(0.5, 5.0, 0.05)
energies = []
magnetisations = []
C = []
energy_errs = []
mag_errs = []
for t in temps:
    E = []
    M = []
    for i in times:
        if i % 100 == 0:
            print t, i
        energy, magnetisation = il.montecarlostep(t)
        E.append(energy)
        M.append(magnetisation)
    cutoff = int(runtime/2)

    aveE = np.mean(E[cutoff:])
    aveE2 = np.mean(E[cutoff:]*E[cutoff:])
    aveM = np.mean(M[cutoff:])
    aveM2 = np.mean(M[cutoff:]*M[cutoff:])
    print "<E> = ", aveE, "+-", np.sqrt((aveE2-aveE*aveE)/E.shape[0])
    print "<M> = ", aveM, "+-", np.sqrt((aveM2-aveM*aveM)/M.shape[0])
    energies.append(aveE/spins)
    energy_errs.append(np.sqrt((aveE2-aveE*aveE)/len(E)/spins))
    mag_errs.append(np.sqrt((aveM2-aveM*aveM)/len(M)/spins))
    magnetisations.append(aveM/spins)
    C.append((aveE2-aveE*aveE)/(t*t)/spins)

fig = pl.figure()
enerax = fig.add_subplot(3,1,1)
magax = fig.add_subplot(3,1,2)
Cax = fig.add_subplot(3,1,3)
enerax.errorbar(temps, energies, yerr=energy_errs)
magax.errorbar(temps, magnetisations, yerr=mag_errs)
Cax.plot(temps, C)
pl.show()

final_data = np.column_stack((temps, energies, energy_errs, magnetisations, mag_errs, C))
np.savetxt("8x8.dat", final_data)

from IsingLattice import *
from matplotlib import pylab as pl
from matplotlib import animation
import sys
from time import *
import numpy as np

il = IsingLattice(8,8)

figure = pl.figure()
matax = figure.add_subplot(3,1,1)
enerax = figure.add_subplot(3,1,2)
magnetax = figure.add_subplot(3,1,3)
mat = matax.matshow(il.lattice, cmap=pl.cm.gray, vmin=-1.0, vmax=1.0)

energies, = enerax.plot([], [], '-', lw=2, label="E")
enerax.legend()
enerax.set_ylim(-2.1, 2.1)

magnetisations, = magnetax.plot([], [], '-', lw=2, label="m")
magnetax.legend()
magnetax.set_ylim(-1.1, 1.1)

xdata, ener_ydata, m_ydata = [], [], []

def data_gen():
    t = data_gen.t
    spins = 8*8
    while True:
        energy, magnetisation = il.montecarlostep(1.0)
        t += 1
        yield t, il.lattice,1.0*energy/spins,1.0*magnetisation/spins

data_gen.t = 0

def updateFigure(data):
    t, lattice, energy, m = data
    mat.set_data(lattice)
    xdata.append(t)
    ener_ydata.append(energy)
    m_ydata.append(m)
    xmin, xmax = enerax.get_xlim()
    if t >= xmax:
        enerax.set_xlim(xmin, 2*xmax)
        enerax.figure.canvas.draw()
        magnetax.set_xlim(xmin, 2*xmax)
        magnetax.figure.canvas.draw()
    enerax.set_title("Step {}.".format(t))
    enerax.figure.canvas.draw()
    energies.set_data(xdata, ener_ydata)
    magnetax.set_title("Step {}".format(t))
    magnetax.figure.canvas.draw()
    magnetisations.set_data(xdata, m_ydata)

    return energies, mat

anim = animation.FuncAnimation(figure, updateFigure, data_gen, repeat=False, interval=0)

pl.show()

E, E2, M, M2 = il.statistics()

print "Averaged quantities:"
print "E = ", E
print "E*E = ", E2
print "M = ", M
print "M*M = ", M2

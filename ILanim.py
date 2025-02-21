from typing import Optional

from IsingLattice import IsingLattice
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
import itertools
import functools

# Increase this number for a faster animation!
STRIDE = 1  # How many Monte-Carlo steps per animation frame

n_rows, n_cols = 8, 8
il = IsingLattice(n_rows, n_cols)
spins = n_rows * n_cols
temperature = 0.5

(figure, (matax, enerax, magnetax)) = plt.subplots(3)
enerax.set_ylabel("$E$ per spin / $k_B$")
magnetax.set_ylabel("$M$ per spin")

colour_map = mpl.colormaps["gray"]
matrix = matax.matshow(il.lattice, cmap=colour_map, vmin=-1.0, vmax=1.0)
matax.xaxis.set_ticks([])
matax.yaxis.set_ticks([])

(energies,) = enerax.plot([], [], "-", lw=2, label="$E$")
enerax.set_ylim(-2.1, 2.1)

(magnetisations,) = magnetax.plot([], [], "-", lw=2, label="$M$")
magnetax.set_ylim(-1.1, 1.1)

xdata, ener_ydata, m_ydata = [], [], []


def data_gen(temp: float, start=0, n_steps=None, stride=1):
    """
    Perform the calculations for the animation

    Parameters
    ----------
    `n_steps` : int | None
        How many frames to animate.
        If `None`, animates until stopped.
        Do not set to None if running in a notebook.

    `stride` : int
        How many simulation steps to run per animation frame.

    """

    # use a separate step, because multiple per animation frame
    spins = il.n_rows * il.n_cols

    if n_steps is None:
        # Infinite loop
        iterator = itertools.count(start=start)
    else:
        # Finite number of frames
        iterator = range(start, start + n_steps)

    for step in iterator:
        energy, magnetisation = il.montecarlostep(temp)
        step += 1
        if step % stride == 0:
            yield step, il.lattice, 1.0 * energy / spins, 1.0 * magnetisation / spins


def updateFigure(data):
    step, lattice, energy, mag = data
    matrix.set_data(lattice)
    xdata.append(step)
    ener_ydata.append(energy)
    m_ydata.append(mag)
    xmin, xmax = enerax.get_xlim()
    if step >= xmax:
        enerax.set_xlim(xmin, 2 * xmax)
        enerax.figure.canvas.draw()
        magnetax.set_xlim(xmin, 2 * xmax)
        magnetax.figure.canvas.draw()
    enerax.set_title("Step {}.".format(step))
    enerax.figure.canvas.draw()
    energies.set_data(xdata, ener_ydata)
    magnetax.figure.canvas.draw()
    magnetisations.set_data(xdata, m_ydata)

    return energies, magnetisations, matrix


def print_stats():
    E, E2, M, M2, N = il.statistics()

    print("Averaged quantities:")
    print("E = ", E / spins)
    print("E*E = ", E2 / spins / spins)
    print("M = ", M / spins)
    print("M*M = ", M2 / spins / spins)
    print(f"Ran for {N} steps")


def setup_animation(
    n_steps: Optional[int] = 2000, frame_interval: int = 30, stride: int = 1
) -> animation.FuncAnimation:
    """
    Create the animation!

    Parameters
    ----------
    `n_steps` : int | None
        How many rames to animate.
        If `None`, animates until stopped.
        Do not set to None if running in a notebook.

    `stride` : int
        How many simulation steps to run per animation frame.

    """

    _data_gen = functools.partial(
        data_gen, temp=temperature, n_steps=n_steps, stride=stride
    )

    if n_steps is None:
        # Otherwise we have a warning about a possibly infinite run
        save_count = 100
    else:
        save_count = n_steps

    return animation.FuncAnimation(
        figure,
        updateFigure,
        _data_gen,
        repeat=False,
        interval=frame_interval,
        save_count=save_count,
        blit=True,  # Improves performance of frame rendering
    )


if __name__ == "__main__":
    anim = setup_animation(n_steps=None, frame_interval=10, stride=STRIDE)
    plt.show(block=True)
    print_stats()

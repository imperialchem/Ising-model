from dataclasses import dataclass
from typing import List, Optional

from matplotlib.axes import Axes

from IsingLattice import IsingLattice
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.figure import Figure
import matplotlib as mpl
import itertools
import functools

# Increase this number for a faster animation!
STRIDE = 1  # How many Monte-Carlo steps per animation frame
N_STEPS = 500  # How many steps to run, when running in a notebook or IPython

N_ROWS, N_COLS = 8, 8
TEMPERATURE = 0.5


@dataclass
class AnimationState:
    """
    Current state of the animation
    """

    figure: Figure
    enerax: Axes
    magnetax: Axes
    matax: Axes
    matrix: ...
    energies: ...
    magnetisations: ...
    step_label: ...
    x_data: List[int]
    ener_y_data: List[float]
    m_y_data: List[float]


def setup_figures(il: IsingLattice) -> AnimationState:
    (figure, (matax, enerax, magnetax)) = plt.subplots(3)
    enerax.set_ylabel("$E$ per spin / $k_B$")
    magnetax.set_ylabel("$M$ per spin")

    colour_map = mpl.colormaps["gray"]
    matrix = matax.matshow(il.lattice, cmap=colour_map, vmin=-1.0, vmax=1.0)
    matax.xaxis.set_ticks([])
    matax.yaxis.set_ticks([])
    # step_label = enerax.set_title("Step: 0")
    matax: Axes
    step_label = matax.text(
        il.n_cols / 2 - 1,
        il.n_rows + 3,
        "",
        transform=matax.transData,
        horizontalalignment="center",
    )

    (energies,) = enerax.plot([], [], "-", lw=2, label="$E$")
    enerax.set_ylim(-2.1, 2.1)

    (magnetisations,) = magnetax.plot([], [], "-", lw=2, label="$M$")
    magnetax.set_ylim(-1.1, 1.1)

    return AnimationState(
        figure=figure,
        enerax=enerax,
        magnetax=magnetax,
        matrix=matrix,
        matax=matax,
        energies=energies,
        magnetisations=magnetisations,
        step_label=step_label,
        x_data=[],
        ener_y_data=[],
        m_y_data=[],
    )


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


def updateFigure(data, state: AnimationState):
    step, lattice, energy, mag = data
    s = state

    s.x_data.append(step)
    s.ener_y_data.append(energy)
    s.m_y_data.append(mag)

    xmin, xmax = s.enerax.get_xlim()
    if step >= xmax:
        s.enerax.set_xlim(xmin, 2 * xmax)
        # s.enerax.figure.canvas.draw()
        s.magnetax.set_xlim(xmin, 2 * xmax)

        # Redraw!
        s.figure.canvas.draw()

    s.matrix.set_data(lattice)
    s.step_label.set_text(f"Step: {step}")
    s.energies.set_data(s.x_data, s.ener_y_data)
    s.magnetisations.set_data(s.x_data, s.m_y_data)

    return s.energies, s.magnetisations, s.matrix, s.step_label


def print_stats(il: IsingLattice):
    E, E2, M, M2, N = il.statistics()
    spins = il.n_rows * il.n_cols

    print("Averaged quantities:")
    print("E = ", E / spins)
    print("E*E = ", E2 / spins / spins)
    print("M = ", M / spins)
    print("M*M = ", M2 / spins / spins)
    print(f"Ran for {N} steps")


def setup_animation(
    il: IsingLattice,
    temperature: float = TEMPERATURE,
    n_steps: Optional[int] = 2000,
    frame_interval: int = 30,
    stride: int = 1,
) -> animation.FuncAnimation:
    """
    Create the animation!

    Parameters
    ----------
    il : IsingLattice
        The IsingLattice object to simulate.

    `n_steps` : int | None
        How many rames to animate.
        If `None`, animates until stopped.
        Do not set to None if running in a notebook.

    `stride` : int
        How many simulation steps to run per animation frame.

    """
    state = setup_figures(il)

    _data_gen = functools.partial(
        data_gen, temp=temperature, n_steps=n_steps, stride=stride
    )

    _updateFigure = functools.partial(updateFigure, state=state)

    if n_steps is None:
        # Otherwise we have a warning about a possibly infinite run
        save_count = 100
    else:
        save_count = n_steps

    return animation.FuncAnimation(
        state.figure,
        _updateFigure,
        _data_gen,
        repeat=False,
        interval=frame_interval,
        save_count=save_count,
        blit=True,  # Improves performance of frame rendering
    )


if __name__ == "__main__":
    is_interactive = plt.isinteractive()
    n_steps = N_STEPS if is_interactive else None
    frame_interval = 30

    il = IsingLattice(n_rows=N_ROWS, n_cols=N_COLS)

    anim = setup_animation(
        il, n_steps=n_steps, frame_interval=frame_interval, stride=STRIDE
    )

    if is_interactive:
        print(f"Rendering {n_steps} frames of animation")
        from IPython.display import HTML, display

        display(HTML(anim.to_html5_video()))
        # To prevent duplicate of the figure appearing after animation
        plt.close()
    else:
        plt.show(block=True)

    print_stats(il)

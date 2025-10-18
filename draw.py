import matplotlib.pyplot as plt
import numpy as np

def Draw_MPC_point_stabilization_v1(rob_diam=0.3, init_state=None, target_state=None, robot_states=None):
    """
    Minimal plotting helper for the drone MPC example.
    - init_state, target_state: 1D arrays (state vector)
    - robot_states: (N+1, nx) array of states over time
    Plots XY trajectory and Z (altitude) vs timestep.
    """
    if robot_states is None:
        print("No robot_states to plot.")
        return

    # try to extract x,y,z from typical state layout:
    # assume positions are first 3 entries (x,y,z). Adapt if different.
    try:
        xs = np.asarray(robot_states)
        x = xs[:, 0]
        y = xs[:, 1]
        z = xs[:, 2]
    except Exception as e:
        print("Unable to extract positions from robot_states:", e)
        return

    fig = plt.figure(figsize=(9,4))
    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(x, y, '-o', markersize=3)
    if init_state is not None:
        ax1.plot(init_state[0], init_state[1], 'gs', label='init')
    if target_state is not None:
        ax1.plot(target_state[0], target_state[1], 'r*', label='target')
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_title('XY Trajectory')
    ax1.axis('equal')
    ax1.legend()

    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(np.arange(len(z)), z, '-o', markersize=3)
    ax2.set_xlabel('step'); ax2.set_ylabel('z'); ax2.set_title('Altitude (z)')

    plt.tight_layout()
    plt.show()

import numpy as np
import random
from scipy.special import factorial
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from joblib import Parallel, delayed


# for interactive plots
matplotlib.use('QtAgg')

def gauss_2d(sigma, size):
    x = np.linspace(-3, 3, size)
    y = np.linspace(-3, 3, size)
    # full coordinate arrays
    xx, yy = np.meshgrid(x, y)

    g = 1/(np.sqrt(2 * np.pi * sigma**2)) * np.exp(-xx**2/ (2*sigma**2)) * 1/(np.sqrt(2 * np.pi * sigma**2)) * np.exp(-yy**2/ (2*sigma**2))

    return g

# 4.1
"""
P_0 = np.zeros((1000, 1000))
# add gradient
for i in range(1000):
    P_0[i, :] = np.flip(np.arange(0, 10, 0.01))

# add obstacles
num_obst = 20
for i in range(num_obst):
    size = np.random.randint(250, 520)
    pos_x = np.random.randint(0, 1000 - size - 20)
    pos_y = np.random.randint(0, 1000 - size - 20)
    sigma = np.random.randint(50, 100)/100
    P_0[pos_x:pos_x+size, pos_y:pos_y+size] += gauss_2d(sigma, size) * 10

border_height = np.amax(P_0)
for x in range(1000):
    for y in range(1000):
        if x < 20 and y < 20:
            P_0[x, y] += (1 - min(x, y) / 20) * border_height
        elif x < 20 and y > 980:
            P_0[x, y] += max((1 - x / 20), (y-980) / 20) * border_height
        elif x > 980 and y < 20:
            P_0[x, y] += max((1 - y / 20), (x - 980) / 20) * border_height
        elif x > 980 and y > 980:
            P_0[x, y] += max((y - 980) / 20, (x - 980) / 20) * border_height
        elif x < 20:
            P_0[x, y] += (1 - x / 20) * border_height
        elif y < 20:
            P_0[x, y] += (1 - y / 20) * border_height
        elif x > 980:
            P_0[x, y] += (x - 980) / 20 * border_height
        elif y > 980:
            P_0[x, y] += (y-980) / 20 * border_height


P_0 = P_0 / np.amax(P_0)

# some robot trajectory
# a)
r_0_x = np.random.randint(20, 50)
r_0_y = np.random.randint(20, 980)

r_0_tr_x = []
r_0_tr_y = []

v_x = 1
v_y = 1

# b)
r_1_x = r_0_x
r_1_y = r_0_y

r_1_tr_x = []
r_1_tr_y = []

v_1_x = 1
v_1_y = 1
delta_v_x = 0
delta_v_y = 0


for t in range(50000):
    # controller for a
    dt = 100
    v_x = P_0[int(r_0_y), int(r_0_x)] - P_0[int(r_0_y), int(r_0_x)+1]
    v_y = P_0[int(r_0_y), int(r_0_x)] - P_0[int(r_0_y)+1, int(r_0_x)]

    r_0_x += v_x * dt
    r_0_y += v_y * dt

    if r_0_x > 998: r_0_x = 998
    if r_0_x < 1: r_0_x = 1
    if r_0_y > 998: r_0_y = 998
    if r_0_y < 1: r_0_y = 1

    r_0_tr_x.append(r_0_x)
    r_0_tr_y.append(r_0_y)

    # controller for b
    c = 0.00000001
    dt = 0.00001
    delta_v_x = c * (v_1_x) + (P_0[int(r_1_y), int(r_1_x)] - P_0[int(r_1_y), int(r_1_x)+1])  # TODO is this formula correct
    delta_v_y = c * (v_1_y) + (P_0[int(r_1_y), int(r_1_x)] - P_0[int(r_1_y)+1, int(r_1_x)])

    scale = np.sqrt(delta_v_x**2 + delta_v_y**2)*10
    v_1_x += delta_v_x/scale
    v_1_y += delta_v_y/scale

    r_1_x += v_1_x * dt
    r_1_y += v_1_y * dt

    if r_1_x > 998: r_1_x = 998
    if r_1_x < 1: r_1_x = 1
    if r_1_y > 998: r_1_y = 998
    if r_1_y < 1: r_1_y = 1

    r_1_tr_x.append(r_1_x)
    r_1_tr_y.append(r_1_y)

fig, ax = plt.subplots()
im = ax.matshow(P_0)
ax.plot(r_0_tr_x, r_0_tr_y, c="r", alpha=0.7, label="no mem")
ax.plot(r_1_tr_x, r_1_tr_y, c="b", alpha=0.7, label="mem")
ax.legend()
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig.colorbar(im, cax=cax)


plt.show()
"""

# 4.2
from swarmy.experiment import Experiment
exp1 = Experiment()

exp1.run(rendering=1, swarm_size=20, controller="cluster", track=False)

import numpy as np
from scipy.special import factorial
import matplotlib
import matplotlib.pyplot as plt
from joblib import Parallel, delayed


# for interactive plots
matplotlib.use('QtAgg')


# 3.1
timesteps = np.arange(0, 3.00000001, 0.01)

b = 0.05
x = np.zeros(timesteps.shape)
y = np.zeros(timesteps.shape)
phi = np.zeros(timesteps.shape)

# a)
for i, t in enumerate(timesteps):
    if t < 1:
        v_r = 1
        v_l = 0.9
    else:
        v_r = 0.9
        v_l = 1

    if i == 0:
        phi[i] = 0
        x[i] = 0
        y[i] = 0
    else:
        x[i] = 1/100 * ((v_r + v_l) / 2) * np.cos(phi[i - 1]) + x[i - 1]
        y[i] = 1/100 * ((v_r + v_l) / 2) * np.sin(phi[i - 1]) + y[i - 1]
        phi[i] = 1/100 * (v_r - v_l) / b + phi[i - 1]  # todo change back order

# b)
error_l = 0.01

x_plus = np.zeros(timesteps.shape)
y_plus = np.zeros(timesteps.shape)
phi_plus = np.zeros(timesteps.shape)

x_minus = np.zeros(timesteps.shape)
y_minus = np.zeros(timesteps.shape)
phi_minus = np.zeros(timesteps.shape)

for i, t in enumerate(timesteps):
    if t < 1:
        v_r = 1
        v_l = 0.9
    else:
        v_r = 0.9
        v_l = 1

    if i == 0:
        phi_plus[i] = 0
        x_plus[i] = 0
        y_plus[i] = 0
        phi_minus[i] = 0
        x_minus[i] = 0
        y_minus[i] = 0
    else:
        if t < 1:
            phi_plus[i] = phi_plus[0] + (v_r - (v_l + error_l)) * t / b
            x_plus[i] = x_plus[0] + ((b * (v_r + (v_l + error_l))) / (2 * (v_r - (v_l + error_l)))) * (np.sin((v_r - (v_l + error_l)) * t / b + phi_plus[0]) - np.sin(phi_plus[0]))
            y_plus[i] = y_plus[0] - ((b * (v_r + (v_l + error_l))) / (2 * (v_r - (v_l + error_l)))) * (np.cos((v_r - (v_l + error_l)) * t / b + phi_plus[0]) - np.cos(phi_plus[0]))

            phi_minus[i] = phi_minus[0] + (v_r - (v_l - error_l)) * t / b
            x_minus[i] = x_minus[0] + ((b * (v_r + (v_l - error_l))) / (2 * (v_r - (v_l - error_l)))) * (np.sin((v_r - (v_l - error_l)) * t / b + phi_minus[0]) - np.sin(phi_minus[0]))
            y_minus[i] = y_minus[0] - ((b * (v_r + (v_l - error_l))) / (2 * (v_r - (v_l - error_l)))) * (np.cos((v_r - (v_l - error_l)) * t / b + phi_minus[0]) - np.cos(phi_minus[0]))
        else:
            t_tmp = t - 1
            phi_plus[i] = phi_plus[99] + (v_r - (v_l + error_l)) * t_tmp / b
            x_plus[i] = x_plus[99] + ((b * (v_r + (v_l + error_l))) / (2 * (v_r - (v_l + error_l)))) * (
                        np.sin((v_r - (v_l + error_l)) * t_tmp / b + phi_plus[99]) - np.sin(phi_plus[99]))
            y_plus[i] = y_plus[99] - ((b * (v_r + (v_l + error_l))) / (2 * (v_r - (v_l + error_l)))) * (
                        np.cos((v_r - (v_l + error_l)) * t_tmp / b + phi_plus[99]) - np.cos(phi_plus[99]))

            phi_minus[i] = phi_minus[99] + (v_r - (v_l - error_l)) * t_tmp / b
            x_minus[i] = x_minus[99] + ((b * (v_r + (v_l - error_l))) / (2 * (v_r - (v_l - error_l)))) * (
                        np.sin((v_r - (v_l - error_l)) * t_tmp / b + phi_minus[99]) - np.sin(phi_minus[99]))
            y_minus[i] = y_minus[99] - ((b * (v_r + (v_l - error_l))) / (2 * (v_r - (v_l - error_l)))) * (
                        np.cos((v_r - (v_l - error_l)) * t_tmp / b + phi_minus[99]) - np.cos(phi_minus[99]))


# c)
plt.figure()
plt.plot(x, y, label="no noise")
plt.plot(x_plus, y_plus, label="+ 0.1")
plt.plot(x_minus, y_minus, label="- 0.1")
plt.legend()


plt.figure()
plt.plot(timesteps, phi, label="no noise")
plt.plot(timesteps, phi_plus, label="+ 0.1")
plt.plot(timesteps, phi_minus, label="- 0.1")
plt.legend()

# final thoughts
# a) add a scaling term to scale it into m/s and rad/s that it looks better
# b) calculate 2 trajectories because the formulas does not account for changing motor conditions
plt.show()

# 3.2
from swarmy.experiment import Experiment

# a)
# exp1 = Experiment()
#
# exp1.run(rendering=1, swarm_size=1, controller="avoid")

# b)
# exp2 = Experiment()
#
# exp2.run(rendering=1, swarm_size=1, controller="wall_follow", track=False)

# c)
# exp3 = Experiment()
#
# exp3.run(rendering=1, swarm_size=1, controller="clean", track=True)


# d)
# show me what you got

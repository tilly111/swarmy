import numpy as np
import pandas as pd
import random
from scipy.special import factorial
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from joblib import Parallel, delayed


# for interactive plots
matplotlib.use('QtAgg')

# for reproducability
np.random.seed(42)

b = 0.7
s = 1
def simulate_needle(b, s):
    pos = np.random.rand()
    angle = np.random.rand() * 2 * np.pi

    if pos + np.cos(angle) * b <= 0 or pos + np.cos(angle) * b >= s:
        return 1
    else:
        return 0

# # 5.1.a)
# P = 0
# trials = 10000000
# for _ in range(trials):
#     P += simulate_needle(b, s)
# P = P / trials
#
# print(f"estimation of pi: {2 * b / (s * P):.4f}")

# 5.1.b)
# n = np.arange(10, 1001, 10)
# trials = 10000
#
# res = np.zeros((trials, n.shape[0]))
#
# for it, n_it in enumerate(n):  # run for different settings of n
#     for j in range(trials):  # repeat each setting trials times
#         # experiment flip the needle n times
#         p = 0
#         for i in range(n_it):
#             p += simulate_needle(b, s)
#         # store result
#         res[j, it] = p / n_it
#     print(f"n={n_it} done...")
#
# plt.figure()
# plt.boxplot(res)
#
# plt.show()

# 5.1.c)
# n = np.arange(1, 101, 1)
# trials = 10000
# p = np.zeros(n.shape)
# bpci_plus = np.zeros(n.shape)
# bpci_minus = np.zeros(n.shape)
#
# for it, n_it in enumerate(n):
#     p_trial = 0
#     for j in range(trials):
#         p_tmp = 0
#         for i in range(n_it):
#             p_tmp += simulate_needle(b, s)
#         p_trial += p_tmp / n_it
#     p[it] = p_trial / trials
#     bpci_plus[it] = p[it] + 1.96 * np.sqrt(1 / n_it * p[it] * (1 - p[it]))
#     bpci_minus[it] = p[it] - 1.96 * np.sqrt(1 / n_it * p[it] * (1 - p[it]))
#
#
# plt.figure()
# plt.plot(n, p, label="p")
# plt.plot(n, bpci_plus, color="orange", label="bin-prop conf interval")  #  label="bin-prop conf interval +",
# plt.plot(n, bpci_minus, color="orange")  # label="bin-prop conf interval -",
# plt.fill_between(n, bpci_plus, bpci_minus, alpha=0.2, color="orange")
# # cut of at 0 because it is a probability
# plt.ylim([0, 1.5])
#
# plt.legend()
# plt.show()

# 5.1.d)
# n = np.arange(1, 101, 1)
# p_true = 2 * b / (s * np.pi)
# trials = 10000
#
# experiment_outside = np.zeros(n.shape)
#
# for it, n_it in enumerate(n):
#     # p_trial = 0
#     for j in range(trials):
#         p_tmp = 0
#         for i in range(n_it):
#             p_tmp += simulate_needle(b, s)
#         p_tmp = p_tmp / n_it
#         upper_lim = p_tmp + 1.96 * np.sqrt(1 / n_it * p_tmp * (1 - p_tmp))
#         lower_lim = p_tmp - 1.96 * np.sqrt(1 / n_it * p_tmp * (1 - p_tmp))
#
#         if p_true <= lower_lim or p_true >= upper_lim:
#             experiment_outside[it] += 1
#     print(f"n={n_it} done...")
#
# plt.figure()
# plt.plot(n, experiment_outside/trials)
# plt.xlabel("n")
# plt.ylabel("experiments outside the confidence interval [%]")
# plt.show()

# 5.2
# N = np.arange(2, 201, 1)
# R = np.arange(0.02, 0.51, 0.01)
# trials = 1000
# means = np.zeros((N.shape[0], R.shape[0], trials))
# stds = np.zeros((N.shape[0], R.shape[0], trials))
#
# for n_it, n in enumerate(N):
#     for r_it, r in enumerate(R):
#         for j in range(trials):
#             # do experiment for each setting
#             x_pos = np.random.random((n,))
#             y_pos = np.random.random((n,))
#             rob_color = np.random.randint(0, 2, size=(n,))  # 0 = white, 1 = black
#             estimations = []
#             # run through all robots
#             for rob in range(n):
#                 all_counter = 0
#                 black_counter = 0
#                 # check all other robots including itself
#                 for other_rob in range(n):
#                     if np.sqrt((x_pos[rob] - x_pos[other_rob]) ** 2 + (y_pos[rob] - y_pos[other_rob]) ** 2) <= r:  # robot in communication range
#                         all_counter += 1
#                         if rob_color[other_rob] == 1:  # neighboring robot is committed to black
#                             black_counter += 1
#                 estimate = black_counter/all_counter  # should never be 0 because we account our selves
#                 estimations.append(estimate)
#             means[n_it, r_it, j] = np.mean(estimations)
#             stds[n_it, r_it, j] = np.std(estimations)
#     print(f"n={n} done...")
#
# with open("plots/task_sheet_05/means.npy", "wb") as f:
#     np.save(f, means)
#
# with open("plots/task_sheet_05/stds.npy", "wb") as f:
#     np.save(f, stds)



# R = 49, 1
# plt.figure()
# mean_to_plot = np.mean(means[:, 2, :], axis=1)
# plt.plot(N, mean_to_plot, label=f"r={R[2]}")
# mean_to_plot = np.mean(means[:, 24, :], axis=1)
# plt.plot(N, mean_to_plot, label=f"r={R[24]}")
# mean_to_plot = np.mean(means[:, 48, :], axis=1)
# plt.plot(N, mean_to_plot, label=f"r={R[48]}")
# plt.xlabel("swarm size N")
# plt.ylabel("mean of estimated black robots")
# plt.legend()
# plt.show()

data = pd.read_csv("plots/task_sheet_05/test.csv")

# print(data)
keys = data.columns.tolist()

plt.figure()
interesting_data = data[data[keys[0]] == 0.02]
plt.plot(interesting_data[keys[1]], interesting_data[keys[2]], label=f"mean with r={interesting_data[keys[0]][0]}", color='b')
plt.fill_between(interesting_data[keys[1]], interesting_data[keys[2]]-interesting_data[keys[3]], interesting_data[keys[2]]+interesting_data[keys[3]], alpha=0.2, color='b', label=f"std r={interesting_data[keys[0]][0]}")
interesting_data = data[data[keys[0]] == 0.24]
plt.plot(interesting_data[keys[1]], interesting_data[keys[2]], label=f"mean with r={interesting_data[keys[0]].to_numpy()[0]}", color='orange')
plt.fill_between(interesting_data[keys[1]], interesting_data[keys[2]]-interesting_data[keys[3]], interesting_data[keys[2]]+interesting_data[keys[3]], alpha=0.2, color='orange', label=f"std r={interesting_data[keys[0]].to_numpy()[0]}")
interesting_data = data[data[keys[0]] == 0.5]
plt.plot(interesting_data[keys[1]], interesting_data[keys[2]], label=f"mean with r={interesting_data[keys[0]].to_numpy()[0]}", color='green')
plt.fill_between(interesting_data[keys[1]], interesting_data[keys[2]]-interesting_data[keys[3]], interesting_data[keys[2]]+interesting_data[keys[3]], alpha=0.2, color='green', label=f"std r={interesting_data[keys[0]].to_numpy()[0]}")
plt.plot(interesting_data[keys[1]], np.ones((interesting_data[keys[1]].to_numpy().shape)) * 0.5, label="ground truth", color='red')

plt.legend()
plt.show()



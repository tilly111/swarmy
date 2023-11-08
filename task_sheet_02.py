import numpy as np
from scipy.special import factorial
import matplotlib
import matplotlib.pyplot as plt
from joblib import Parallel, delayed


# for interactive plots
matplotlib.use('QtAgg')
# np.random.seed(42)

# implementing the simulation
def sim_firefly(r=0):
    N = 150  # swarm size
    L = 50  # cycle length

    # generate neighborhood
    adj_matrix = np.zeros((N, N))
    pos = np.random.rand(N, 2)  # robot x pos
    for i in range(N):
        for j in range(N):
            if not (i == j):  # do not count yourself
                if np.linalg.norm(pos[i, :]-pos[j, :], ord=2) <= r:
                    adj_matrix[i, j] = 1

    # counter of cycles
    counter = np.random.randint(0, high=L, size=(N,))

    res = np.zeros((1, 5000))
    counter_res = np.zeros((1, 5000))

    for t in range(5000):
        idx = np.random.permutation(N)  # shuffle execution order
        for i in idx:
            if counter[i] == 25:  # first step after starting to flash
                flash_neigh = len(np.where(counter[np.where(adj_matrix[i, :].astype(int) == 1)] >= 25)[0])
                if flash_neigh > np.sum(adj_matrix[i, :]) / 2:
                    counter[i] += 1
            if counter[i] > 24:  # flashing
                res[0, t] += 1
            else:  # not flashing
                counter_res[0, t] += 1
            counter[i] += 1

            counter[i] = counter[i] % L

    return res  #, counter_res





# a)

r_all = [0.05, 0.1, 0.5, 1.4]

# generate population
pos = np.random.rand(150, 2)  # robot x pos
# counter = np.random.randint(0, high=L, size=(N,))

adj_matrix = np.zeros((len(r_all), 150, 150))

neighbors = np.zeros((len(r_all),))
for count, r in enumerate(r_all):
    for i in range(150):
        for j in range(150):
            if not (i == j):  # do not count yourself
                if np.linalg.norm(pos[i, :]-pos[j, :], ord=2) <= r:
                    neighbors[count] += 1
                    adj_matrix[count, i, j] = 1

neighbors = neighbors / 150

plt.figure()
plt.plot(r_all, neighbors)
plt.xlabel("communication range")
plt.ylabel("average number of neighbours")

res = np.zeros((len(r_all), 5000))
counter_res = np.zeros((len(r_all), 5000))

for count, r in enumerate(r_all):  # run through all settings
    # res[count, :], counter_res[count, :] = sim_firefly(r)
    res[count, :] = sim_firefly(r)

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(range(5000), res[0, :], label="r = 0.05")
axs[0, 0].set_ylim([-5, 160])
axs[0, 0].set_xlabel("Time in discretesteps")
axs[0, 0].set_ylabel("Number of flashing fireflies")
axs[0, 0].set_title("r = 0.05")

axs[0, 1].plot(range(5000), res[1, :], label="r = 0.1")
axs[0, 1].set_ylim([-5, 160])
axs[0, 1].set_xlabel("Time in discretesteps")
axs[0, 1].set_ylabel("Number of flashing fireflies")
axs[0, 1].set_title("r = 0.1")

axs[1, 0].plot(range(5000), res[2, :], label="r = 0.5")
axs[1, 0].set_ylim([-5, 160])
axs[1, 0].set_xlabel("Time in discretesteps")
axs[1, 0].set_ylabel("Number of flashing fireflies")
axs[1, 0].set_title("r = 0.5")

axs[1, 1].plot(range(5000), res[3, :], label="r = 1.4")
axs[1, 1].set_ylim([-5, 160])
axs[1, 1].set_xlabel("Time in discretesteps")
axs[1, 1].set_ylabel("Number of flashing fireflies")
axs[1, 1].set_title("r = 1.4")


# plt.figure()
# plt.plot(res[1, :] + counter_res[1, :])

# b)

# sims = 50
# r_all = np.arange(0.025, 1.41, 0.025)
#
#
# res_b = np.zeros((len(r_all), sims, 5000))
# counter_res_b = np.zeros((len(r_all), sims, 5000))
#
# for count, r in enumerate(r_all):
#     # for s in range(sims):
#     #     res_b[count, s, :], counter_res_b[count, s, :] = sim_firefly(N, L, None, r=r)
#     ret = Parallel(n_jobs=10)(delayed(sim_firefly)(r=r) for _ in range(sims))
#     res_b[count, :, :] = np.concatenate(ret, axis=0)
#     print(f"communciation range {r} simulation done...")
#     # print(len(ret[0][0][0]))
#
#
#
# res_b_2 = res_b[:, :, 4950:]
#
# res_b_2_min = np.min(res_b_2, axis=2)
# res_b_2_max = np.max(res_b_2, axis=2)
#
# print(res_b_2.shape)
# print(res_b_2_min.shape)
# print(res_b_2_max.shape)
#
# res_b_3 = np.mean(res_b_2_max - res_b_2_min, axis=1)
#
# print("res 3 shape", res_b_3.shape)
#
# plt.figure()
# plt.plot(r_all, res_b_3)
# plt.xlabel("communication range")
# plt.ylabel("amplitude")



plt.show()

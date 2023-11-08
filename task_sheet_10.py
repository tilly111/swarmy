import numpy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# for interactive plots
matplotlib.use('QtAgg')


## taken from 7.1
C = 0.5
mov_speed = 0.01
r = 0.045
P_switch = 0.15
N = 50
T = 120


def locust_sim():
    # initialize locusts
    locusts = np.random.random((N,)) * C
    mov_left = np.random.randint(0, 2, (N,))
    # run = np.zeros((T,))
    delta_sum = np.zeros((N+1,))
    delta_sum_counter = np.zeros((N+1,))

    # run sim
    for ts in range(T):
        # shuffle the execution of locuts
        idx = np.random.permutation(N)
        # compute heading of all locusts
        for i in idx:
            # decision on direction
            if np.random.rand() < P_switch:
                mov_left[i] = np.mod(mov_left[i] + 1, 2)
                # switch[ts] += 1
            else:
                counter = 0
                left_goers = 0
                for j in range(N):
                    if not (j == i):  # filter out yourself
                        if np.abs(locusts[j] - locusts[i]) < r:  # in communication range
                            counter += 1
                            left_goers += mov_left[j]
                # check new state
                if counter/2 < left_goers:
                    # if mov_left[i] == 0:
                    #     switch[ts] += 1
                    mov_left[i] = 1
                else:
                    # if mov_left[i] == 1:
                    #     switch[ts] += 1
                    mov_left[i] = 0
        # update movement
        for i in range(N):
            if mov_left[i] == 1:
                locusts[i] = np.mod(locusts[i] - mov_speed, C)
            else:
                locusts[i] = np.mod(locusts[i] + mov_speed, C)

        l_t = np.sum(mov_left)
        if ts >= 100:  # track for 101 till 120
            delta_sum[int(l_t_m1)] += l_t - l_t_m1
            delta_sum_counter[int(l_t_m1)] += 1
        l_t_m1 = l_t

    return delta_sum, delta_sum_counter


# total_delta_sum = np.zeros((N+1,))
# total_delta_sum_counter = np.zeros((N+1,))
#
# TOTAL_NUMBER_OF_RUNS = 50000
# for i in range(TOTAL_NUMBER_OF_RUNS):
#     tmp_delta_sum, tmp_delta_sum_counter = locust_sim()
#     total_delta_sum = total_delta_sum + tmp_delta_sum
#     total_delta_sum_counter = total_delta_sum_counter + tmp_delta_sum_counter
#
#     if i % 100 == 0:
#         print(f"finished run {i}...")
#
# np.save("measurements/10_total_delta_sum_" + str(TOTAL_NUMBER_OF_RUNS) + ".npy", total_delta_sum)
# np.save("measurements/10_total_delta_sum_counter_" + str(TOTAL_NUMBER_OF_RUNS) + ".npy", total_delta_sum_counter)


d = np.load("measurements/10_total_delta_sum_50000.npy")
d2 = np.load("measurements/10_total_delta_sum_counter_50000.npy")

delta_l = d/d2





'''
a) What is the meaning: it is a saddle point 
in average the number of leftgoers does not change -> neither positive nor negative feedback
'''

phi = 0.1  # range 0 to 1
c = 0.001
L = np.arange(0, 51, 1)



def delta_s(xdata, phi, c):
    s = xdata / N
    P_fb = phi * np.sin(np.pi * s)
    return 4 * c * (P_fb - 1/2) * (s - 1/2)


popt, pcov = curve_fit(delta_s, L, delta_l, bounds=([0, -10], [1, 10]))

delta_s_plot = delta_s(L, *popt)
P_fb_plot = popt[0] * np.sin(np.pi * L/N)

print(popt)

plt.figure()
plt.scatter(L, delta_l, label="delta l")
# plt.plot(P_fb_plot, label="positive feedback")
plt.plot(delta_s_plot, label="delta s")
plt.legend()

plt.figure()
plt.plot(P_fb_plot, label="positive feedback")
plt.hlines(0.5, xmin=0, xmax=51, colors="r", alpha=0.7)
plt.legend()

plt.show()
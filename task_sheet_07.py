import numpy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# for interactive plots
matplotlib.use('QtAgg')


## 7.1
C = 1
mov_speed = 0.001
r = 0.045
P_switch = 0.015
# N = 20
# T = 500
# A = np.zeros((N+1, N+1))  # runs x time steps
# M = np.zeros((N+1,))
#
# def locust_sim():
#     # initialize locusts
#     locusts = np.random.random((N,)) * C
#     mov_left = np.random.randint(0, 2, (N,))
#     run = np.zeros((T,))
#     #switch = np.zeros((T,))
#
#     # run sim
#     for ts in range(T):
#         # shuffle the execution of locuts
#         idx = np.random.permutation(N)
#         # compute heading of all locusts
#         for i in idx:
#             # decision on direction
#             if np.random.rand() < P_switch:
#                 mov_left[i] = np.mod(mov_left[i] + 1, 2)
#                 # switch[ts] += 1
#             else:
#                 counter = 0
#                 left_goers = 0
#                 for j in range(N):
#                     if not (j == i):  # filter out yourself
#                         if np.abs(locusts[j] - locusts[i]) < r:  # in communication range
#                             counter += 1
#                             left_goers += mov_left[j]
#                 # check new state
#                 if counter/2 < left_goers:
#                     # if mov_left[i] == 0:
#                     #     switch[ts] += 1
#                     mov_left[i] = 1
#                 else:
#                     # if mov_left[i] == 1:
#                     #     switch[ts] += 1
#                     mov_left[i] = 0
#         # update movement
#         for i in range(N):
#             if mov_left[i] == 1:
#                 locusts[i] = np.mod(locusts[i] - mov_speed, C)
#             else:
#                 locusts[i] = np.mod(locusts[i] + mov_speed, C)
#
#         run[ts] = np.sum(mov_left)
#         if ts > 0:
#             M[int(run[ts - 1])] += 1
#             A[int(run[ts - 1]), int(run[ts])] += 1
#
#     return run


# 7.1. a)
# res = locust_sim()
#
# plt.figure()
# plt.plot(res)
# plt.show()

# 7.1. b) and c)
# for k in range(1000):
#     _ = locust_sim()
#     #switchers[k, :] = switches
#     print(f"finished run {k}")
# # switchers = np.sum(switchers, axis=1)
# for g in range(N+1):
#     if M[g] == 0:
#         A[g, :] = A[g, :] / 1
#     else:
#         A[g, :] = A[g, :] / M[g]
# plt.figure()
# # plt.hist(switchers, bins=500)
# plt.imshow(A)
# plt.colorbar()
# # plt.show()
# np.save("plots/task_sheet_07/P.npy", A)


#
# P = np.load("plots/task_sheet_07/P.npy")
#
# leftis = np.zeros((500,))
# leftis[0] = np.random.randint(0, 21)
#
# for t in range(499):
#     leftis[t+1] = np.random.choice(numpy.arange(0, 21), p=P[int(leftis[t]), :])
#
# plt.figure()
# plt.plot(leftis)
# plt.show()


# 7.2
# T = 5000
# N = np.arange(20, 30, 1)  # 151
#
# def locust_sim_2(n, switch_to_A_counter, switch_to_C_counter):
#     # initialize locusts
#     locusts = np.random.random((n,)) * C
#     mov_left = np.random.randint(0, 2, (n,))
#     run = np.zeros((T,))
#     tmp_counter = 0
#     state = None
#
#     # run sim
#     for ts in range(T):
#         # shuffle the execution of locuts
#         idx = np.random.permutation(n)
#         # compute heading of all locusts
#         for i in idx:
#             # decision on direction
#             if np.random.rand() < P_switch:
#                 mov_left[i] = np.mod(mov_left[i] + 1, 2)
#             else:
#                 counter = 0
#                 left_goers = 0
#                 for j in range(n):
#                     if not (j == i):  # filter out yourself
#                         if np.abs(locusts[j] - locusts[i]) < r:  # in communication range
#                             counter += 1
#                             left_goers += mov_left[j]
#                 if counter/2 < left_goers:
#                     mov_left[i] = 1
#                 else:
#                     mov_left[i] = 0
#         # update movement
#         for i in range(n):
#             if mov_left[i] == 1:
#                 locusts[i] = np.mod(locusts[i] - mov_speed, C)
#             else:
#                 locusts[i] = np.mod(locusts[i] + mov_speed, C)
#
#         run[ts] = np.sum(mov_left)
#         if state is None:
#             if run[ts] > 0.7*n:
#                 state = "A"
#             elif run[ts] < 0.3*n:
#                 state = "C"
#             else:
#                 state = "B"
#         else:
#             if state == "A":
#                 if run[ts] > 0.7*n:
#                     tmp_counter = 0
#                 elif run[ts] < 0.3*n:
#                     switching_time_to_C.append(tmp_counter)
#                     tmp_counter = 0
#                     switch_to_C_counter += 1
#                     state = "C"
#                 else:
#                     tmp_counter += 1
#             elif state == "C":
#                 if run[ts] < 0.3*n:
#                     tmp_counter = 0
#                 elif run[ts] > 0.7*n:
#                     switching_time_to_A.append(tmp_counter)
#                     tmp_counter = 0
#                     switch_to_A_counter += 1
#                     state = "A"
#                 else:
#                     tmp_counter += 1
#             elif state == "B":
#                 tmp_counter += 1
#             else:
#                 print("wrong state!")
#
#     return switch_to_A_counter, switch_to_C_counter
#
# switching_time_to_A = []
# switching_time_to_C = []
# switch_to_A_counter = 0
# switch_to_C_counter = 0
#
# switch_to_A_total = np.zeros(N.shape)
# switch_to_C_total = np.zeros(N.shape)
#
# switching_time_to_A_total = np.zeros(N.shape)
# switching_time_to_C_total = np.zeros(N.shape)
#
# for ii, ni in enumerate(N):
#     for _ in range(100):
#         switch_to_A_counter, switch_to_C_counter = locust_sim_2(ni, switch_to_A_counter, switch_to_C_counter)
#     switch_to_A_total[ii] = switch_to_A_counter
#     switch_to_C_total[ii] = switch_to_C_counter
#     switching_time_to_A_total[ii] = np.mean(switching_time_to_A)
#     switching_time_to_C_total[ii] = np.mean(switching_time_to_C)
#
#     switching_time_to_A = []
#     switching_time_to_C = []
#     switch_to_A_counter = 0
#     switch_to_C_counter = 0
#
#     print(f"done with {ni} robots...")

data = pd.read_csv("measurements/72.csv")

N = data["swarm_size"].to_numpy()
# print(data)
# print(data.columns.tolist())
switch_to_A_total = data["total_switches_a"].to_numpy()
switch_to_C_total = data["total_switches_c"].to_numpy()
avg_switching_time_a = data["avg_switching_time_a"].to_numpy()
avg_switching_time_c = data["avg_switching_time_c"].to_numpy()


plt.figure()
plt.plot(N, switch_to_A_total + switch_to_C_total, label="total switches")
# plt.plot(N, switch_to_C_total, label="switches to C")
plt.legend()

plt.figure()
plt.plot(N, (avg_switching_time_a + avg_switching_time_c)/2, label="mean switching time")
# plt.plot(N, avg_switching_time_c)
plt.legend()
plt.show()








import numpy as np
from scipy.special import factorial
import matplotlib
import matplotlib.pyplot as plt


# for interactive plots
matplotlib.use('QtAgg')


# task 1 a
# lambda = alpha
i = np.linspace(0, 10, 100)

lam = np.ones(i.shape) * 0.01
alpha_001 = (np.exp(-lam) * np.power(lam, i)) / (factorial(i))
lam = np.ones(i.shape) * 0.1
alpha_01 = (np.exp(-lam) * np.power(lam, i)) / (factorial(i))
lam = np.ones(i.shape) * 0.5
alpha_05 = (np.exp(-lam) * np.power(lam, i)) / (factorial(i))
lam = np.ones(i.shape) * 1
alpha_1 = (np.exp(-lam) * np.power(lam, i)) / (factorial(i))





fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(i, alpha_001)
axs[0, 0].set_title(r"$\alpha$ = 0.01")
axs[0, 0].set_xlabel("Time in discrete units")
axs[0, 0].set_ylabel("Incoming jobs")
axs[0, 0].set_ylim([0, 1])

axs[0, 1].plot(i, alpha_01)
axs[0, 1].set_title(r"$\alpha$ = 0.1")
axs[0, 1].set_xlabel("Time in discrete units")
axs[0, 1].set_ylabel("Incoming jobs")
axs[0, 1].set_ylim([0, 1])

axs[1, 0].plot(i, alpha_05)
axs[1, 0].set_title(r"$\alpha$ = 0.5")
axs[1, 0].set_xlabel("Time in discrete units")
axs[1, 0].set_ylabel("Incoming jobs")
axs[1, 0].set_ylim([0, 1])

axs[1, 1].plot(i, alpha_1)
axs[1, 1].set_title(r"$\alpha$ = 1")
axs[1, 1].set_xlabel("Time in discrete units")
axs[1, 1].set_ylabel("Incoming jobs")
axs[1, 1].set_ylim([0, 1])


# task 1 b
alpha_001 = np.random.poisson(lam=0.01, size=100000)
alpha_01 = np.random.poisson(lam=0.1, size=100000)
alpha_05 = np.random.poisson(lam=0.5, size=100000)
alpha_1 = np.random.poisson(lam=1, size=100000)

fig, axs = plt.subplots(2, 2)

axs[0, 0].hist(alpha_001, bins=100)
axs[0, 0].set_title(r"$\alpha$ = 0.01")
axs[0, 0].set_xlabel("Time in discrete units")
axs[0, 0].set_ylabel("Incoming jobs")
axs[0, 0].set_ylim([0, 100000])
axs[0, 0].set_xlim([-0.5, 8])

axs[0, 1].hist(alpha_01, bins=100)
axs[0, 1].set_title(r"$\alpha$ = 0.1")
axs[0, 1].set_xlabel("Time in discrete units")
axs[0, 1].set_ylabel("Incoming jobs")
axs[0, 1].set_ylim([0, 100000])
axs[0, 1].set_xlim([-0.5, 8])

axs[1, 0].hist(alpha_05, bins=100)
axs[1, 0].set_title(r"$\alpha$ = 0.5")
axs[1, 0].set_xlabel("Time in discrete units")
axs[1, 0].set_ylabel("Incoming jobs")
axs[1, 0].set_ylim([0, 100000])
axs[1, 0].set_xlim([-0.5, 8])

axs[1, 1].hist(alpha_1, bins=100)
axs[1, 1].set_title(r"$\alpha$ = 1")
axs[1, 1].set_xlabel("Time in discrete units")
axs[1, 1].set_ylabel("Incoming jobs")
axs[1, 1].set_ylim([0, 100000])
axs[1, 1].set_xlim([-0.5, 8])


# task 1 c
alpha = 0.1
queue_length_ts = []
queue_length = 0
job_processing_time = 4
job_processing_counter = 0
for ts in range(2000):  # run for 2000 time steps
    # check how many jobs come in this time step
    num_jobs = np.random.poisson(lam=alpha, size=1)
    queue_length += num_jobs[0]
    # process some jobs
    if queue_length > 0:  # there is a job
        if job_processing_counter < job_processing_time:  # this job needs to process
            job_processing_counter += 1
        else:  # job finished processing
            job_processing_counter = 0
            queue_length -= 1
    else:  # no jobs in queue run empty cycle
        pass
    queue_length_ts.append(queue_length)

plt.figure()
plt.plot(queue_length_ts)
plt.title("Task 1 c)")
plt.xlabel("Time in discrete steps")
plt.ylabel("Queue length")
print(f"Mean queue length: {np.mean(queue_length_ts)} time steps")


# task 1 d
def queue_experiment(alpha, job_processing_time):
    queue_length_ts = []
    queue_length = 0
    job_processing_counter = 0
    for ts in range(2000):  # run for 2000 time steps
        # check how many jobs come in this time step
        num_jobs = np.random.poisson(lam=alpha, size=1)
        queue_length += num_jobs[0]
        # process some jobs
        if queue_length > 0:  # there is a job
            if job_processing_counter < job_processing_time:  # this job needs to process
                job_processing_counter += 1
            else:  # job finished processing
                job_processing_counter = 0
                queue_length -= 1
        else:  # no jobs in queue run empty cycle
            pass
        queue_length_ts.append(queue_length)

    return np.mean(queue_length_ts)

samples = 200
job_processing_time = 4
alpha = np.arange(0.005, 0.255, 0.005)
mean_queue_time = np.zeros(alpha.shape)
for count, a in enumerate(alpha):
    print("alpha", a)
    tmp_mean = 0
    for _ in range(samples):
        tmp_mean += queue_experiment(a, job_processing_time)
    mean_queue_time[count] = tmp_mean / samples

plt.figure()
plt.plot(alpha, mean_queue_time)
plt.title("Task 1 d)")
plt.xlabel(r"$\alpha$")
plt.ylabel("Mean queue time in discrete time steps")


# task 1 e
samples = 200
job_processing_time = 2
alpha = np.arange(0.005, 0.505, 0.005)
mean_queue_time = np.zeros(alpha.shape)
for count, a in enumerate(alpha):
    print("alpha", a)
    tmp_mean = 0
    for _ in range(samples):
        tmp_mean += queue_experiment(a, job_processing_time)
    mean_queue_time[count] = tmp_mean / samples

plt.figure()
plt.plot(alpha, mean_queue_time)
plt.title("Task 1 e)")
plt.xlabel(r"$\alpha$")
plt.ylabel("Mean queue time in discrete time steps")

plt.show()
exit(42)
# task 2
from joblib import Parallel, delayed


def experiment(num_robots, samples, quat=False):
    M = 20  # stick sides
    time_steps = 1000
    w_atStick = 7  # stick side waiting time

    pulled_out_sticks_tmp = 0
    for sam in range(samples):  # average over runs
        # initial robots
        rob_pos = np.random.randint(0, M, size=num_robots)
        rob_waiting_time = np.zeros((num_robots,))
        rob_target = np.zeros((num_robots,))
        rob_moving_counter = np.ones((num_robots,)) * (-1)
        rob_state = np.ones((num_robots,))  # 1 = waiting, 0 = moving

        for ts in range(time_steps):
            # permute in which order we process the robots
            idx = np.random.permutation(num_robots)
            # execute each robot
            rob_flag = np.zeros((num_robots,))  # check which robot needs to be computed
            # print("------------------------", ts)
            # print("positions", rob_pos)
            # print("waiting_time", rob_waiting_time)
            # print("target", rob_target)
            # print("moving_counter", rob_moving_counter)
            for rob in idx:
                if rob_flag[rob]:  # robot already calculated
                    continue
                elif np.count_nonzero(rob_pos == rob_pos[rob]) >= 2 and rob_state[rob] == 1 and not rob_pos[rob] == -1:  # we can pull a stick  - rob_moving_counter[rob] == 0 and rob_waiting_time[rob] < w_atStick
                    pulled_out_sticks_tmp += 1
                    # print(f"robot {rob} found stick")
                    # reset all robots
                    # print("np where", np.where(rob_pos == rob_pos[rob])[0])
                    for rob_i in np.where(rob_pos == rob_pos[rob])[0]:
                        # print(f"resetting robot {rob_i}")
                        rob_pos[rob_i] = -1
                        rob_waiting_time[rob_i] = 0
                        rob_target[rob_i] = np.random.randint(0, M)
                        if quat:
                            rob_moving_counter[rob_i] = int(0.12 * num_robots ** 2 + np.random.randint(0, 3))
                        else:
                            rob_moving_counter[rob_i] = num_robots + np.random.randint(0, 3)
                        rob_state[rob_i] = 0
                        rob_flag[rob_i] = 1
                elif rob_moving_counter[rob] > 0 and rob_state[rob] == 0:  # robot is currently moving
                    # print(f"robot {rob} is moving")
                    rob_moving_counter[rob] -= 1
                elif rob_moving_counter[rob] == 0 and rob_state[rob] == 0:  # robot reaches goal
                    # print(f"robot {rob} changes afte moving to {rob_target[rob]}")
                    rob_pos[rob] = rob_target[rob]  # is at new position
                    rob_target[rob] = -1
                    rob_state[rob] = 1  # robot changes in waiting state
                elif rob_waiting_time[rob] < w_atStick and rob_state[rob] == 1:  # robot waits at stick
                    rob_waiting_time[rob] += 1
                elif rob_waiting_time[rob] == w_atStick and rob_state[rob] == 1:  # robot waited to long -> reset robot
                    # print(f"robot {rob} is changing state ...")
                    rob_pos[rob] = -1
                    rob_waiting_time[rob] = 0
                    rob_target[rob] = np.random.randint(0, M)
                    if quat:
                        rob_moving_counter[rob] = int(0.12 * num_robots ** 2 + np.random.randint(0, 3))
                    else:
                        rob_moving_counter[rob] = num_robots + np.random.randint(0, 3)
                    rob_state[rob] = 0
                else:
                    print(f"robot {rob} is in an undefined state!")
                rob_flag[rob] = 1
    print(f"finished robots {num_robots}")
    # print(pulled_out_sticks_tmp)
    pulled_out_sticks_tmp = pulled_out_sticks_tmp / samples
    return pulled_out_sticks_tmp

N = range(2, 21)  # number of robots
samples = 5000

pulled_out_sticks_l = Parallel(n_jobs=10)(delayed(experiment)(num_robots, samples) for num_robots in N)
pulled_out_sticks_l = np.asarray(pulled_out_sticks_l)
pulled_out_sticks_l = pulled_out_sticks_l / pulled_out_sticks_l[0]

pulled_out_sticks_q = Parallel(n_jobs=10)(delayed(experiment)(num_robots, samples, quat=True) for num_robots in N)
pulled_out_sticks_q = np.asarray(pulled_out_sticks_q)
pulled_out_sticks_q = pulled_out_sticks_q / pulled_out_sticks_q[0]


plt.figure()
plt.plot(N, pulled_out_sticks_l, label="normalized linear")
plt.plot(N, pulled_out_sticks_q, label="normalized quadratic")
plt.plot(N, N, linestyle="dashed", color="gray")
plt.title("Task 2")
plt.xlabel(r"# robots")
plt.ylabel("Pulled out sticks")
plt.legend()


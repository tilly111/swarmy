from swarmy.experiment import Experiment

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# for interactive plots
matplotlib.use('QtAgg')


def helper_calc_distance(data, items):
    # calculate inter object distance
    distance = np.zeros((data.shape[0],))
    for t in range(data.shape[0]):  # ts
        for i in range(items):
            for j in range(i):
                distance[t] += np.sqrt((data[t, (i * 2) + 1] - data[t, (j * 2) + 1]) ** 2 + (
                            data[t, (i + 1) * 2] - data[t, (j + 1) * 2]) ** 2)
    return distance


n_items_TOTAL = 40
### selecting controllers
controllers = ["collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent"]

### experiments
exp1 = Experiment()
exp1.run(rendering=1, swarm_size=len(controllers), controllers=controllers, n_items=n_items_TOTAL, save_file_name="no_anti_agents_embodied_03")

controllers = ["collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_agent",
               "collecting_anti_agent"]

exp2 = Experiment()
exp2.run(rendering=1, swarm_size=len(controllers), controllers=controllers, n_items=n_items_TOTAL, save_file_name="1_anti_agent_embodied_03")

with open("measurements/no_anti_agents_embodied_03.npy", 'rb') as f:
    data = np.load(f)

with open("measurements/1_anti_agent_embodied_03.npy", 'rb') as f:
    data_aa = np.load(f)

print(data.shape)

distance = helper_calc_distance(data, n_items_TOTAL)
distance_aa = helper_calc_distance(data_aa, n_items_TOTAL)

plt.figure()
plt.plot(data[:, 0], distance, label="no anti agents")
plt.plot(data_aa[:, 0], distance_aa, label="1 anti agents")
plt.legend()
plt.show()


# print(data_aa)
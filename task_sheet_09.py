import numpy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from swarmy.experiment import Experiment

# for interactive plots
matplotlib.use('QtAgg')


controllers = ["foraging"] * 10
n_items_TOTAL = 40

print(controllers)

### experiments
exp1 = Experiment()
exp1.run(rendering=1, swarm_size=len(controllers), controllers=controllers, n_items=n_items_TOTAL, save_file_name="no_anti_agents_embodied_03")

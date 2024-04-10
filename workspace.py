# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   06/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================

"""
Description:
This module is the workspace for the simulation environment where:
    - paths and directories can be defined
    - experiments can be performed
    - measurement results can be saved
    - results can be evaluated
"""


# %% Experiment: Testing
import yaml
from swarmy.experiment import Experiment

with open ('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

### import your controller and sensors
from controller.aggressive import Aggressive
from controller.fear import Fear
from controller.my_controller import MyController
from Sensors.my_sensors import MySensor
from Sensors.proximitySensor import ProximitySensor
from world.my_world import my_environment
from agent.my_agent import MyAgent




agent_controller = [Aggressive, Fear]
agent_sensing = [MySensor, ProximitySensor]
world = my_environment(config)  #<----- proably not needed

exp1 = Experiment(config, agent_controller, agent_sensing, world, MyAgent)

exp1.run(1)

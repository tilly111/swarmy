# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   06/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
import yaml
from swarmy.experiment import Experiment

# Import your implementation of the controller, sensor, environment and agent
from controller.my_controller import MyController
from sensors.bumper_sensor import BumperSensor
from environment.my_environment import MyEnvironment
from agent.my_agent import MyAgent

# load the configuration file, check the config.yaml file for more information and to change to your needs
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# add your controller, if you have more than one controller, add them to the list and set the share of robots for each controller with controller_ratios in the config.yaml file
controllers = [MyController]
# add your sensors, if you have more than one sensor, add them to the list, all sensors are added to each robot
sensors = [BumperSensor]

experiment = Experiment(config, controllers, sensors, MyEnvironment, MyAgent)

experiment.run(config['rendering'])

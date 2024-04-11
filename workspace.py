# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   06/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
import yaml
from swarmy.experiment import Experiment

### load the configuration file, check the config.yaml file for more information and to change to your needs
with open ('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
## Import uour implementation of the controller, sensor, environment and agent
from controller.my_controller import MyController
from sensors.bumper_sensor import BumperSensor
from world.my_world import My_environment
from agent.my_agent import MyAgent



# add your controller, if you have more than one controller, add them to the list and specify the percentage of robots that should use this controller in the config.yaml file
agent_controller = [MyController]
# add your sensors, if you have more than one sensor, add them to the list all sensors are added to each robot
agent_sensing = [BumperSensor]

exp1 = Experiment(config, agent_controller, agent_sensing, My_environment, MyAgent)

exp1.run(1)

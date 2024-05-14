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
from controller.hill_climber import HillClimber
from sensors.bumper_sensor import BumperSensor
from world.my_world import My_environment
from agent.my_agent import MyAgent
from evolution.evolution import Evolution

# add your controller, if you have more than one controller, add them to the list and specify the percentage of robots that should use this controller in the config.yaml file
agent_controller = [HillClimber]
# add your sensors, if you have more than one sensor, add them to the list all sensors are added to each robot
agent_sensing = [BumperSensor]


""" initialize your evolution object and start the evolution process by initializing the first genome 
    and then run the experiment for each generation, evaluate the fitness of the genome and update the genome.

    One generation could look like this:
    - initialize the experiment with: exp = Experiment(config, agent_controller, agent_sensing, My_environment, MyAgent)
    - initialize the robots with: exp.init_robots()
    - set the control parameters of the robot with: exp.agent_list[0].set_control_params(genome) 
        here, the genome could be a list of floating point values that are used in the controller class
    - run the experiment with: exp.run(config['rendering'])
    - use ecp.agent_list[0].get_evaluation_params() to get the information you need to calculate the the fitness 
    (don't forget to overwrite the get_evaluation_params() function in your agent class to your needs)
    - calculate the fitness and mutate
    - repeat for each generation
"""




evolution = Evolution(config)

exp = Experiment(config, agent_controller, agent_sensing, My_environment, MyAgent)
exp.init_robots()
exp.run(config['rendering'])

from swarmy.agent import Agent
import random
import pygame

class MyAgent(Agent):
    def __init__(self,environment,controller, sensor, config):
        super().__init__(environment,controller, sensor, config)

        self.environment = environment
        self.trajectory = []



    def initial_position(self):
        """
        Define the initial position of the agent.
        Hint:
        Use x,y,gamma = self.set_position(x-position, y-position, heading) to set the position of the agent.
        """
        x = random.randint(0, self.config['world_width'])
        y = random.randint(0, self.config['world_height'])

        gamma = random.randint(0, 360)
        self.actuation.position[0] = x
        self.actuation.position[1] = y
        self.actuation.angle = gamma
        self.set_position(x, y, gamma)


    def save_information(self, last_robot):
        """
        Save information of the agent, e.g. trajectory or the environmental plot.
        Hint:
        - Use pygame.draw.lines() to draw the trajectory of the robot and access the surface of the environment with self.environment.displaySurface
        - pygame allows to save an image of the current environment
        """
        print("Save information not implemented, check my_agent.py")
        """ your implementation here """

        pass








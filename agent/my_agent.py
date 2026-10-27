from swarmy.agent import Agent
import random
import pygame


class MyAgent(Agent):
    def __init__(self, environment, controller, sensors, config):
        super().__init__(environment, controller, sensors, config)

        self.trajectory = []

    def initial_position(self):
        """
        Define the initial position of the agent.
        Hint:
        Use self.set_position(x, y, heading) to set the position of the agent.
        """
        margin = 30  # keep the robot away from the walls
        x = random.randint(margin, self.config['world_width'] - margin)
        y = random.randint(margin, self.config['world_height'] - margin)
        heading = random.randint(0, 359)
        self.set_position(x, y, heading)

    def save_information(self, save_image):
        """
        Save information of the agent, e.g. trajectory or the environmental plot.
        save_image is True only for the last agent, so the shared image is saved once after all agents have drawn on it.
        Hint:
        - Use pygame.draw.lines() to draw the trajectory of the robot and access the surface of the environment with self.environment.display_surface
        - pygame allows to save an image of the current environment
        """
        print('Save information not implemented, check my_agent.py')
        """ your implementation here """

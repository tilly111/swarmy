from swarmy.environment import Environment
import pygame
import numpy as np


class MyEnvironment(Environment):
    def __init__(self, config):
        self.config = config
        super().__init__(config)

        self.light_distribution = self.define_light()

    def add_static_rectangle_object(self):
        """
        Add static rectangle objects to the environment such as walls or obstacles.
        Example:
            self.static_rectangle_list.append([color, pygame.Rect(x, y, width, height), border_width])
        """
        self.static_rectangle_list.append(['BLACK', pygame.Rect(5, 5, self.config['world_width'] - 10, 5), 5])
        self.static_rectangle_list.append(['BLACK', pygame.Rect(5, 5, 5, self.config['world_height'] - 10), 5])
        self.static_rectangle_list.append(['BLACK', pygame.Rect(5, self.config['world_height'] - 10, self.config['world_width'] - 10, 5), 5])
        self.static_rectangle_list.append(['BLACK', pygame.Rect(self.config['world_width'] - 10, 5, 5, self.config['world_height'] - 10), 5])

    def add_static_circle_object(self):
        """
        Add static circle objects to the environment such as sources or sinks.
        Example:
            self.static_circle_list.append([color, position, radius, border_width])
        """
        pass

    def set_background_color(self):
        """
        Set the background color of the environment.
        Example:
            self.display_surface.fill(self.background_color)
        Hint: It is possible to use the light distribution to set the background color.
        For displaying a light distribution you might find pygame.surfarray.make_surface and self.display_surface.blit useful
        """
        self.display_surface.fill(self.background_color)

    ###  LIGHT DISTRIBUTION ###

    def define_light(self):
        """
        Define the light distribution of the environment.
        Returns: 3 dimensional light distribution tuple (x, y, light_intensity)
        """
        """ your implementation here """
        pass

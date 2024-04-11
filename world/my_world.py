from swarmy.environment import Environment
import pygame
import numpy as np

class My_environment(Environment):
    def __init__(self, config):
        self.config = config
        super().__init__(config)

        self.light_dist = self.defineLight()

    def add_static_rectangle_object(self):
        """
        Add static rectangle object to the environment such as walls or obstacles.
        Example:
            self.staticRectList.append(color, pygame.Rect(x, y, width, height), border_width))
        Returns:
        """
        self.staticRectList.append(['BLACK', pygame.Rect(5, 5, self.config['world_width'] - 10, 5),5])
        self.staticRectList.append(['BLACK', pygame.Rect(5, 5, 5, self.config['world_height']-10), 5])
        self.staticRectList.append(['BLACK', pygame.Rect(5, self.config['world_height']-10, self.config['world_width'] - 10,5), 5])
        self.staticRectList.append(['BLACK', pygame.Rect(self.config['world_width'] - 10, 5, 5, self.config['world_height']-10), 5])


    def add_static_circle_object(self):
        """
        Add static circle object to the environment such as sources or sinks.
        Example:
            self.staticCircList.append([color, position, border_width, radius])
        Returns:
        """
        pass



    def set_background_color(self):
        """
        Set the background color of the environment.
        Example:
            self.displaySurface.fill(self.BACKGROUND_COLOR)
        Hint: It is possible to use the light distribution to set the background color.
        For displaying a light destribution you might find pygame.surfarray.make_surface and self.displaySurface.blit usefull)
        Returns:
        """
        self.displaySurface.fill(self.BACKGROUND_COLOR)

    ###  LIGHT DISTRIBUTION ###

    def defineLight(self):
        """
        Define the light distribution of the environment.
        Returns: 3 dimensional light distribution tuple (x,y,light_intensity)

        """
        """ your implementation here"""
        pass


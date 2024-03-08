from swarmy.environment import Environment
import pygame
import numpy as np

class my_environment(Environment):
    def __init__(self, rendering, config):
        self.config = config
        super().__init__(rendering, config)
        #self.add_static_rectangle_object()
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


    def add_dynamic_rectangle_object(self):
        """
        Add dynamic rectangle object to the environment such as moving obstacles.
        Example:
            self.dynamicRectList.append(color, pygame.Rect(x, y, width, height), border_width))
        Returns:
        """
        pass

    def add_static_circle_object(self):
        """
        Add static circle object to the environment such as sources or sinks.
        Example:
            self.staticCircList.append(color, position, border_width, radius)
        Returns:
        """
        pass

    def add_dynamic_circle_object(self):
        """
        Add dynamic circle object to the environment such as moving sources or sinks.
        Example:
            self.dynamicCircList.append(color, position, border_width, radius)
        Returns:
        """
        pass

    def set_background_color(self):
        """
        Set the background color of the environment.
        Example:
            self.displaySurface.fill(self.BACKGROUND_COLOR)
        Returns:
        """
        self.displaySurface.fill(self.BACKGROUND_COLOR)

        #surface = pygame.surfarray.make_surface(self.light_dist)
        #self.displaySurface.blit(surface,(0,0))

        # for displaying a light destribution you might find pygame.surfarray.make_surface and self.displaySurface.blit usefull)



    ###  LIGHT DISTRIBUTION ###

    def defineLight(self):

        center = np.array([self.config['world_width'] / 2, self.config['world_height'] / 2])

        light_dist = np.zeros((self.config['world_width'] , self.config['world_height'], 3))
        for i in range(self.config['world_width'] ):
            for j in range(self.config['world_height']):
                p = np.array([i, j])
                dist = int((1 - np.linalg.norm((center - p) / self.config['world_width'] )) * 255)
                light_dist[i][j][2] = int(dist)
        return light_dist

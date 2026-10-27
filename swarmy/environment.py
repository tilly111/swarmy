# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
This module represents the physical environment.
"""

# =============================================================================
# Imports
# =============================================================================
import pygame
import numpy as np
from abc import ABC, abstractmethod


# =============================================================================
# Class
# =============================================================================
class Environment(ABC):
    """
    The environment object represents the simulation world of an agent.
    It is the testbed where the experiments are conducted.
    The object expects that pygame is already initialized.

    Args:
        config (dict): simulation configuration from config.yaml
    """
    def __init__(self, config):
        """
        Initialize environment object.
        """
        super(Environment, self).__init__()

        # Variables and constants - set screws
        self.fps = config['FPS']
        self.background_color = config['background_color']
        self.width = config['world_width']
        self.height = config['world_height']
        self.config = config

        # list with objects to be plotted
        self.static_rectangle_list = []
        self.static_circle_list = []
        self.dynamic_circle_list = []
        self.dynamic_polygon_list = []
        self.dynamic_line_list = []
        self.dynamic_rectangle_list = []
        self.agent_list = []
        self.agent_object_list = []

        self.clock = pygame.time.Clock()  # create an object to help track time
        self.add_static_rectangle_object()
        self.add_static_circle_object()
        ### SOLUTION LIGHT DISTRIBUTION ###
        # self.light_distribution = np.zeros((self.width, self.height))
        # self.define_light()

    def render_init(self):
        # init basic rendering surface
        if self.config['rendering'] == 1:
            if self.width == pygame.display.Info().current_w and self.height == pygame.display.Info().current_h:   # fullscreen size
                self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:                                                                                                   # size smaller than fullscreen
                self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        elif self.config['rendering'] == -1:
            self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.HIDDEN)                 # no screen
        elif self.config['rendering'] == 0:
            self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)                # borderless window, e.g. to capture images

    @abstractmethod
    def add_static_rectangle_object(self):
        pass

    def add_dynamic_rectangle_object(self, rectangle):
        self.dynamic_rectangle_list.append(rectangle)

    def add_dynamic_line_object(self, line):
        self.dynamic_line_list.append(line)

    @abstractmethod
    def add_static_circle_object(self):
        pass

    def add_dynamic_circle_object(self, circle):
        self.dynamic_circle_list.append(circle)

    @abstractmethod
    def set_background_color(self):
        self.display_surface.fill(self.background_color)

    def get_static_rectangle_list(self):
        return self.static_rectangle_list

    def get_dynamic_rectangle_list(self):
        return self.dynamic_rectangle_list

    def get_static_circle_list(self):
        return self.static_circle_list

    def get_dynamic_circle_list(self):
        return self.dynamic_circle_list

    def get_agent_object(self):
        return self.agent_object_list

    def get_dynamic_line_list(self):
        return self.dynamic_line_list

    """
    def define_light(self):
        center = np.array([self.width / 2, self.height / 2])

        light_distribution = np.zeros((self.width, self.height, 3))
        for i in range(self.width):
            for j in range(self.height):
                p = np.array([i, j])
                dist = int((1 - np.linalg.norm((center - p) / self.width)) * 255)
                light_distribution[i][j][0] = int(dist)
        # test = light_distribution[:, :, 0]
        # test = np.roll(test, +350, axis=1)
        # light_distribution[:, :, 0] = np.roll(test, +350, axis=0)

        self.light_distribution = light_distribution
    """

    # =============================================================================
    # Rendering and Helper functions
    # =============================================================================
    def render(self):
        """
        This method is used to update the environment.
        """
        self.set_background_color()

        # draw static objects (walls, obstacles, sources, sinks)
        for color, rect, width in self.static_rectangle_list:
            pygame.draw.rect(self.display_surface, color, rect, width)

        for color, center, radius, width in self.static_circle_list:
            pygame.draw.circle(self.display_surface, color, center, radius, width)

        # draw dynamic polygons (agents)
        for color, points, width in self.dynamic_polygon_list:
            pygame.draw.polygon(self.display_surface, (255, 255, 255), points)  # fill the polygon
            pygame.draw.polygon(self.display_surface, color, points, width)

        # draw dynamic circles, lines and rectangles (e.g. sensors)
        for color, center, radius, width in self.dynamic_circle_list:
            pygame.draw.circle(self.display_surface, color, center, radius, width)

        for color, start, end in self.dynamic_line_list:
            pygame.draw.line(self.display_surface, color, start, end)

        for color, rect, width in self.dynamic_rectangle_list:
            pygame.draw.rect(self.display_surface, color, rect, width)

        # update content on display and enforce given frames per second
        pygame.display.flip()
        self.force_framerate()

    def reset_dynamic_buffers(self):
        self.dynamic_circle_list = []
        self.dynamic_polygon_list = []
        self.dynamic_line_list = []
        self.dynamic_rectangle_list = []

    def force_framerate(self):
        """
        This method is used once per frame to enforce a fixed number of frames per second.
        It will delay the simulation to get the desired fps.
        """
        self.clock.tick(self.fps)  # every second at most fps frames should pass.
        # self.clock.tick_busy_loop(self.fps)  # more accurate to ensure fps than tick but needs more CPU computation power

# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module represents the body of an agent.
"""

# =============================================================================
# Imports and Variables
# =============================================================================
import math
import numpy as np
import pygame

# Helper variable
poly_rotated_lookup = []  # the table reduces computation steps to improve rendering speed


# =============================================================================
# Class
# =============================================================================
class Body():
    """
    The body is the visual representation of an agent in the simulation.
    The object defines the dimensions and the position of an agent in the environment.

    Args:
        agent (agent.py): instance of the agent
    """
    def __init__(self, agent):
        """
        Initialize body object.
        """
        super(Body, self).__init__()

        # constants
        self.WIDTH = 24                 # agent body width
        self.HEIGHT = 10                # agent body height
        self.COLOR = (0, 90, 90)        # turquoise
        self.BOUNDING = round(np.hypot(self.WIDTH, self.HEIGHT)) + 20

        # variables
        self.agent = agent

        # initial position with agent center in coordinate system origin
        W = self.WIDTH
        H = self.HEIGHT
        wheel_dist = 8          # helper variable to calculate the agent body
        motor_dist = 3          # helper variable to calculate the agent body
        ratio_body_wheel = 6    # helper variable to calculate the agent body
        v1 = pygame.Vector2(-W/ratio_body_wheel/2 - W/2 - wheel_dist, -H*2/2)
        v2 = pygame.Vector2(W/ratio_body_wheel/2 - W/2 - wheel_dist, -H*2/2)
        v3 = pygame.Vector2(W/ratio_body_wheel/2 - W/2 - wheel_dist, -H/2 + motor_dist)
        v4 = pygame.Vector2(-W/2, -H/2 + motor_dist)
        v5 = pygame.Vector2(-W/2, -H/2)
        v6 = pygame.Vector2(W/2, -H/2)
        v7 = pygame.Vector2(W/2, -H/2 + motor_dist)
        v8 = pygame.Vector2(-W/ratio_body_wheel/2 + W/2 + wheel_dist, -H/2 + motor_dist)
        v9 = pygame.Vector2(-W/ratio_body_wheel/2 + W/2 + wheel_dist, -H*2/2)
        v10 = pygame.Vector2(W/ratio_body_wheel/2 + W/2 + wheel_dist, -H*2/2)
        v11 = pygame.Vector2(W/ratio_body_wheel/2 + W/2 + wheel_dist, H*2/2)
        v12 = pygame.Vector2(-W/ratio_body_wheel/2 + W/2 + wheel_dist, H*2/2)
        v13 = pygame.Vector2(-W/ratio_body_wheel/2 + W/2 + wheel_dist, H/2 - motor_dist)
        v14 = pygame.Vector2(W/2, H/2 - motor_dist)
        v15 = pygame.Vector2(W/2, H/2)
        v16 = pygame.Vector2(-W/2, H/2)
        v17 = pygame.Vector2(-W/2, H/2 - motor_dist)
        v18 = pygame.Vector2(W/ratio_body_wheel/2 - W/2 - wheel_dist, H/2 - motor_dist)
        v19 = pygame.Vector2(W/ratio_body_wheel/2 - W/2 - wheel_dist, H*2/2)
        v20 = pygame.Vector2(-W/ratio_body_wheel/2 - W/2 - wheel_dist, H*2/2)

        self.poly_ref = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20]  # coordinates for reference polygon
        self.poly_cur = []              # coordinates for current polygon

        # init bounding rect
        self.rect = pygame.Rect(0, 0, self.BOUNDING, self.BOUNDING)
        self.rect.centerx = 0
        self.rect.centery = 0

    # =============================================================================
    # Rendering and Helper functions
    # =============================================================================
    def render(self):
        """
        Render body orientation and position.
        """
        self.poly_cur = []
        # use precalculated rotations and add position vector
        for p in poly_rotated_lookup[int(round(self.agent.actuation.heading)) % 360 - 1]:
            self.poly_cur.append(p + self.agent.actuation.position)
        self.agent.environment.dynamic_polygon_list.append([self.COLOR, self.poly_cur, 3])

        # Debug mode: show bounding rect
        # self.agent.environment.dynamic_rectangle_list.append([self.COLOR, self.rect, 3])

    def build_rotation_lookup(self):
        """
        Calculates a lookup table for the rotation of an agent to improve rendering performance.
        The lookup table is not relevant for logic performance (when simulating without drawing on a display).
        The results are stored in a global variable, so that the calculation has only to be performed once.
        """
        for degree in range(360):
            ang = math.radians(degree + 1)
            turn_mat = [[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]]

            self.poly_cur = []
            for p in self.poly_ref:
                self.poly_cur.append(np.matmul(p, turn_mat))
            poly_rotated_lookup.append(self.poly_cur)

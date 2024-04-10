from swarmy.perception import Perception
import pygame
import math
import numpy as np


class BumperSensor(Perception):
    def __init__(self, a,e, config):
        super().__init__(a,e)
        self.agent = a
        self.environment = e
        self.config = config

    def sensor(self):

        ## Bumper returs 1 if collision is detected, 0 otherwise

        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        rob_pos = pygame.Vector2(robot_position_x, robot_position_y)

        sensor_1_direction_x_l = math.sin(math.radians(robot_heading + 40))
        sensor_1_direction_y_l = math.cos(math.radians(robot_heading + 40))
        sensor_2_direction_x_r = math.sin(math.radians(robot_heading - 40))
        sensor_2_direction_y_r = math.cos(math.radians(robot_heading - 40))

        bumper_l_pos = [(robot_position_x+(sensor_1_direction_x_l*35)),
                   (robot_position_y+(sensor_1_direction_y_l*35))]
        bumper_r_pos= [(robot_position_x+(sensor_2_direction_x_r*35)),
                  (robot_position_y+(sensor_2_direction_y_r*35))]



        bumper_color = (255, 0, 0)

        bumper = [bumper_color, bumper_l_pos, bumper_r_pos]

        self.environment.add_dynamic_line_object(bumper)

        # helper to transform lines to rectange objects, allows for collision detection
        helper_object = pygame.draw.line(self.agent.environment.displaySurface, bumper_color, rob_pos, bumper_l_pos)
        self.environment.bumper_object_list.append(helper_object)


        # list of all objects in the environment
        objects = self.environment.get_agent_object() + [wall[1] for wall in self.environment.get_static_rect_list()]

        # check if the robot is colliding with any object
        sensor_val = 0
        for idx,line in enumerate(objects):
            if idx == self.agent.unique_id:         # skips the robot itself
                continue

            intersection = np.asarray(line.clip(helper_object))
            if intersection [2]>0:
                return 1

        return sensor_val



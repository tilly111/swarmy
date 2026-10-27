from swarmy.perception import Perception
import pygame
import math


class BumperSensor(Perception):
    def __init__(self, agent, environment, config):
        super().__init__(agent, environment)
        self.config = config

    def sensor(self):
        """
        Bumper returns 1 if collision is detected, 0 otherwise
        Hints:
        - x, y, heading = self.agent.get_position() # returns the current position and heading of the robot to calculate the relative position of the sensor
        - to visualize the sensors the following functions can help
            - self.environment.add_dynamic_line_object([(R, G, B), start_of_line, end_of_line])
            - self.environment.add_dynamic_circle_object([(R, G, B), (x_pos, y_pos), radius, line_width])
            - self.environment.add_dynamic_rectangle_object([(R, G, B), pygame.Rect(x, y, width, height), line_width])
        - to detect other objects the following functions might help:
            - self.environment.get_agent_object() - get all robots boundary boxes as pygame.Rect objects
            - self.environment.get_static_rectangle_list() - get static rectangles such as walls
            - self.environment.get_static_circle_list() - none implemented yet
            - self.environment.get_dynamic_circle_list() - none implemented yet
            - self.environment.get_dynamic_line_list() - get dynamic lines such as bumpers
            - self.environment.get_dynamic_rectangle_list() - none implemented yet
        """
        # get robot position and heading
        x, y, heading = self.agent.get_position()

        robot_position = pygame.Vector2(x, y)

        left_direction_x = math.sin(math.radians(heading + 40))
        left_direction_y = math.cos(math.radians(heading + 40))
        right_direction_x = math.sin(math.radians(heading - 40))
        right_direction_y = math.cos(math.radians(heading - 40))

        bumper_left_end = [x + left_direction_x * 35,
                           y + left_direction_y * 35]
        bumper_right_end = [x + right_direction_x * 35,
                            y + right_direction_y * 35]

        bumper_color = (255, 0, 0)

        bumper = [bumper_color, bumper_left_end, bumper_right_end]

        self.environment.add_dynamic_line_object(bumper)

        # get all objects in arena
        objects = self.environment.get_agent_object() + [wall[1] for wall in self.environment.get_static_rectangle_list()]

        # checks for collision
        for idx, rect in enumerate(objects):
            if idx == self.agent.unique_id:         # skips the robot itself
                continue
            if rect.clipline(robot_position, bumper_left_end) or rect.clipline(robot_position, bumper_right_end):
                return 1
        return 0

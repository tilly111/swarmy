import random

from swarmy.actuation import Actuation
import yaml
import math

class Aggressive(Actuation):

    def __init__(self, agent, p, d, config):
        super().__init__(agent, p, d)
        self.linear_velocity = 3
        self.angle_velocity = 6

        self.config = config


    def controller(self):
        """
        This function overwrites the abstract method of the robot controller.
        these function might help:
        - self.stepForward(velocity)
        - self.stepBackward(velocity)
        - self.turn_right(angle_velocity)
        - self.turn_left(angle_velocity)
        - self.agent.get_position() # get the current position of the robot x,y and angle (unit vector)
        Returns:
        """


        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        s_r, s_l = self.agent.perception.Sensor()

        vel_r = s_r * 10
        vel_l = s_l * 10

        new_robot_heading = (robot_heading - int(15 * (vel_r - vel_l))) % 360

        new_direction_x = math.sin(math.radians(new_robot_heading))
        new_direction_y = math.cos(math.radians(new_robot_heading))

        new_position_x = robot_position_x + new_direction_x * (vel_r + vel_l) / 2
        new_position_y = robot_position_y + new_direction_y * (vel_r + vel_l) / 2

        self.agent.set_position(new_position_x, new_position_y, robot_heading)


        """
        #self.stepForward(self.linear_velocity * random.random())
        #self.turn_right(self.angle_velocity * random.randint(-4, 4))
        """

    def torus(self):

        """
        Implement torus world by manipulating the robot position.
        Hint: use self.robot_position[0] and self.robot_position[1] to access the robot position
        """
        # print(self.agent.get_position()) # get the current position of the robot x,y and angle (unit vector)

        robot_position_x,robot_position_y, robot_heading = self.agent.get_position()
        #print(self.agent.get_position())
        ### Solution ##
        if robot_position_x < 0 or robot_position_y < 0 or robot_position_x > self.config['world_width'] or robot_position_y > self.config['world_height']:
            robot_position_x %=  self.config['world_width']
            robot_position_y %=  self.config['world_height']
            self.agent.set_position(robot_position_x, robot_position_y, robot_heading)






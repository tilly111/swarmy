import random

from swarmy.actuation import Actuation
import yaml

class MyController(Actuation):

    def __init__(self, agent,config):
        super().__init__(agent)
        """
        self.linear_velocity = <your value> # set the linear velocity of the robot
        self.angle_velocity =  <your value> # set the angular velocity of the robot
        """
        self.config = config
        self.init_pos = True            # flag to set initial position of the robot




    def controller(self):
        """
        This function overwrites the abstract method of the robot controller.
        these function might help:
        - self.stepBackward(velocity)
        - self.turn_right(angle_velocity)
        - self.turn_left(angle_velocity)
        - x,y,gamme = self.agent.get_position() # returns the current position and heading of the robot.
        - self.agent.set_position(new_position_x, new_position_y, robot_heading) # set the new position of the robot
        - self.agent.get_perception() returns the ID of the robot and sensor values that you implemented in sensor() of the class MySensor()
        Returns:
        """

        #Set initial robot position and direction
        if self.init_pos:
            self.agent.initial_position()
            self.init_pos = False

        # example controller
        sensor = self.agent.get_perception()
        if sensor[1] == 1:
            self.stepForward(0) # move backwards
        else:
            self.stepForward(1) # move forward with random velocity
            # self.turn_right(2 * random.randint(-4, 4)) # turn right or left with random angle velocity

    def torus(self):
        """
        Implement torus world by manipulating the robot position. Again self.agent.get_position and self.agent.set_position might be useful
        """
        robot_position_x,robot_position_y, robot_heading = self.agent.get_position()


        """ Implement torus world by manipulating the robot position, here."""


        self.agent.set_position(robot_position_x, robot_position_y, robot_heading)




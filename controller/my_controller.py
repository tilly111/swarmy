import random

from swarmy.actuation import Actuation


class MyController(Actuation):

    def __init__(self, agent, config):
        super().__init__(agent, config)
        # self.linear_velocity = <your value>   # set the linear velocity of the robot
        # self.angular_velocity = <your value>  # set the angular velocity of the robot

    def controller(self):
        """
        This function overwrites the abstract method of the robot controller.
        These functions might help:
        - self.step_forward(velocity)
        - self.step_backward(velocity)
        - self.turn_right(angular_velocity)
        - self.turn_left(angular_velocity)
        - x, y, heading = self.agent.get_position() # returns the current position and heading of the robot
        - self.agent.set_position(new_x, new_y, heading) # set the new position of the robot
        - self.agent.get_perception() # returns the ID of the robot followed by the values of each sensor's sensor()
        """
        # example controller
        sensor = self.agent.get_perception()
        if sensor[1] == 1:
            self.step_forward(0)  # stop
        else:
            self.step_forward(1)  # move forward
            # self.turn_right(2 * random.randint(-4, 4))  # turn right or left with random angular velocity

    def torus(self):
        """
        Implement torus world by manipulating the robot position. Again self.agent.get_position and self.agent.set_position might be useful
        """
        x, y, heading = self.agent.get_position()

        """ Implement torus world by manipulating the robot position, here."""

        self.agent.set_position(x, y, heading)

import random

from swarmy.actuation import Actuation
import yaml

class MyController(Actuation):

    def __init__(self, agent,config):
        super().__init__(agent)
        self.config = config
        self.init_pos = True


    def controller(self):
        "Inititial robot position and direction"
        if self.init_pos:
            self.agent.set_position(random.randint(10, self.config['world_width'] - 10), random.randint(10, self.config['world_height'] - 10), random.randint(0, 360))
            self.init_pos = False
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
        self.stepForward(2 * random.random())
        self.turn_right(2 * random.randint(-4, 4))


        #self.agent.perception[0].Sensor()
        #self.agent.perception[1].Sensor()

    # ==========================Space for your implementation===================================================

    def torus(self):
        pass
        """
        Implement torus world by manipulating the robot position.
        Hint: use self.robot_position[0] and self.robot_position[1] to access the robot position
        """
        robot_position_x,robot_position_y, robot_heading = self.agent.get_position()
        #print(self.agent.get_position())
        ### Solution ##
        #if robot_position_x < 0 or robot_position_y < 0 or robot_position_x > self.config['world_width'] or robot_position_y > self.config['world_height']:
        #    robot_position_x %=  self.config['world_width']
        #    robot_position_y %=  self.config['world_height']
        #    self.agent.set_position(robot_position_x, robot_position_y, robot_heading)




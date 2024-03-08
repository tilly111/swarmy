from swarmy.perception import Perception

import math
class MySensor(Perception):
    def __init__(self, a,e, config):
        super().__init__(a,e)
        self.agent = a
        self.environment = e   # This is the environment, your implementation in world.py
        self.config = config

    def Sensor(self):
        #print("I am a sensor")
        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()

        sensor_1_direction_x_l = math.sin(math.radians(robot_heading + 70))
        sensor_1_direction_y_l = math.cos(math.radians(robot_heading + 70))
        sensor_2_direction_x_r = math.sin(math.radians(robot_heading - 70))
        sensor_2_direction_y_r = math.cos(math.radians(robot_heading - 70))

        s_l_pos = [(robot_position_x+(sensor_1_direction_x_l*15))%self.config['world_width'],
                   (robot_position_y+(sensor_1_direction_y_l*15))%self.config['world_height']]
        s_r_pos= [(robot_position_x+(sensor_2_direction_x_r*15))%self.config['world_width'],
                  (robot_position_y+(sensor_2_direction_y_r*15))%self.config['world_height']]


        self.env.dynamicCircList.append([(255,0,0), (s_l_pos[0], s_l_pos[1]) , 5, 1])
        self.env.dynamicCircList.append([(255,0,0), (s_r_pos[0], s_r_pos[1]), 5, 1])

        s_l = self.environment.light_dist[int(s_l_pos[0]),int(s_l_pos[1]),2]/255
        s_r = self.environment.light_dist[int(s_r_pos[0]),int(s_r_pos[1]),2]/255

        return s_l, s_r

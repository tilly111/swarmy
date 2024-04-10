from swarmy.perception import Perception
import pygame
import math
import numpy as np


class ProximitySensor(Perception):
    def __init__(self, a,e, config):
        super().__init__(a,e)
        self.agent = a
        self.environment = e
        self.config = config

    def sensor(self):
        #print("Proximity Sensor")
        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        rob_pos = pygame.Vector2(robot_position_x, robot_position_y)
        range = 60
        direction_lx = math.sin(math.radians(robot_heading + 45))
        direction_ly = math.cos(math.radians(robot_heading + 45))
        direction_mx = math.sin(math.radians(robot_heading))
        direction_my = math.cos(math.radians(robot_heading))
        direction_rx = math.sin(math.radians(robot_heading-45))
        direction_ry = math.cos(math.radians(robot_heading-45))

        p_l_pos = pygame.Vector2((robot_position_x + (direction_lx * range)), (robot_position_y + (direction_ly * range)))
        p_m_pos = pygame.Vector2((robot_position_x + (direction_mx * range)), (robot_position_y + (direction_my * range)))
        p_r_pos = pygame.Vector2((robot_position_x + (direction_rx * range)), (robot_position_y + (direction_ry * range)))
        sensors = [p_l_pos, p_m_pos, p_r_pos]
        self.env.dynamicLineList.append([(255, 0, 0), rob_pos, p_l_pos])
        self.env.dynamicLineList.append([(255, 0, 0), rob_pos, (p_m_pos)])
        self.env.dynamicLineList.append([(255, 0, 0), rob_pos, (p_r_pos)])

        dynamicLineList = []
        dynamicLineList.append(pygame.draw.line(self.agent.environment.displaySurface, (255, 0, 0), rob_pos, (p_l_pos)))
        dynamicLineList.append(pygame.draw.line(self.agent.environment.displaySurface, (255, 0, 0), rob_pos, (p_m_pos)))
        dynamicLineList.append(pygame.draw.line(self.agent.environment.displaySurface, (255, 0, 0), rob_pos, (p_r_pos)))

        # for x in self.dynamicLineList:
        #    pygame.draw.line(self.displaySurface, x[0], x[1], x[2])
        testbedWidth = self.agent.environment.width
        testbedHeight = self.agent.environment.height

        sensor_val = [0, 0, 0]
        #print(self.agent.environment.staticRectList)
        for idx_w,wall in enumerate(self.agent.environment.staticRectList):
            for idx,line in enumerate(dynamicLineList):
                line_new = np.asarray(wall[1].clip(line))
                if (line_new[2]>0):
                    d = math.dist([line_new[0],line_new[1]],[rob_pos.x, rob_pos.y])
                    sensor_val[idx]= 1-d/range
        #print(sensor_val)
        return sensor_val



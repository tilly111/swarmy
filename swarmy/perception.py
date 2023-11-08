# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module includes all perception possibilites of an agent.
"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
import pygame
import math
# =============================================================================
# Class
# =============================================================================
class Perception():
    pass
    """
    The perception object represents the all sensing capabilites of an agent.
    All sensors will be defined here. 
        
    Args:
        a (agent.py): instance of the agent    
    
    Available sensors:
        Your light sensor
    
    """
    def __init__(self, a, e):
        
        """
        Initialize perception object.
        """    

        # variables        
        self.agent = a
        self.env = e

        self.resolution = 1
        self.range = 70

        # TODO make dynamic
        self.light_souce_x = self.env.width / 2
        self.light_souce_y = self.env.height / 2


    # returns between 1 and 0
    def light_sensor(self):
        r_pos = self.agent.actuation.position  # x = 0, y = 0
        r_ori = - self.agent.actuation.angle + 90
        # make 5 units apart
        x_sens = np.array([0, 0])  # left right?
        y_sens = np.array([10, -10])
        # rotate
        x_sens_rot = x_sens * np.cos(np.deg2rad(r_ori)) - y_sens * np.sin(np.deg2rad(r_ori))
        y_sens_rot = x_sens * np.sin(np.deg2rad(r_ori)) + y_sens * np.cos(np.deg2rad(r_ori))
        # translate
        x_sens_fin = x_sens_rot + r_pos[0]
        y_sens_fin = y_sens_rot + r_pos[1]

        dis_l = np.sqrt((x_sens_fin[0] - self.light_souce_x)**2 + (y_sens_fin[0] - self.light_souce_y)**2)
        dis_r = np.sqrt((x_sens_fin[1] - self.light_souce_x) ** 2 + (y_sens_fin[1] - self.light_souce_y) ** 2)
        return [1 - (dis_l / 1415), 1 - (dis_r / 1415)]


    def proximity_sensor(self):
        """
        Returns a value between [0...1] depending on the distance of the obstacle
        """
        robot_pos = self.agent.actuation.position
        robot_ori = - self.agent.actuation.angle + 90

        # generate rays
        ray_x = np.arange(30, 30+self.range, self.resolution, dtype=int)
        ray_y = np.arange(30, 30+self.range, self.resolution, dtype=int) * 0

        # print("rayx", ray_x)
        # print("rayy", ray_y)

        # rotate rays
        # x′ = x * cos(θ) - y * sin(θ)
        # y′ = x * sin(θ) + y * cos(θ)
        ray_x_rot = ray_x * np.cos(np.deg2rad(robot_ori)) - ray_y * np.sin(np.deg2rad(robot_ori))
        ray_y_rot = ray_x * np.sin(np.deg2rad(robot_ori)) + ray_y * np.cos(np.deg2rad(robot_ori))

        # sensor left
        ray_x_rot1 = ray_x * np.cos(np.deg2rad(robot_ori-45)) - ray_y * np.sin(np.deg2rad(robot_ori-45))
        ray_y_rot1 = ray_x * np.sin(np.deg2rad(robot_ori-45)) + ray_y * np.cos(np.deg2rad(robot_ori-45))

        # sensor right
        ray_x_rot2 = ray_x * np.cos(np.deg2rad(robot_ori+45)) - ray_y * np.sin(np.deg2rad(robot_ori+45))
        ray_y_rot2 = ray_x * np.sin(np.deg2rad(robot_ori+45)) + ray_y * np.cos(np.deg2rad(robot_ori+45))

        # translate rays
        ray_x_fin = ray_x_rot + robot_pos[0]
        ray_y_fin = ray_y_rot + robot_pos[1]

        ray_x_fin1 = ray_x_rot1 + robot_pos[0]
        ray_y_fin1 = ray_y_rot1 + robot_pos[1]

        ray_x_fin2 = ray_x_rot2 + robot_pos[0]
        ray_y_fin2 = ray_y_rot2 + robot_pos[1]

        # append for rendering
        ray_render = [ray_x_fin[0], ray_y_fin[0], ray_x_fin[-1], ray_y_fin[-1]]
        self.env.sensor_rays.append(ray_render)
        ray_render = [ray_x_fin1[0], ray_y_fin1[0], ray_x_fin1[-1], ray_y_fin1[-1]]
        self.env.sensor_rays.append(ray_render)
        ray_render = [ray_x_fin2[0], ray_y_fin2[0], ray_x_fin2[-1], ray_y_fin2[-1]]
        self.env.sensor_rays.append(ray_render)

        # for obstacles
        vals = [0.0, 0.0, 0.0]
        for i in range(len(self.env.staticRectList)):
            # print("obj", type(self.env.staticRectList[i][1]))
            # go along the ray
            for j in range(self.range):
                if self.env.staticRectList[i][1].collidepoint(int(ray_x_fin1[j]), int(ray_y_fin1[j])) and vals[0] == 0.0:
                    vals[0] = (self.range - j) / self.range
                if self.env.staticRectList[i][1].collidepoint(int(ray_x_fin[j]), int(ray_y_fin[j])) and vals[1] == 0.0:
                    vals[1] = (self.range - j) / self.range
                if self.env.staticRectList[i][1].collidepoint(int(ray_x_fin2[j]), int(ray_y_fin2[j])) and vals[2] == 0.0:
                    vals[2] = (self.range - j) / self.range

        # check for moving obstacles aka other agents
        # print(f"[{self.agent.agent_id}] length of list {len(self.env.dynamicObstacles)}")
        vals_dyn = [0.0, 0.0, 0.0]
        for i in range(len(self.env.dynamicObstacles)):
            # go along the ray
            if self.env.dynamicObstacles[i] == self.agent.body.rect:
                # do not check yourself
                continue

            for j in range(self.range):
                if self.env.dynamicObstacles[i].collidepoint(int(ray_x_fin1[j]), int(ray_y_fin1[j])) and vals_dyn[0] == 0.0:
                    vals_dyn[0] = (self.range - j) / self.range
                if self.env.dynamicObstacles[i].collidepoint(int(ray_x_fin[j]), int(ray_y_fin[j])) and vals_dyn[1] == 0.0:
                    vals_dyn[1] = (self.range - j) / self.range
                if self.env.dynamicObstacles[i].collidepoint(int(ray_x_fin2[j]), int(ray_y_fin2[j])) and vals_dyn[2] == 0.0:
                    vals_dyn[2] = (self.range - j) / self.range


        # return np.maximum(vals, vals_dyn)
        return [vals, vals_dyn]


    # sensor which returns true if a item is in reach and not picked up already
    # returns False otherwise
    def item_sensor(self):
        # get the item density
        # sum(1 - normalized_distance * 1/n)
        n = len(self.env.dynamicItems)
        dens = 0
        for item in self.env.dynamicItems:
            if (np.sqrt((self.agent.body.rect.centerx - item.rect.centerx) ** 2 + (
                        self.agent.body.rect.centery - item.rect.centery) ** 2) / 1414.2) < 0.3:
                dens += 1
        #     dens += 1 - (np.sqrt((self.agent.body.rect.centerx - item.rect.centerx) ** 2 + (
        #                 self.agent.body.rect.centery - item.rect.centery) ** 2) / 1414.2)
        dens /= n

        # find the next item
        for item in self.env.dynamicItems:
            if np.sqrt((self.agent.body.rect.centerx - item.rect.centerx)**2 + (self.agent.body.rect.centery - item.rect.centery)**2) < item.radius + 15:  # if in range
                if not item.picked_up:  # item is not picked up
                    return [True, item, dens]
        return [False, None, dens]


    def bumper_sensor(self):
        objects_to_push = []

        r_ori = self.agent.actuation.angle - 90


        for item in self.env.dynamicItems:
            if np.sqrt((self.agent.body.rect.centerx - item.rect.centerx) ** 2 + (
                    self.agent.body.rect.centery - item.rect.centery) ** 2) < item.radius + 30:  # if in range

                obj_ori = np.rad2deg(np.arctan2(-(item.rect.centery - self.agent.body.rect.centery),
                                                item.rect.centerx - self.agent.body.rect.centerx))

                if np.abs(r_ori - obj_ori) < 80 or np.abs(r_ori - obj_ori) > 280:  # calcualte angle of object
                    objects_to_push.append(item)

        return objects_to_push

 

       

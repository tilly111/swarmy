# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   18/02/2021 -- 13/04/2022
# modified by: Eduard Buss  (17.03.2023)
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
In this module one specific experiment can be executed.
The module initilizes pygame.
The parameters for the simulation are:
    - simulation speed
    - maximum agent speed
    - number of obstacles
"""

# =============================================================================
# Imports
# =============================================================================
import pygame
import random
import itertools
import numpy as np


# import internal object classes
from .environment import Environment
from .item import Obstacle, Item
from .agent import Agent

# =============================================================================
# Class
# =============================================================================
class Experiment():
    
    def __init__(self):
        super(Experiment, self).__init__()
        # kommentare 

        
    def run(self, rendering=1, swarm_size=1, controllers=["avoid"], track=False, n_items=1, save_file_name=None):
        """
        Start swarm simulation expermiment
        
        Args:
            rendering               (int):   1 = show simulation; -1 = hide simulation; 0 = black screen (capture mode)           
        """
        # pygame presets
        pygame.init()  					        # initialize pygame
        running = True  				        # termination condition
            
        # tracking variable
        timesteps_counter = 0

        # -----------------------------------------------------------------------------
        # instantiations

        # instantiate environment
        environment = Environment(rendering) 
        w = environment.width
        h = environment.height
        
        # instatiate obstacles
        # TODO add obstacles here
        obstacleList = []
        # create walls
        left_wall = Obstacle(environment, 10, h/2, 20, h, 3)
        right_wall = Obstacle(environment, w-10, h / 2, 20, h, 3)

        top_wall = Obstacle(environment, w/2, 10, w, 20, 3)
        bot_wall = Obstacle(environment, w/2, h-10, w, 20, 3)

        # TODO add back in for tasksheet 3
        # obstacle1 = Obstacle(environment, w/2, h/2, 20, 300, 3)
        # obstacleList.append(obstacle1)

        obstacleList.append(left_wall)
        obstacleList.append(right_wall)
        obstacleList.append(top_wall)
        obstacleList.append(bot_wall)

        # instatiate agent
        agent_list = []
        for i in range(swarm_size):
            agent_list.append(Agent([random.randint(30, w-30), random.randint(30, h-30)], 0, environment, i, controllers[i], track))  #  random.randint(0, 360)


        item_list = []
        for i in range(n_items):
            item_list.append(Item(environment, random.randint(100, w-100), random.randint(100, h-100), 30, 30, 15))
    
        # -----------------------------------------------------------------------------
        # initializations
        for i in range(swarm_size):
            agent_list[i].body.helperLUT()
        # newAgent.body.helperLUT()   # global lookup table needs to be calculated only once
        ##print("Range: " + str(agentList[0].nesting.communication.BROADCASTING_RANGE_MM))

        # update after all agents were instantiated
        #newAgent.perception.helperOAO()  # update other agents list and obstacles list


        # tracking the position of the objects
        save_path = "measurements/" + str(save_file_name) + ".npy"
        save_data = None

        # =============================================================================
        # Run experiment: Loop-Processing
        # =============================================================================
        while running:
            timesteps_counter += 1
            print(timesteps_counter)
            
            #-----------------------------------------------------------------------------
            # ASYNCHRON 
            
            # get the set of keys pressed and check for user input
            pressedKeys = pygame.key.get_pressed()
                       
            # handle user input
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:    # Check for KEYDOWN event
                                    
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.QUIT:
                    running = False

            # exit condition;
            if timesteps_counter > 20000:
                running = False
     
            #-----------------------------------------------------------------------------
            # SYNCHRON         
     
            # update agents
            idx = np.random.permutation(swarm_size)
            for i in idx:
                agent_list[i].processing.perform(pressedKeys)

            # track items
            save_data_tmp = np.zeros((1, 1+2*n_items))
            save_data_tmp[0, 0] = timesteps_counter
            for i in range(n_items):
                # x
                save_data_tmp[0, (i*2)+1] = item_list[i].rect.centerx
                # y
                save_data_tmp[0, (i + 1) * 2] = item_list[i].rect.centery
            if save_data is None:
                save_data = save_data_tmp
            else:
                save_data = np.concatenate((save_data, save_data_tmp), axis=0)

            # reset bodies of the robots
            environment.resetDynamicObstacles()

            # newAgent.processing.perform(pressedKeys)
            # Torus
            #newAgent.actuation.position[0] = newAgent.actuation.position[0] % environment.width
            #newAgent.actuation.position[1] = newAgent.actuation.position[1] % environment.height

            # display results
            if(rendering == 1):
                for i in range(swarm_size):
                    agent_list[i].body.render()
                for i in range(n_items):
                    item_list[i].render()
                # newAgent.body.render()         # update agent body
                environment.render()           # update content on display        


        # save tracked data
        with open(save_path, 'wb') as f:
            np.save(f, save_data)


        pygame.quit()

        return None

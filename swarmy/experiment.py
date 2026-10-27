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
The module initializes pygame, creates the environment and the agents
and runs the simulation loop. All parameters are set in config.yaml.
"""

# =============================================================================
# Imports
# =============================================================================
import random
import numpy as np
import pygame


# =============================================================================
# Class
# =============================================================================
class Experiment():

    def __init__(self, config, controllers, sensors, environment, agent):
        super(Experiment, self).__init__()

        if len(config['controller_ratios']) != len(controllers):
            raise ValueError('config.yaml: controller_ratios needs one entry per controller in workspace.py')

        # seed the random number generators, so that runs can be repeated
        seed = config.get('seed')
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.config = config
        self.controllers = controllers
        self.sensors = sensors
        self.environment = environment(config)
        self.agent = agent

    def run(self, rendering):
        """
        Start swarm simulation experiment

        Args:
            rendering (int): 1 = normal window; 0 = borderless window; -1 = no window (no fps limit)
        """
        # pygame presets
        pygame.init()                   # initialize pygame
        running = True                  # termination condition

        # tracking variable
        timesteps_counter = 0

        # -----------------------------------------------------------------------------
        # instantiations

        # instantiate environment
        environment = self.environment
        environment.render_init()

        # instantiate agents, controllers are assigned according to controller_ratios in config.yaml
        controller_ratios = self.config['controller_ratios']
        agent_list = []
        agent_counter = 0
        while agent_counter < self.config['number_of_agents']:
            share = agent_counter / self.config['number_of_agents']
            controller_index = 0
            while controller_index < len(controller_ratios) - 1 and share >= sum(controller_ratios[:controller_index + 1]):
                controller_index += 1
            new_agent = self.agent(environment, self.controllers[controller_index], self.sensors, self.config)
            new_agent.initial_position()
            new_agent.unique_id = agent_counter
            agent_list.append(new_agent)
            agent_counter += 1
        environment.agent_list = agent_list

        # -----------------------------------------------------------------------------
        # initializations
        if agent_list:
            agent_list[0].body.build_rotation_lookup()    # global lookup table needs to be calculated only once

        # =============================================================================
        # Run experiment: Loop-Processing
        # =============================================================================
        while running and timesteps_counter < self.config['max_timestep']:
            timesteps_counter += 1

            # -----------------------------------------------------------------------------
            # ASYNCHRON

            # get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()

            # handle user input
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:    # Check for KEYDOWN event

                    # If the Esc key is pressed, then exit the main loop
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.QUIT:
                    running = False

            # -----------------------------------------------------------------------------
            # SYNCHRON
            for agent in agent_list:
                environment.agent_object_list.append(
                    pygame.Rect(agent.actuation.position[0] - 15, agent.actuation.position[1] - 15, 30, 30))

            # update agents
            for agent in agent_list:
                agent.processing.perform(pressed_keys)

            # display results
            if rendering != -1:
                for agent in agent_list:
                    agent.body.render()         # update agent body
                environment.render()            # update content on display

            environment.agent_object_list = []
            environment.reset_dynamic_buffers()

        if self.config['save_trajectory']:
            for i, agent in enumerate(agent_list):
                if i == len(agent_list) - 1:
                    agent.save_information(True)
                else:
                    agent.save_information(False)

        print('Experiment finished by manual stopping or maximum timesteps reached. Check config.yaml to increase the maximum timesteps.')
        pygame.quit()
        return None

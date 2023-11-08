# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   18/02/2021 -- 13/04/2022
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
    - number of agents
    - number of obstacles
    - total number of tokens
    - number of sources and sinks
    - source and sink interaction radius
    - token difficulty level
    - communication properties: range, noise
"""


# =============================================================================
# Imports
# =============================================================================
import pygame
import time
import random

# import internal object classes
from .environment import Environment
from .item import Source
from .item import Sink
from .item import Obstacle
from .agent import Agent

import os
import datetime


# =============================================================================
# Class
# =============================================================================
class Experiment():
    
    def __init__(self):
        super(Experiment, self).__init__()
        
    def run(self, numberOfAgents, rendering, measFolderPath, captFolderPath, xParams):
        print("das ding ist mega schrott")
        print("rendering", rendering)
        """
        Start swarm simulation expermiment
        
        Args:
            numberOfAgents          (int):   choose number of agents for experiment
            rendering               (int):   1 = show simulation; -1 = hide simulation; 0 = black screen (capture mode)           
            measFolderPath       (string):   path to measurement results folder or None if unused
            captFolderPath       (string):   path to image capture folder or None if unused
            xParams                (list):   list with experiment specific parameters. [0] = sensibility rssi fiter; [1] = boolean broadcast token acknowledge
        """
        
        # prepare directories, filenames and measurement file
        filenameExperiment = "" + datetime.datetime.now().strftime("%Y%m%d - Experiment.txt")
        filenameCaptureTemplate = "" + datetime.datetime.now().strftime("%Y%m%d %H%M%S - Capture - ")
            
        if captFolderPath != None:
            os.makedirs(os.path.dirname(captFolderPath), exist_ok=True)
        
        if measFolderPath != None:
            os.makedirs(os.path.dirname(measFolderPath), exist_ok=True)
            measFile = open(measFolderPath + filenameExperiment, "a")
        
        # pygame presets
        pygame.init()  					        # initialize pygame
        print("omega lul")
        running = True  				        # termination condition
            
        # tracking variables
        time_simulation = 0
        timesteps_counter = 0
        timesteps_allTokensInSink = 0           # discarded all tokens in sink
        timesteps_allTokensFromSource = 0       # picked up all tokens from source
        totalCollisions_counter = 0             # collisions of the whole swarm per experiment
        totalReceivedMessages_counter = 0       # Received messages for the whole swarm 
        totalBroadcastedMessages_counter = 0    # Broadcasted messages for the whole swarm 

        # -----------------------------------------------------------------------------
        # instantiations

        # instantiate environment
        environment = Environment(rendering) 
        w = environment.width
        h = environment.height
        
        # instantiate sources
        sourceList = []
        source1 = Source(1, environment, 0+100, h/2, 75, 75, 3, 10) ## add a new source on a fixed position
        sourceList.append(source1)
        
        # instantiate sinks
        sinkList = []
        sink1 = Sink(1, environment, w-100, h/2, 75, 75, 3)
        sinkList.append(sink1)
        
        # instatiate obstacles
        obstacleList = []
        obstacle1 = Obstacle(environment, w/2, h/2, 20, 300, 3)    
        obstacleList.append(obstacle1)
        # obstacle2 = Obstacle(environment, w/4, h/4, 50, 50, 3)       
        # obstacleList.append(obstacle2)

        # instatiate agents
        agentList = []
        count = 0
        print("test print", numberOfAgents)
        while count < numberOfAgents:
            # the agent list is added by reference not by value --> agents have at the end a complete list of all agents
            newAgent = Agent(count+1, [random.randint(10, w-10), random.randint(10, h-10)], random.randint(0, 360), environment, agentList, sourceList, sinkList, obstacleList, xParams)
            positonAvailable = not newAgent.perception.collisionSensor()
            if(positonAvailable):
                count = count + 1
                agentList.append(newAgent)
        
        # -----------------------------------------------------------------------------
        # initializations
        
        agentList[0].body.helperLUT()   # global lookup table needs to be calculated only once
        print("Range: " + str(agentList[0].nesting.communication.BROADCASTING_RANGE_MM))

        
        # update after all agents were instantiated
        for agent in agentList:
            agent.perception.helperOAO()  # update other agents list and obstacles list


        # =============================================================================
        # Run experiment: Loop-Processing
        # =============================================================================
        locked = [False,False]   # needed to monitor the timesteps for specific events
        time_start = time.time() # simulation start time

        while running:
            timesteps_counter += 1
            print("is running step", timesteps_counter)
            
            #-----------------------------------------------------------------------------
            # ASYNCHRON 
            
            # get the set of keys pressed and check for user input
            pressedKeys = pygame.key.get_pressed()
                       
            # handle user input
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:    # Check for KEYDOWN event
                                    
                    # capture current image
                    if event.key == pygame.K_SPACE:
                        for agent in agentList:
                            agent.body.render()
                            #agent.nesting.communication.renderCommRadius()
                        environment.render()
                        if(captFolderPath != None):
                            filenameCapture = filenameCaptureTemplate + str(timesteps_counter) + ".png"
                            filename = captFolderPath + filenameCapture
                            pygame.image.save(environment.getDisplay(), filename) # capture image of current step
                    
                    # print current frames per second
                    elif event.key == pygame.K_f:
                        environment.printFPS()
                        
                    # print all tokens in source
                    elif event.key == pygame.K_q:
                        source1.printTokens()

                    # print all tokens in sink
                    elif event.key == pygame.K_s:
                        sink1.printTokens()                       

                    # print all tokens carried by agents
                    elif event.key == pygame.K_1:
                        allTokens = "Tokens - "
                        for agent in agentList:
                            if(len(agent.nesting.communication.tokens)>0):
                                allTokens = allTokens + "A" + str(agent.ID) + ":" + str( agent.nesting.communication.tokens) + str(" ")
                        print(allTokens)

                    # print number of tokens per token type
                    elif event.key == pygame.K_2:
                        allTokens = []
                        countTokens = []
                        for agent in agentList:
                            for t in agent.nesting.communication.tokens:
                                allTokens.append(t)  
                        for x in range(10):        
                            countTokens.append(allTokens.count("T" + str(x+1)))        
                        print("Tokens per type: " + str(countTokens))
                    
                    # print number of tokens per agent
                    elif event.key == pygame.K_3:
                        countAgentTokens = []
                        for agent in agentList:
                            countAgentTokens.append(len(agent.nesting.communication.tokens))
                        print("Tokens per agent: " + str(countAgentTokens))
                      
                    # print number of tokens per agent
                    elif event.key == pygame.K_e:
                        print("Battery Capcity in mAh: " + str(agentList[0].energy.battery))
                        print("Steps: " + str(timesteps_counter))
                    # If the Esc key is pressed, then exit the main loop
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.QUIT:
                    running = False
     
            #-----------------------------------------------------------------------------
            # SYNCHRON         
     
            # update agents                                     
            for agent in random.sample(agentList, len(agentList)):
                agent.processing.perform(pressedKeys)
                agent.energy.dischargeBatteryOneStep()     
            
            # DEBUG
            # print("-------------------------------")
            # print("Agent " + str(agentList[0].ID))
            # print("Outgoing " + str(len(agentList[0].nesting.communication.outgoing)))   
            # print("Incoming " + str(len(agentList[0].nesting.communication.incoming)))
            # print("Tokens " + str(len(agentList[0].nesting.communication.tokens)))
            # print("BroadSteps " + str(agentList[0].nesting.communication.remainingBroadcastingSteps))
            # print("RecMessages " + str(agentList[0].nesting.communication.counterReceivedMessages))

            # display results
            if(rendering == 1):          
                for agent in agentList:             
                    agent.body.render()         # update agent body           
                    #agent.nesting.communication.renderCommRadius()
                environment.render()     # update content on display
            
            # tracking statistics
            if(source1.getNumberOfTokens() == 0 and not locked[0]):         #tokens in source
                timesteps_allTokensFromSource = timesteps_counter
                locked[0] = True
             
            if(sink1.getNumberOfTokens() == 10 and not locked[1]):          # track tokens in sink
                running = False 
                timesteps_allTokensInSink = timesteps_counter
                time_simulation = round((time.time() - time_start), 2)
                locked[1] = True
                for agent in agentList:
                    totalCollisions_counter += agent.processing.monitoring["collisions"]
                    totalReceivedMessages_counter += agent.nesting.communication.counterReceivedMessages
                    totalBroadcastedMessages_counter += agent.nesting.communication.counterBroadcastedMessages
                    
                     
        # =============================================================================
        # Save measurement results
        # =============================================================================       
        timestep = 1/environment.FPS
        if measFolderPath != None:
            measFile.write(str(numberOfAgents) + ";")  # number of agents 
            measFile.write(str(round((timestep),6)) + ";")                                     # number of agents
            measFile.write(str(time_simulation) + ";")                              # simulation time
            measFile.write(str(timesteps_allTokensFromSource) + ";")                # performance - all tokens collected from source - number of timesteps
            measFile.write(str(timesteps_allTokensInSink) + ";")                    # performance - all tokens discarded in sink - number of timesteps
            measFile.write(str(round((totalCollisions_counter),2)) + ";")           # collisions in total
            measFile.write(str(round((totalReceivedMessages_counter),2)) + ";")     # received messages in total
            measFile.write(str(round((totalBroadcastedMessages_counter),2)) + ";")  # broadcasts per agent in total
            measFile.write(str(xParams[0]) + ";")                                   # Broadcasting range
            measFile.write(str(xParams[1]))                                         # tokenExchange 
            measFile.write("\n")                                                    # new line
            measFile.close()
        
        # =============================================================================
        # Print measurement results
        # =============================================================================  
        print("\n------------------------------------")    
        print("Number of Agents: " + str(numberOfAgents))
        print("Simulation time: " + str(time_simulation) + " s")
        print("Natural time: " + str(round((timesteps_allTokensInSink*timestep),2)) + " s")        
        print("Collected all tokens from source: " + str(timesteps_allTokensFromSource) + " steps")        
        print("Discarded all tokens in sink: " + str(timesteps_allTokensInSink) + " steps")
        print("Collisions per agent: " + str(round((totalCollisions_counter/numberOfAgents),2)))     # collisions per agent        
        print("Simulation terminated!")

        # DEBUG
        # print q-tables for each agent
        # for agent in agentList:
        #     print("Agent " + str(agent.ID))
        #     print("Cumulated Rewards:"  + str(agent.processing.monitoring["cumulatedRewards"]))
        #     print(agent.processing.learning.qTable)
        #     print("----------------------")            

        pygame.quit()
        return str(measFolderPath) + filenameExperiment

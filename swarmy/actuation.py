# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
The module represents the motion capabilites of an agent.
"""

# =============================================================================
# Imports
# =============================================================================
import random
import math
import pygame

# =============================================================================
# Class
# =============================================================================
class Actuation():
    """
    The actuation object represents the physical movement and physical actions.
    
    Available capabilities:
        Move forward, move backward, 
        turn left, turn right, turn random, turn angle, 
        collect token, discard token.
    
    Args:
        g (agent.py): instance of the agent
        p ([int, int]): center position
        d (int): initial angle (direction)    
    """
    def __init__(self, g, p, d):
        """
        Initialize actuation object.
        """    
        
        # constants
        self.LINEAR_VELOCITY = 4                # choose even number
        self.ANGLE_VELOCITY = 6                 # choose even number
        self.MAX_NOISE_AMPLITUDE = 1            
        self.MAX_NOISE_DURATION = 7
        self.TURN_DIRECTIONS = [-1, 1]          # 1 = clockwise, -1 = counterclockwise

        # variables
        self.agent = g                  # parent python module
        self.position = p
        self.angle = (d + 90) % 360     # intial position is 90 degrees
        self.direction = [math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle))] # unit vector showing the direction

        # help variables
        self.noiseAngle = 0
        self.noiseDuration = 0
        self.turnDuration = 0                                        # number of rotation steps
        self.turnInProgress = False
        self.turnDirection = random.choice(self.TURN_DIRECTIONS)     # 1 = clockwise, -1 = counterclockwise
                    
        
    def turnRandom(self):
        """
        Choose a random turn angle
        """    
        if(not self.turnInProgress):
            self.turnInProgress = True
            self.turnDuration = random.randint(1,int(180/self.ANGLE_VELOCITY)) # choose the number of rotation steps
            self.turnDirection = random.choice(self.TURN_DIRECTIONS) # choose a direction        
    
    
    def turnAngle(self, angle):
        """
        Choose a turn angle. 
        The function turn() will perform the turn steps.
        """        
        if(not self.turnInProgress):
            self.turnInProgress = True
            
            # choose number of rotation steps
            if(angle > 0):
                self.turnDirection = 1
            elif(angle < 0):
                self.turnDirection = -1
                
            # choose rotation duration    
            self.turnDuration = int(abs(angle)/self.ANGLE_VELOCITY)
            print("Duration: " + str(self.turnDuration))


    def turn(self):
        """
        Perform turn, if turn is in progress.
        
        Returns:
            turned (boolean): True = turn performed, False = no turn performed
        """   
        turned = False
        
        if(self.turnInProgress):
            self.angle = (self.angle + self.ANGLE_VELOCITY*self.turnDirection) % 360
            self.direction[0] = math.sin(math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle)) 
            self.turnDuration -= 1        
            if(self.turnDuration == 0):
                self.turnInProgress = False
            turned =  True
        
        return turned
    
  
    def turnLeft(self):
        """
        Turn one step left.
        """        
        self.angle = (self.angle + self.ANGLE_VELOCITY) % 360
        self.direction[0] = math.sin(math.radians(self.angle))
        self.direction[1] = math.cos(math.radians(self.angle)) 


    def turnRight(self):
        """
        Turn one step right.
        """        
        self.angle = (self.angle - self.ANGLE_VELOCITY) % 360
        self.direction[0] = math.sin(math.radians(self.angle))
        self.direction[1] = math.cos(math.radians(self.angle))             


    def addNoise(self):
        """
        Adds noise to the movement.
        """        
        if(self.noiseDuration == 0):
            self.noiseDuration = random.randint(1,self.MAX_NOISE_DURATION)
            self.noiseAngle = random.randint(-self.MAX_NOISE_AMPLITUDE, self.MAX_NOISE_AMPLITUDE)
        
        if(self.noiseAngle > 0):
            self.angle = (self.angle + 1) % 360
        elif (self.noiseAngle < 0):
            self.angle = (self.angle - 1) % 360
         
        # decrement duration
        self.noiseDuration -= 1

        # calculate the direction from the angle variable
        self.direction[0] = math.sin(math.radians(self.angle))
        self.direction[1] = math.cos(math.radians(self.angle)) 
        self.agent.body.rect.centerx = self.position[0]
        self.agent.body.rect.centery = self.position[1]

        
    def stepForward(self):
        """
        One step forward.
        """
        self.addNoise()

        # calculate the position from the direction and speed and update body position
        self.position[0] += self.direction[0]*self.LINEAR_VELOCITY
        self.position[1] += self.direction[1]*self.LINEAR_VELOCITY
        self.agent.body.rect.centerx = self.position[0]
        self.agent.body.rect.centery = self.position[1]

        
    def stepBackward(self):
        """
        One step backward.
        """
        # calculate the position from the direction and speed and update body position
        self.position[0] -= self.direction[0]*self.LINEAR_VELOCITY
        self.position[1] -= self.direction[1]*self.LINEAR_VELOCITY
        self.agent.body.rect.centerx = self.position[0]
        self.agent.body.rect.centery = self.position[1]
    
    
    def collectToken(self, source):
        """
        Collect a token from a source
        """
        
        # Note: empty list is False else True
        if((source != None) and (not self.agent.nesting.communication.tokens) and self.agent.body.rect.colliderect(source)):   # comply with the physical framework
            token = source.decrementTokens()
            self.agent.nesting.communication.tokens.append(token)
            
            # update state and monitoring      
            self.agent.processing.monitoring["rewards"] += 10       # reward for collecting a token from a source
        else:
            self.agent.processing.monitoring["rewards"] += -1       # punishment for trying to collect a token from a wrong place      
            
        #print("Remaining tokens in source: " + str(len(source.tokens)))


    def discardToken(self, sink):
        """
        Discard a token in a sink
        """
        
        # Note: empty list is False else True
        if((sink != None) and self.agent.nesting.communication.tokens and self.agent.body.rect.colliderect(sink)): # comply with the physical framework
            token = self.agent.nesting.communication.tokens.pop(0)
            sink.incrementTokens(token)
            
            # update state and monitoring            
            self.agent.processing.monitoring["rewards"] += 10         # reward for discarding a token in a sink          
        else:
            self.agent.processing.monitoring["rewards"] += -1         # punishment for discarding a token in a wrong place      
             
        #print("Collected tokens in sink: " + str(len(sink.tokens)))
        
        
#%% Helper functions
        
    def processUserInput(self, pressedKeys):
        """
        Process user keyboard input.
        
        Args:
            pressedKeys (Pygame Keyboard Codes)
        
        """
        if pressedKeys[pygame.K_UP]:           
            self.stepForward()
            
        if pressedKeys[pygame.K_DOWN]:
            self.stepBackward()
            
        if pressedKeys[pygame.K_LEFT]:
            # new angle
            self.angle = (self.angle+self.ANGLE_VELOCITY)%360
                    
            # calculate the direction from the angle variable
            self.direction[0] = math.sin(math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))         
            
        if pressedKeys[pygame.K_RIGHT]:          
            # new angle
            self.angle = (self.angle-self.ANGLE_VELOCITY)%360

            # calculate the direction from the angle variable
            self.direction[0] = math.sin(math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))
            
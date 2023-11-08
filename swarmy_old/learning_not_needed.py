# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   25/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module implements the learning algorithms and represents the acquired behaviour.
"""

# =============================================================================
# Imports
# =============================================================================
import numpy as np
import random

# =============================================================================
# Class
# =============================================================================
class Learning():
    """
    The learning object represents the agent behaviour acquired by learning at lifetime.
        
    Args:
        p (Processing): processing unit    
    """    
    def __init__(self, p):
        """
        Initialize learning object.
        """    
        self.processing = p
        self.agent = self.processing.agent     

        # RL training parameters, hyperparameters
        self.alpha = 0.1                                                         # learning rate
        self.gamma = 0.6                                                         # discount factor
        self.epsilon = 0.1                                                       # exploration-exploitation balance
        self.actionSpaceSize = len(self.processing.actionCodes)
        self.stateSpaceSize = len(self.processing.stateCombinations)
        self.qTable = np.zeros([self.stateSpaceSize, self.actionSpaceSize])      # initialize Q-table with zeros         
                
    def rl_qLearning(self):
        """
        Reinfocement learning algorithm.       
        """
        # reset current rewards
        self.agent.processing.monitoring["rewards"] = 0
        
        # observe current situation
        self.agent.perception.sourceSensor()  
        self.agent.perception.sinkSensor()           
        
        # get current state as a tuple
        state_t0 = tuple(self.processing.state.values())
        stateCode_t0 = self.rl_getStateCode(self.processing.stateCombinations, state_t0)
        
        # get current action
        actionCode_t0 = self.rl_getNextActionCode(self.qTable, stateCode_t0, self.actionSpaceSize, self.epsilon)
        
        # perform current action
        self.rl_performAction(actionCode_t0)

        # get reward for performing action[action_t0] in the current state
        reward_t1 = self.agent.processing.monitoring["rewards"]
        self.agent.processing.monitoring["cumulatedRewards"] += reward_t1
        
        # get next state
        state_t1 = tuple(self.processing.state.values())
        stateCode_t1 = self.rl_getStateCode(self.processing.stateCombinations, state_t1)
                
        # calculate new Q-value
        qNew = self.rl_updateQtable(self.qTable, stateCode_t0, actionCode_t0, reward_t1, stateCode_t1, self.alpha, self.gamma)
        
        # update the Q-table
        self.qTable[stateCode_t0, actionCode_t0] = qNew
        
        

        #print(self.qTable)


    def rl_updateQtable(self, qTable, stateCode_t0, actionCode_t0, reward_t1, stateCode_t1, alpha, gamma):
        """
        Update the given qTable.
        
        Args:
            qTable          (np.array):     Q-Table array Q: state x action --> R)
            state_t0        (int):          current state code (= index in Q-table)
            actionCode_t0   (int):          action that was performed - numeric action code
            reward_t1       (int):          reward after action_t0 was performed            
            state_t1        (int):          next state code after action_t0 was performed
            alpha           (int):          learning rate            
            gamma           (int):          discount factor
            
        """        
        # get current Q-value
        qCurr = qTable[stateCode_t0, actionCode_t0]  

        # calculate the temporal difference                              
        td = reward_t1 + (gamma * np.max(qTable[stateCode_t1, :])) - qCurr
        
        # calculate the new Q-value
        qNew = qCurr + (alpha * td)
        
        # update the Q-table
        return qNew
  
    
    def rl_getStateCode(self, stateCombinations, stateTuple):
        """
        Get state code
        """
        return stateCombinations.index(stateTuple)
        

    def rl_getNextActionCode(self, qTable, stateCode, actionSpaceSize, epsilon):
        """
        Choose next action using an epsilon greedy algorithm.
        
        Returns:
            actionCode (int): numeric code that represents an action
        """
        # choose next action
        if random.uniform(0, 1) < epsilon:
            actionCode = random.randint(0, actionSpaceSize-1)       # Explore action space by choosing a random action
        else:
            actionCode = np.argmax(qTable[stateCode, :])            # Exploit learned values by choosing the best promising action
            
        return actionCode
    
        
    def rl_performAction(self, actionCode):
        """
        Perform next action by mapping the numeric action code to the action function    

        Args:
            actionCode (int): numeric code that represents an action         
        """
        # perform action
        
        if  actionCode == 0: 
            self.processing.innate.move()
            
        elif actionCode == 1: 
            tokenDetected,  affectedSource = self.agent.perception.sourceSensor()            
            self.agent.actuation.collectToken(affectedSource)
            
        elif actionCode == 2: 
            sinkDetected,  affectedSink = self.agent.perception.sinkSensor()            
            self.agent.actuation.discardToken(affectedSink)
            
        elif actionCode == 3: 
            self.processing.innate.wait()
            
        else: 
            print("No Action")    
          
        
            
            
            
            
            
            
            
            
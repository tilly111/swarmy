# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   30/05/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module implements the swarm communication. 
"""

# =============================================================================
# Imports
# =============================================================================
import math
import numpy

# =============================================================================
# Class
# =============================================================================
class Communication():
    """
    The communication object represents the scalable swarm communication based on Bluetooth Low Energy.
    
    Args:
        i (Nesting): nesting unit    
        
    The communication protocol is based on Bluetooth Low Energy Broadcaster and Observer Roles.
    The messages are spread using a publish-subscribe paradigm.
    
    ------------------------------
    Bluetooth Low Energy protocol 
    ------------------------------
    The packet structure represents a Bluetooth Low Energy broadcasting protocol.
    It complies with the [size, type, data] triplet format that is described in the BLE spec.
    BLE restriction: The advertising interval can be set between 20ms and 10.24s.
    Simulation restriction: 60 FPS = 16.67ms per Frame
    
    The packet is represented in python as a list. 
    All list items include in total 31 bytes. Packet format based triplet format of BLE advertising packet : [1,1,4, 1,1,23]
    Packet = [4, N, SMY1, 23, M, 0000, 0000, 0, 0000, 00, 000000, 00] --> 12 items including 31 bytes in total
    
    * -----------------------------------------------------------------------------------------
    * |                                  ADVERTISING DATA                                     |
    * -----------------------------------------------------------------------------------------
    * |     COMPLETE LOCAL NAME       |                  MANUFACTURER SPECIFIC DATA           |
    * -----------------------------------------------------------------------------------------
    * |  size  |  type  |     uid     |  size  |  type  |             message                 |        
    * |  0     |  1     |    [2-5]    |  6     |  7     |             [8-30]                  |
    * -----------------------------------------------------------------------------------------
    *
    * -----------------------------------------------------------------------------------
    * |                                  message [8-30]                                 |
    * -----------------------------------------------------------------------------------
    * |                       header                    |     payload     |   trailer   |
    * -----------------------------------------------------------------------------------
    * |   stamp   |  destination   |       topic        |     content     |  metadata   |
    * |   [8-11]  |    [12-15]     |      [16-20]       |     [21-28]     |   [29-30]   |
    * -----------------------------------------------------------------------------------       
    
    Stamp:          Consecutive numbers to differ between advertising packets (packet ID) or/and Current timestamp for chronological order
    Destination:    Packet Destination
    Topic:          Classification for pub-sub-pattern / Messages categorization / Message prioritization
    Content:        Placeholder for any content
    Metadata:       Trailer of the packet to ensure data integrity
    
    ----------------------------
    Publish-Subscribe paradigm
    ----------------------------
    Each agent can publish a message by advertising.
    An agent can receive diffrent contents by subscribing to message classes.        
    """
    
    def __init__(self, i):
        """
        Initialize communication object.
        """    
        
        # variables
        self.nesting = i
        self.agent = self.nesting.agent     

        # constants
        self.BROADCASTING_DURATION = 80                                     # number of steps where the outgoing message will be broadcasted
        self.ADVERTISING_RATIO = 2                                          # reductio ratio, 1 equals an advertising interval of 1/60 = 16.67ms, 2=2*16.67ms etc.    
        self.TRANSMISSION_POWER_DBM = -40                                   # output power in dBm; -40dBm equals 100nW; Every 6-dBm increase in output power doubles the possible distance
        self.SPACELOSS_2400_MHZ = 20*math.log10((3*10**8)/(2.4*10**9))
        self.BLUETOOTH_COLOR = (0,130,252)                                  # bluetooth color

        #self.SENSITIVITY_RSSI_FILTER_DBM = -40                             # RSSI filter
        self.SENSITIVITY_RSSI_FILTER_DBM = self.agent.xParams[0]            # RSSI filter
        self.SENSITIVITY_LEVEL_DBM = -103                                   # senstivity level in dBm


        # calc max broadcasting distance
        self.MAXIMUM_PATHLOSS_DBM = self.TRANSMISSION_POWER_DBM - self.SENSITIVITY_RSSI_FILTER_DBM  
        self.BROADCASTING_RANGE_MM = 10**((self.MAXIMUM_PATHLOSS_DBM - 21.98 + self.SPACELOSS_2400_MHZ)/20)*1000  # maximum path loss that a system can incur

        # communicaton variables
        self.incoming = []
        self.outgoing = []                      # List of outgoing messages. The list is emptied after each broadcast duration.
        
        self.counterReceivedMessages = 0        # counter to track received messages      
        self.counterBroadcastedMessages = 0     # counter to track number of broadcasts 
        
        self.remainingBroadcastingSteps = 0     # monitoring remaining broadcasting duration
        self.ratioMonitoring = 0                   # count number of advertisings
        
        # communication protocol: advertising packet (outgoing)
        self.NAME_SIZE = 4                      # 00 complete local name (CLN): size - 1 byte
        self.NAME_TYPE = 0x09                   # 01 CLN: type - 1 byte
        self.MANUFACTURER_SIZE = 23             # 03 manufacturer specific data (MSD): size - 1 byte
        self.MANUFACTURER_TYPE = 0xFF           # 04 MSD: type - 1 byte Type = 0xFF
        
        self.uid = self.agent.ID                # 02 CLN: data - 4 bytes
        self.stamp = 0                          # 05 MSD: data - 4 bytes
        self.destination = 0                    # 06 MSD: data - 4 bytes
        self.topic = 0                          # 07 MSD: data - 5 bytes 
        self.content = 0                        # 08 MSD: data - 8 bytes
        self.metadata = 0                       # 09 MSD: data - 2 bytes
        
        self.packet = [self.NAME_SIZE, self.NAME_TYPE, self.uid, self.MANUFACTURER_SIZE, self.MANUFACTURER_TYPE, self.stamp, self.destination, self.topic, self.content, self.metadata]

        # readable topics - consonants from left to right and back
        self.TOPIC_GENERAL       = "GNRLL"
        self.TOPIC_ACK           = "ACKNL"
        self.TOPIC_TOKEN         = "TKNNK"
        self.TOPIC_REWARD        = "RWRDD"

        # destinations
        self.DESTINATION_OMNI   = 0x00000000  # undicrected omnidirectional broadcasting
        self.DESTINATION_GROUP1 = 0x00001000  # directed communication to all members of group 1

        # publish-subscribe messaging pattern
        self.subscriptions = [self.TOPIC_TOKEN, self.TOPIC_ACK]

        # storage of token information
        self.tokens = []     # Tokens are a special piece of information. In the current configuration carrying only one token per agent is allowed. Tokens designed in a list for future application.


    def broadcast(self):
        """
        Update the broadcast procedure.
        """
        
        self.ratioMonitoring = (self.ratioMonitoring + 1) % self.ADVERTISING_RATIO
        
        # update communication on right advertising interval and only if broadcast time isn't over and a message is available
        if(self.ratioMonitoring == 0 and self.remainingBroadcastingSteps > 0 and len(self.outgoing) > 0):    
            
            # this agent's position
            x1 = self.agent.actuation.position[0]
            y1 = self.agent.actuation.position[1]

            # start a broadcast
            self.counterBroadcastedMessages += 1
            for agent in self.agent.agents:
                    if(self.agent.ID != agent.ID): 
                        
                        # other agent's position       
                        x2 = agent.actuation.position[0]
                        y2 = agent.actuation.position[1]
                        
                        # calculate the distance
                        distance_mm = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                        distance_m = distance_mm * 10**(-3)
                        #print(distance_m)
                        
                        # calculate path loss
                        pathLoss = 21.98 - self.SPACELOSS_2400_MHZ + 20*math.log10(distance_m)
                        
                        # calculate rssi
                        rssi = self.TRANSMISSION_POWER_DBM - pathLoss
                        agent.nesting.communication.startScanning(rssi, self.outgoing[0]) # receiveMessage function of other agent
    
            # decrement broadcasting time
            self.remainingBroadcastingSteps -= 1  
            
            # reset outgoing broadcasting messages if broadcasting duration is over
            if(self.remainingBroadcastingSteps <= 0):
                self.stopAdvertising()

                    
    def startAdvertising(self):
        """
        Start advertising a new message.
        """ 
        self.remainingBroadcastingSteps = self.BROADCASTING_DURATION


    def startScanning(self, rssi, msg):
        """
        Start message reception depending on the RSSI value and noise level.
        
        Args:
            rssi (float): Received signal strength of broadcasting message from other agent
            msg (string): Broadcasting message from other agent
        """            
        # add noise in dBm? --> substract from rssi
        noise = numpy.random.uniform(0,10)
        rssi = rssi - noise
        if(rssi > self.SENSITIVITY_RSSI_FILTER_DBM):
            if(msg[7] in self.subscriptions): # add subscription filter
                self.incoming.append(msg)
                self.counterReceivedMessages  += 1
                #print("Agent " + str(self.agent.ID) + ": " + str(rssi) + "Message: " + msg[0])
     
    def stopAdvertising(self):
        """
        Stop advertising messages and reset outgoing messages buffer.
        """ 
        self.remainingBroadcastingSteps = 0
        self.outgoing = []
        
    def processIncomingMessages(self):
        """
        Parse and process the received packet
        
        Args:
            msg (list): received packet in BLE format
        """  
        
        # process incoming messages
        for msg in self.incoming:
        
            oID = msg[2]            # other agent's id
            stamp = msg[5]          # NOQA unique packet identifier
            destination = msg[6]    # NOQA time stamp
            topic = msg[7]          # message priority
            content = msg[8]        # message content
            metadata = msg[9]       # NOQA metadata to ensure data integrity
                   
            # other agents try to send a token
            if(topic == self.TOPIC_TOKEN): 
                if(len(self.tokens)==0):                    # agent has no tokens
                    self.tokens.append(content)             # collect the broadcasted token
                    if(self.agent.xParams[1]):
                        self.publishAcknowledge(oID, content)   # acknowledge to the other agent
                elif(content in self.tokens and self.agent.xParams[1]):               # if agent has already same token
                    self.publishAcknowledge(oID, content)   # show other agent that this token is already existent --> to avoid duplicates
                    
            # acknowledge received
            elif(topic == self.TOPIC_ACK and destination == self.agent.ID):
                if content in self.tokens:
                    self.tokens.remove(content)  # own token can be deleted, after receiving the corresponding acknowledge --> avoids also duplicates
                    self.stopAdvertising()       # broadcasted token already received by other agent --> stop Advertising
                    
        # reset incoming messages    
        self.incoming = []
        
        
    def publishToken(self):
        """
        Publish collected token, to share with other agents
        """          
        if(len(self.tokens) > 0): # token publish only possible if token is available 
            
            self.stopAdvertising()          # reset ongoing advertising          
            self.stamp += 1                 # increment packet number
            
            # prepare outgoing message
            self.packet[5] = self.stamp
            self.packet[7] = self.TOPIC_TOKEN       
            self.packet[8] = self.tokens[0]
    
            # add message to outgoing buffer and start advertising           
            self.outgoing.append(self.packet[:]) # add to list by value not by reference
            self.startAdvertising()  

    
    def publishAcknowledge(self, destination, content):
        """
        Publish acknowledge. Stop ongoing communication to enable immediate acknowledge responses.
        
        Args:
            destination (integer):  destination of the acknowledge
            content (string):       acknowledge content
        """
        
        self.stopAdvertising()          # reset ongoing advertising          
        self.stamp += 1                 # increment packet number
        
        # prepare outgoing message
        self.packet[5] = self.stamp        
        self.packet[6] = destination       
        self.packet[7] = self.TOPIC_ACK
        self.packet[8] = content 
        
        # add message to outgoing buffer and start advertising
        self.outgoing.append(self.packet[:]) # add to list by value not by reference
        self.startAdvertising()
          
        
 #%% render and helper functions
       
    def renderCommRadius(self):
        """
        Update the communication drawing. 
        """        
        # add broadcasting radius to plot list
        self.agent.environment.dynamicCircList.append([self.BLUETOOTH_COLOR, self.agent.actuation.position, self.BROADCASTING_RANGE_MM, 2])           
            
    def printTokens(self):
        """
        Print all tokens that the agent carries
        """
        print("\n------------------------------------")    

        tks = ""
        tks = tks + "Tokens in agent " + str(self.agent.ID) + ": "     
        if(len(self.tokens) > 0):
            for t in self.tokens[:-1]:
               tks = tks + t + ", "
            tks = tks + self.tokens[-1] # add last element without comma
           
        print(tks)
           

    
            
            
            
            
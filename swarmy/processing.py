# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module includes all computation procedures of an agent, e.g. its behavior in perform()
"""

# =============================================================================
# Imports
# =============================================================================
import numpy as np
import pygame

# =============================================================================
# Class
# =============================================================================
class Processing():
    """
    In the processing object all computation procedures of an agent are represented.
    
    Args:
        a (agent.py): instance of the agent
    """    
    def __init__(self, a, controller):
        """
        Initialize processing object.
        """    
        self.agent = a
        self.controller = controller


        # space for initializing timers and other variables needed for the controller
        # escape behavior
        self.escape_state = "forward"
        self.escape_turning = 0
        self.escape_timer = 0  # timer in simulation steps

        # wall follow behavior
        self.wall_follow_timer = 0
        self.wall_follow_state = "forward"
        self.wall_follow_max_timer = 2
        self.wall_follow_where_wall = ""

        # clean behavior
        self.clean_counter = 0
        self.clean_state = "escape"

        # cluster behavior
        self.cluster_counter = 0
        self.cluster_state = "forward"
        if a.agent_id < 1:
            self.cluster_max_wait = 100000  #np.random.randint(200, 10000)
        else:
            self.cluster_max_wait = np.random.randint(200, 500)
        self.cluster_max_turn = 0

        # agent behavior
        self.has_item = False
        self.item_hold = None
        self.cooldown_timer = 0

        # foraging behavior
        self.escape_nest_state = "forward"
        self.escape_nest_timer = 0
        self.escape_nest_turning = 0


    def perform(self, pressedKeys):
        """
        Here you can implement the robot controller which is executed on each robot.
        Update agent processing for one timestep.
        Robot actuation:
            self.agent.actuation.stepForward()
                drives forward for one step
            self.agent.actuation.stepBackward()
                drives backward for one step
            self.agent.actuation.turnLeft()
                turns left
            self.agent.actuation.turnRight()
                turns right
            self.agent.actuation.turnRightForward()
                ...
            self.agent.actuation.turnLeftForward()
                ...
            self.agent.actuation.processUserInput(pressedKeys)
                control the robot with the arrow keys
        """
        # for convenience read out sensors
        proximity_sensor = self.agent.perception.proximity_sensor()

        # select state based on behavior
        if self.controller == "avoid":
            proximity_sensor = proximity_sensor[0]
            state = self.avoid_controller(proximity_sensor)
        elif self.controller == "escape":
            proximity_sensor = proximity_sensor[0]
            state = self.escape_controller(proximity_sensor)
        elif self.controller == "wall_follow":
            proximity_sensor = proximity_sensor[0]
            state = self.wall_follow_controller(proximity_sensor)
        elif self.controller == "clean":
            proximity_sensor = proximity_sensor[0]
            state = self.clean_controller(proximity_sensor)
        elif self.controller == "cluster":
            state = self.cluster_controller(proximity_sensor)
        elif self.controller == "collecting_agent":
            # for the 6. task sheet
            item_sensor = self.agent.perception.item_sensor()
            state = self.collecting_agent_controller(proximity_sensor, item_sensor)
        elif self.controller == "collecting_anti_agent":
            # for the 6. task sheet
            item_sensor = self.agent.perception.item_sensor()
            state = self.collecting_anti_agent_controller(proximity_sensor, item_sensor)
        elif self.controller == "foraging":
            bumper_sensor = self.agent.perception.bumper_sensor()
            light_sensor = self.agent.perception.light_sensor()
            state = self.foraging_controller(proximity_sensor, light_sensor, bumper_sensor, pressedKeys)
        else:
            print("Controller not implemented, exiting experiment")
            exit(42)


        # actuate the robot
        if state == "forward":
            self.agent.actuation.stepForward()
        elif state == "backward":
            self.agent.actuation.stepBackward()
        elif state == "turnleft":
            self.agent.actuation.turnLeft()
        elif state == "turnright":
            self.agent.actuation.turnRight()
        elif state == "turnrightforward":
            self.agent.actuation.turnRightForward()
        elif state == "turnleftforward":
            self.agent.actuation.turnLeftForward()
        elif state == "wait":
            self.agent.actuation.wait()
        elif state is None:
            pass
        else:
            print("bad state")
            self.agent.actuation.processUserInput(pressedKeys)

        # track robot
        if self.agent.track:
            if self.agent.visited[int(self.agent.actuation.position[0]*100/750), int(self.agent.actuation.position[1]*100/750)] == 0:
                print("enters")
                self.agent.visited[int(self.agent.actuation.position[0]*100/750), int(self.agent.actuation.position[1]*100/750)] = 1

                rect = pygame.Rect(0, 0, 30, 30)
                rect.centerx = int(self.agent.actuation.position[0])
                rect.centery = int(self.agent.actuation.position[1])
                self.agent.environment.staticVisitedList.append([(255, 255, 0), rect, 0])


    def escape_controller(self, prox_s):
        if self.escape_state == "forward" and (prox_s[1] > 0.5 or prox_s[0] > 0.5 or prox_s[2] > 0.5):
            self.escape_state = "backward"
            self.escape_timer = np.random.randint(5, 10)
        elif self.escape_state == "backward" and self.escape_timer <= 0:
            self.escape_turning = np.random.randint(0, 2)
            if self.escape_turning == 0:
                self.escape_state = "turnleft"
            elif self.escape_turning == 1:
                self.escape_state = "turnright"
            else:
                print("out of bounds")
            self.escape_timer = np.random.randint(17, 35)
        elif (self.escape_state == "turnleft" or self.escape_state == "turnright") and self.escape_timer <= 0:
            self.escape_state = "forward"
            self.escape_timer = 0

        self.escape_timer -= 1

        return self.escape_state


    def avoid_controller(self, prox_s):
        if prox_s[0] > 0.5:
            return "turnrightforward"
        elif prox_s[2] > 0.5:
            return "turnleftforward"
        else:
            return "forward"


    def wall_follow_controller(self, prox_s):

        # wall lost
        if self.wall_follow_max_timer > 100:
            self.wall_follow_state = "searching"

        if prox_s[2] > 0.5 and not self.wall_follow_state == "turnright":
            self.wall_follow_state = "turnright"
            self.wall_follow_max_timer += 1
            self.wall_follow_where_wall = "r"
            self.wall_follow_timer = 0
            self.wall_follow_max_timer = 0
            return "turnleft"
        elif prox_s[0] > 0.5 and not self.wall_follow_state == "turnright":
            self.wall_follow_state = "turnright"
            self.wall_follow_where_wall = "l"
            self.wall_follow_timer = 0
            self.wall_follow_max_timer = 0
            return "turnright"
        elif self.wall_follow_state == "turnright":
            self.wall_follow_timer += 1
            self.wall_follow_max_timer += 1

            if self.wall_follow_timer > 10:
                self.wall_follow_timer = 0
                self.wall_follow_state = "forward"

            return "turnright"
        elif self.wall_follow_state == "forward":
            self.wall_follow_timer += 1
            self.wall_follow_max_timer += 1

            if self.wall_follow_timer > 2:
                # self.wall_follow_max_timer += 1
                self.wall_follow_timer = 0
                self.wall_follow_state = "turnleft"

            return "forward"
        elif self.wall_follow_state == "turnleft":
            self.wall_follow_timer += 1
            self.wall_follow_max_timer += 1

            if self.wall_follow_timer > 2:
                self.wall_follow_timer = 0
                self.wall_follow_state = "forward"
            if self.wall_follow_where_wall == "l":
                return "turnleft"
            elif self.wall_follow_where_wall == "r":
                return "turnright"
            else:
                print("something wrong!")
        elif self.wall_follow_state == "searching":
            return "forward"
        else:
            print("error in wall follow controller, exiting....")
            exit(42)


    def clean_controller(self, prox_s):
        if self.clean_state == "escape" and self.clean_counter < 1500:
            self.clean_counter += 1

            if self.clean_counter == 1500:
                self.clean_state = "wall_follow"
                self.clean_counter = np.random.randint(0, 1000)

            return self.escape_controller(prox_s)
        elif self.clean_state == "wall_follow" and self.clean_counter < 1500:
            self.clean_counter += 1

            if self.clean_counter == 1500:
                self.clean_state = "escape"
                self.clean_counter = np.random.randint(0, 1000)

            return self.wall_follow_controller(prox_s)
        else:
            print("something wrong in clean controller, exiting...")
            exit(42)


    def cluster_controller(self, prox_s):
        static_prox = prox_s[0]
        dynamic_prox = prox_s[1]

        # "hardware protection"
        state = self.escape_controller(static_prox)

        counter = 0
        cluster_state = ""
        if state == "forward":
            if (dynamic_prox[0] > 0.5 or dynamic_prox[1] > 0.5 or dynamic_prox[2] > 0.5) and self.cluster_state == "forward":  # we see robot
                self.cluster_state = "wait"
                self.cluster_counter = 0
                state = "wait"
            elif self.cluster_state == "wait":
                self.cluster_counter += 1
                state = "wait"
                if self.cluster_counter > self.cluster_max_wait:
                    self.cluster_state = "avoiding"
                    self.cluster_counter = 0
                    self.cluster_max_turn = np.random.randint(20, 50)
            elif self.cluster_state == "avoiding":
                self.cluster_counter += 1
                state = "turnright"
                if self.cluster_counter > self.cluster_max_turn:
                    self.cluster_state = "forward"
                    self.cluster_counter = 0

        return state


    def collecting_agent_controller(self, prox_s, item_s):
        # pick up object
        # print(item_s[2])
        if not self.has_item:
            # if item is in range
            if item_s[0]:
                # TODO some strategy to pick item up
                if self.cooldown_timer == 0 and item_s[2] < 0.5:
                    # pick up item
                    self.item_hold = item_s[1]  # robot knows item
                    self.has_item = True  # robot has item flag
                    item_s[1].holding_robot = self.agent  # item knows robot
                    item_s[1].picked_up = True  # item knows piked up
                    self.cooldown_timer = 50
        else:
            # TODO strategy to drop item
            if item_s[0] and self.cooldown_timer == 0 and item_s[2] >= 0.2:
                # drop item
                self.item_hold.holding_robot = None
                self.item_hold.picked_up = False
                self.item_hold = None
                self.has_item = False
                self.cooldown_timer = 100

        # handle cooldown controller
        if self.cooldown_timer == 0:
            pass
        else:
            self.cooldown_timer -= 1

        static_prox = prox_s[0]
        dynamic_prox = prox_s[1]

        # "hardware protection"
        state = self.escape_controller(static_prox)

        if state == "forward":
            state = self.avoid_controller(dynamic_prox)

        return state


    def collecting_anti_agent_controller(self, prox_s, item_s):
        # pick up object
        # print(item_s[2])
        if not self.has_item:
            # if item is in range
            if item_s[0]:
                # TODO some strategy to pick item up
                if self.cooldown_timer == 0 and item_s[2] > 0.5:
                    # pick up item
                    self.item_hold = item_s[1]  # robot knows item
                    self.has_item = True  # robot has item flag
                    item_s[1].holding_robot = self.agent  # item knows robot
                    item_s[1].picked_up = True  # item knows piked up
                    self.cooldown_timer = np.random.randint(50, 300)
        else:
            # TODO strategy to drop item
            if self.cooldown_timer == 0 and item_s[2] < 0.2:  # item_s[0] and
                # drop item
                self.item_hold.holding_robot = None
                self.item_hold.picked_up = False
                self.item_hold = None
                self.has_item = False
                self.cooldown_timer = 100

        # handle cooldown controller
        if self.cooldown_timer == 0:
            pass
        else:
            self.cooldown_timer -= 1

        static_prox = prox_s[0]
        dynamic_prox = prox_s[1]

        # "hardware protection"
        state = self.escape_controller(static_prox)

        # TODO add avoid other robots
        if state == "forward":
            state = self.avoid_controller(dynamic_prox)

        return state


    def foraging_controller(self, prox_s, light_s, bumper_sensor, pressedKeys):
        # TODO for debugging
        # self.agent.actuation.processUserInput(pressedKeys)
        # print(f"sensor {light_s[0]} {light_s[1]}")
        # return None

        # print(f"Number of pushing objects: {len(bumper_sensor)}")
        if len(bumper_sensor) > 0:  # objects to push
            for items in bumper_sensor:
                items.pushing_robots.append(self.agent)

        static_prox = prox_s[0]
        dynamic_prox = prox_s[1]
        # "hardware protection"
        state = self.escape_controller(static_prox)

        # TODO add avoid other robots
        if state == "forward":
            state = self.avoid_controller(dynamic_prox)
        # print(f"data {light_s[0] - light_s[1]}")
        if state == "forward":
            if (len(bumper_sensor) > 0 and light_s[0] > 0.9 and light_s[1] > 0.9) or not (self.escape_nest_state == "forward"):  # escape objects from nest site
                print("ESCAPE MID")
                if self.escape_nest_state == "forward":  #and (prox_s[1] > 0.5 or prox_s[0] > 0.5 or prox_s[2] > 0.5)
                    self.escape_nest_state = "backward"
                    self.escape_nest_timer = np.random.randint(5, 10)
                elif self.escape_nest_state == "backward" and self.escape_nest_timer <= 0:
                    self.escape_nest_turning = np.random.randint(0, 2)
                    if self.escape_nest_turning == 0:
                        self.escape_nest_state = "turnleft"
                    elif self.escape_nest_turning == 1:
                        self.escape_nest_state = "turnright"
                    else:
                        print("out of bounds")
                    self.escape_nest_timer = np.random.randint(17, 35)
                elif (self.escape_nest_state == "turnleft" or self.escape_nest_state == "turnright") and self.escape_nest_timer <= 0:
                    self.escape_nest_state = "forward"
                    self.escape_nest_timer = 0

                self.escape_nest_timer -= 1
                state = self.escape_nest_state
            elif len(bumper_sensor) > 0 and light_s[0] < 0.9 and light_s[1] < 0.9:  # pushing objects
                if light_s[0] - light_s[1] < 0.001:
                    state = "turnleft"
                elif light_s[1] - light_s[0] < 0.001:
                    state = "turnright"
                else:
                    state = "forward"

        return state

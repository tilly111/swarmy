# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   12/04/2022 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module represents the energy budget of an agent.
"""

# =============================================================================
# Class
# =============================================================================
class Energy():
    """
    The energy object represents the energy budget and takes the current consumption from
    all different swarm robot parts into account.
    
    Args:
        a (agent.py): instance of the agent    
    """
    def __init__(self, a):
        """
        Initialize energy object.
        """          
        # variables
        self.agent = a
        self.battery = 380               # initial battery capacity in mAh

    	# Estimate consumption for each module
        self.consumption = []            # consumption in mA
        self.consumption.append(5)       # processor consumption in mA
        self.consumption.append(5)       # sensor x consumption in mA
        self.consumption.append(50)      # motor y consumption in mA
        self.consumption.append(15)      # radio consumption in mA

        self.totalConsumption = sum(self.consumption)                       # average power consumption in mA
        self.hoursPerStep = 1/self.agent.environment.FPS/60/60              # one simulation step represented in hours
        self.capacityDischarge = self.totalConsumption * self.hoursPerStep  # amount of battery discharge per step

    def dischargeBatteryOneStep(self):
        """
        Battery power consumption for one simulation step.
        """
        self.battery -= self.capacityDischarge

    def dischargeBattery(self, mAh):
        """
        Consume battery power --> Decrease battery capacity.

        Args:
            amount (int): consumption in mAh
        """
        
        self.battery -= mAh

    def chargeBattery(self, mAh):
        """
        Consume battery power --> Decrease battery capacity.

        Args:
            amount (int): consumption in mAh
        """
        self.battery += mAh

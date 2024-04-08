# Swarmy - the simple simulator
`swarmy` is a [pygame](https://www.pygame.org/news) based simulator.

## Get started
Run `python3 workspace.py` to start the simulator. You can customize the size of the environment, background color and number of agents in the `config.yaml` file. To implement your own controllers, you can use the template in `my_controller.py` which overwrites the abstract method of the Actuation class. To implement your own sensors, you can use the template in `my_sensors.py` which overwrites the abstract method of the Perception class. You can also add static objects, like walls, and dynamic objects in the environment. You can implement objects in `World.py` which overwrites the abstract method of Environment class.


Don't forget to import your implemented sensors, world and controller to `workspace.py`:

```
from controller.my_controller import MyController
from Sensors.my_sensors import MySensor
from world.my_world import my_environment
```

## File structure
```
.
+-- swarmy 
+-- controller
|   +-- my_controller.py
+-- world
|   +-- my_world.py
+-- sensor
|   +-- my_sensor.py
+-- agent
|   +-- my_agent.py
++-- workspace.py
```

- `swarmy` - the main folder of the simulator (as a user you should not care about it)
- `controller` - the folder for the controller which includes your controller implementations, it overwrites the abstract methods in Actuation class
- `world` - the main folder for implementing your world, it overwrites the abstract methods in Environment class, you can implement static and dynamic objects
- `sensor` - folder implements the sensor
- `agent` - folder implementing the agent (the robot)
- - `workspace.py` - example on how to invoke the simulator
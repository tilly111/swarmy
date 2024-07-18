# Swarmy - the simple simulator
`swarmy` is a [pygame](https://www.pygame.org/news) based simulator.

## Get started
Run `python3 workspace.py` to start the simulator. By default you are able control one robot using the arrow-keys. 
Use the `config.yaml` to set parameters such as size of the enviornment or the number of agens.
 To implement your own controllers, you can use the template in `my_controller.py` which overwrites the abstract method of the swarmy internal Actuation class. To implement your own sensors, you can use the template in `my_sensors.py` which overwrites the abstract method of the swarmy internal perception class. Static objects, like walls, or dynamic objects in the environment should be implemented in `my_world.py` which overwrites the abstract method of swarmys internal environment class. In the course of the exercises, different worlds, controllers or sensors may be tested. In particular, different types of sensors are used at the same time. To keep it well organized, it is highly recommended to implement a separate class for each controller, world and sensor and to import the classes you want to use in the respective runs in `workspace.py`.
 
Don't forget to import your implemented sensors, world and controller to `workspace.py`:

```
from controller.my_controller import MyController
from Sensors.my_sensors import MySensor
from world.my_world import my_environment
```

## One possible file structure
```
.
+-- swarmy 
+-- controller
|   +-- my_first_controller.py
|   +-- my_second_controller.py
|   +-- ...
+-- world
|   +-- my_first_world.py
|   +-- my_second_world.py
|   +-- ...
+-- sensor
|   +-- my_first_sensor.py
|   +-- my_second_sensor.py
|   +-- ...
+-- agent
|   +-- my_agent.py
++-- workspace.py
```

- `swarmy` - the main folder of the simulator (as a user you should not care about it)
- `controller` - the folder for the controller which includes your controller implementations, it overwrites the abstract methods in Actuation class
- `world` - the main folder for implementing your world, it overwrites the abstract methods in Environment class, you can implement static and dynamic objects
- `sensor` - folder implements the sensor
- `agent` - folder implementing the agent (the robot)
- `workspace.py` - example on how to invoke the simulator

## Credit
This simulator is based on `swarmy` by Samer Al-Magazachi. The original version can be found on [`original_version`](https://github.com/tilly111/swarmy/tree/original_version).

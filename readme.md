# Swarmy - the simple simulator

## Get started
TODO: here we need a simple explanation on how to get started with the simulator.


## File structure
```
.
+-- swarmy 
+-- controller
|   +-- abstract_controller.py
|   +-- user_controller.py
+-- world
|   +-- abstract_world.py
|   +-- user_world.py
+-- object
|   +-- abstract_fix_object.py
|   +-- abstract_movable_object.py
|   +-- user_object.py
+-- sensor
|   +-- abstract_sensor.py
|   +-- user_sensor.py
+-- agent
|   +-- abstract_agent.py
|   +-- user_agent.py
++-- workspace.py
```

- `swarmy` - the main folder of the simulator (as a user you should not care about it)
- `controller` - the main folder of the controller should include an abstract class on how to implement a 
controller + the user controller
- `world` - folder containing abstract class on how to implement a world and user world files 
- `object` - folder implementing the objects of the world
- `sensor` - folder implements the sensor
- `agent` - folder implementing the agent (the robot)
- - `workspace.py` - example on how to invoke the simulator
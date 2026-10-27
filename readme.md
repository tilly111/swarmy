# Swarmy - the simple simulator
`swarmy` is a [pygame](https://www.pygame.org/news) based simulator.

## Setup
Create a virtual environment and install the requirements (once):

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Activate the virtual environment with `source .venv/bin/activate` every time you open a new terminal.

## Get started
Run `python3 workspace.py` to start the simulator. By default you are able to steer the robots using the arrow keys.
Use the `config.yaml` to set parameters such as size of the environment or the number of agents.
To implement your own controllers, you can use the template in `my_controller.py` which overwrites the abstract method of the swarmy internal Actuation class. To implement your own sensors, you can use the template in `bumper_sensor.py` which overwrites the abstract method of the swarmy internal perception class. Static objects, like walls, or dynamic objects in the environment should be implemented in `my_environment.py` which overwrites the abstract method of swarmy's internal environment class. In the course of the exercises, different environments, controllers or sensors may be tested. In particular, different types of sensors are used at the same time. To keep it well organized, it is highly recommended to implement a separate class for each controller, environment and sensor and to import the classes you want to use in the respective runs in `workspace.py`.

Don't forget to import your implemented sensors, environment, controller and agent to `workspace.py`:

```
from controller.my_controller import MyController
from sensors.bumper_sensor import BumperSensor
from environment.my_environment import MyEnvironment
from agent.my_agent import MyAgent
```

## One possible file structure
```
.
+-- swarmy
+-- controller
|   +-- my_first_controller.py
|   +-- my_second_controller.py
|   +-- ...
+-- environment
|   +-- my_first_environment.py
|   +-- my_second_environment.py
|   +-- ...
+-- sensors
|   +-- my_first_sensor.py
|   +-- my_second_sensor.py
|   +-- ...
+-- agent
|   +-- my_agent.py
+-- workspace.py
```

- `swarmy` - the main folder of the simulator (as a user you should not care about it)
- `controller` - the folder for the controller which includes your controller implementations, it overwrites the abstract methods in Actuation class
- `environment` - the folder for implementing your environment, it overwrites the abstract methods in Environment class, you can implement static and dynamic objects
- `sensors` - folder implementing the sensors
- `agent` - folder implementing the agent (the robot)
- `workspace.py` - example on how to invoke the simulator

## Credit
This simulator is based on `swarmy` by Samer Al-Magazachi. The original version can be found on [`original_version`](https://github.com/tilly111/swarmy/tree/original_version).

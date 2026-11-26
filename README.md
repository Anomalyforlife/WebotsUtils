# Webots utility PROTOs and controllers

Reusable objects and controller helpers for Webots.

## Ball Tee

- [protos/BallTee.proto](protos/BallTee.proto): reusable ball tee.
- [worlds/pioneer3dx_gripper_reverse.wbt](worlds/pioneer3dx_gripper_reverse.wbt): example world.

The tee exposes color and dimension fields. Its concave plate uses a compact collision mesh; the example world configures the matching contact material.

## Door

- [protos/Door.proto](protos/Door.proto): reusable 0.5 m door panel with configurable pose, size, and color (10 cm default thickness).
- [controllers/pioneer3dx_door_controller/door_controller.py](controllers/pioneer3dx_door_controller/door_controller.py): reusable Supervisor helper.
- [controllers/pioneer3dx_door_controller/pioneer3dx_door_controller.py](controllers/pioneer3dx_door_controller/pioneer3dx_door_controller.py): Pioneer example with keyboard controls.

### Import the door

    IMPORTABLE EXTERNPROTO "https://raw.githubusercontent.com/Anomalyforlife/WebotsUtils/master/protos/Door.proto"

    DEF DOOR Door {
      translation 1.7 0.25 0.2
      rotation 0 0 1 -1.5707953071795862
      size 0.5 0.1 0.4
    }

### Control it from Python

Set the robot's supervisor field to TRUE. Keep door_controller.py beside your robot controller, then use:

    from controller import Supervisor
    from door_controller import DoorController

    robot = Supervisor()
    door = DoorController(robot, "DOOR")

    # Call these when the robot decides to change the door state.
    door.open_door()
    door.close_door()

    # Call every simulation step to animate movement.
    door.update()

The example controller also maps O to open and C to close. In the SquareDoor layout, the closed panel fills the 0.5 m opening; when open, its inner end is flush with the wall face at x = 1.70 m.

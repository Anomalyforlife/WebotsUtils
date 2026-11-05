# Ball Tee for Webots

Reusable Webots PROTO based on the red and blue tee objects from the Pioneer 3DX world.

## Files

- [protos/BallTee.proto](protos/BallTee.proto): reusable object.
- [worlds/pioneer3dx_gripper_reverse.wbt](worlds/pioneer3dx_gripper_reverse.wbt): example world with both tees.

## Customizable fields

- `translation`, `rotation`, and `name`
- `plateColor`: concave plate color
- `color`: stem and conical top color
- `stemHeight`, `stemRadius`, `headRadius`, and `headHeight`: dimensions in meters
- `headBottom`: enables or disables the cone's bottom face
- `contactMaterial`: Webots contact material name

The concave plate keeps its original dimensions and uses an 8-section mesh (25 vertices), reducing collision points below Webots’ 32-joint contact limit.

## Import from GitHub

Add this declaration near the top of a world file:

```webots
IMPORTABLE EXTERNPROTO "https://raw.githubusercontent.com/Anomalyforlife/WebotsUtils/master/protos/BallTee.proto"
```

Webots makes `BallTee` available through its node import/add menu. You can also add a `BallTee {}` node directly. The example world shows red and blue instances.

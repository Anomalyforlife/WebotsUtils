"""Supervisor helper for animating a Door PROTO instance around its Z-axis hinge."""

import math


class DoorController:
    """Animate a DEF-named Door node using its exposed pose and size fields."""

    def __init__(self, supervisor, def_name="DOOR", opening_angle=math.pi / 2.0, angular_step=0.04):
        self.node = supervisor.getFromDef(def_name)
        if self.node is None:
            raise RuntimeError("Door node with DEF %r was not found" % def_name)

        self.translation = self.node.getField("translation")
        self.rotation = self.node.getField("rotation")
        size_field = self.node.getField("size")
        if self.translation is None or self.rotation is None or size_field is None:
            raise RuntimeError("Door PROTO must expose translation, rotation, and size fields")

        self.half_length = size_field.getSFVec3f()[0] / 2.0
        self.closed_position = self.translation.getSFVec3f()
        self.closed_rotation = self.rotation.getSFRotation()
        if abs(self.closed_rotation[2]) < 0.999:
            raise ValueError("DoorController expects a vertical Z-axis hinge")

        self.closed_angle = self.closed_rotation[3]
        self.open_angle = self.closed_angle + opening_angle
        self.hinge_x = self.closed_position[0] - self.half_length * math.cos(self.closed_angle)
        self.hinge_y = self.closed_position[1] - self.half_length * math.sin(self.closed_angle)
        self.angle = self.closed_angle
        self.target_angle = self.closed_angle
        self.angular_step = abs(angular_step)

    def open_door(self):
        """Start opening the door; call update() on each simulation step."""
        self.target_angle = self.open_angle

    def close_door(self):
        """Start closing the door; call update() on each simulation step."""
        self.target_angle = self.closed_angle

    def update(self):
        """Advance the door toward its target angle. Returns True while it moves."""
        difference = self.target_angle - self.angle
        if abs(difference) < 1e-9:
            return False

        self.angle += math.copysign(min(abs(difference), self.angular_step), difference)
        self.translation.setSFVec3f([
            self.hinge_x + self.half_length * math.cos(self.angle),
            self.hinge_y + self.half_length * math.sin(self.angle),
            self.closed_position[2],
        ])
        self.rotation.setSFRotation([0.0, 0.0, 1.0, self.angle])
        return True

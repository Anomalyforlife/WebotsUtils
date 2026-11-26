"""Supervisor helper for animating a Door PROTO instance around its Z-axis hinge."""

import math


class DoorController:
    """Animate a DEF-named Door node while keeping its hinge corner fixed."""

    def __init__(self, supervisor, def_name="DOOR", opening_angle=math.pi / 2.0, angular_step=0.04,
                 hinge_offset=None):
        self.node = supervisor.getFromDef(def_name)
        if self.node is None:
            raise RuntimeError("Door node with DEF %r was not found" % def_name)

        self.translation = self.node.getField("translation")
        self.rotation = self.node.getField("rotation")
        size_field = self.node.getField("size")
        if self.translation is None or self.rotation is None or size_field is None:
            raise RuntimeError("Door PROTO must expose translation, rotation, and size fields")

        size = size_field.getSFVec3f()
        self.half_length = size[0] / 2.0
        self.half_thickness = size[1] / 2.0
        self.closed_position = self.translation.getSFVec3f()
        self.closed_rotation = self.rotation.getSFRotation()
        if abs(self.closed_rotation[2]) < 0.999:
            raise ValueError("DoorController expects a vertical Z-axis hinge")

        # Local vector from hinge to panel center. Default hinge: negative-X,
        # negative-Y corner of the panel (the outer wall face in SquareDoor).
        self.hinge_offset = hinge_offset or (self.half_length, self.half_thickness)
        self.closed_angle = self.closed_rotation[3]
        self.open_angle = self.closed_angle + opening_angle
        cosine = math.cos(self.closed_angle)
        sine = math.sin(self.closed_angle)
        dx, dy = self.hinge_offset
        self.hinge_x = self.closed_position[0] - (dx * cosine - dy * sine)
        self.hinge_y = self.closed_position[1] - (dx * sine + dy * cosine)
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
        cosine = math.cos(self.angle)
        sine = math.sin(self.angle)
        dx, dy = self.hinge_offset
        self.translation.setSFVec3f([
            self.hinge_x + dx * cosine - dy * sine,
            self.hinge_y + dx * sine + dy * cosine,
            self.closed_position[2],
        ])
        self.rotation.setSFRotation([0.0, 0.0, 1.0, self.angle])
        return True

from controller import Keyboard, Supervisor
from door_controller import DoorController

MAX_SPEED = 5.24
MAX_SENSOR_VALUE = 1024.0
MIN_DISTANCE = 1.0
WHEEL_WEIGHT_THRESHOLD = 100.0
SENSOR_WEIGHTS = (
    (150, 0), (200, 0), (300, 0), (600, 0),
    (0, 600), (0, 300), (0, 200), (0, 150),
    (0, 0), (0, 0), (0, 0), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0),
)

robot = Supervisor()
time_step = int(robot.getBasicTimeStep())
left_wheel = robot.getDevice("left wheel")
right_wheel = robot.getDevice("right wheel")
left_wheel.setPosition(float("inf"))
right_wheel.setPosition(float("inf"))
left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

sensors = []
for i in range(16):
    sensor = robot.getDevice("so%d" % i)
    sensor.enable(time_step)
    sensors.append(sensor)

leds = [robot.getDevice("red led %d" % i) for i in range(1, 4)]
keyboard = Keyboard()
keyboard.enable(time_step)
door = DoorController(robot, "DOOR")

state = "FORWARD"
led_number = 0
led_delay = 0

while robot.step(time_step) != -1:
    key = keyboard.getKey()
    if key in (ord("O"), ord("o")):
        door.open_door()
    elif key in (ord("C"), ord("c")):
        door.close_door()
    door.update()

    wheel_weight_total = [0.0, 0.0]
    for sensor, weights in zip(sensors, SENSOR_WEIGHTS):
        value = sensor.getValue()
        if value == 0.0:
            speed_modifier = 0.0
        else:
            distance = 5.0 * (1.0 - value / MAX_SENSOR_VALUE)
            speed_modifier = 1.0 - distance / MIN_DISTANCE if distance < MIN_DISTANCE else 0.0
        wheel_weight_total[0] += weights[0] * speed_modifier
        wheel_weight_total[1] += weights[1] * speed_modifier

    if state == "FORWARD":
        if wheel_weight_total[0] > WHEEL_WEIGHT_THRESHOLD:
            speed = [0.7 * MAX_SPEED, -0.7 * MAX_SPEED]
            state = "LEFT"
        elif wheel_weight_total[1] > WHEEL_WEIGHT_THRESHOLD:
            speed = [-0.7 * MAX_SPEED, 0.7 * MAX_SPEED]
            state = "RIGHT"
        else:
            speed = [MAX_SPEED, MAX_SPEED]
    elif state == "LEFT":
        if max(wheel_weight_total) > WHEEL_WEIGHT_THRESHOLD:
            speed = [0.7 * MAX_SPEED, -0.7 * MAX_SPEED]
        else:
            speed = [MAX_SPEED, MAX_SPEED]
            state = "FORWARD"
    else:
        if max(wheel_weight_total) > WHEEL_WEIGHT_THRESHOLD:
            speed = [-0.7 * MAX_SPEED, 0.7 * MAX_SPEED]
        else:
            speed = [MAX_SPEED, MAX_SPEED]
            state = "FORWARD"

    led_delay += 1
    if led_delay == 70:
        leds[led_number].set(0)
        led_number = (led_number + 1) % len(leds)
        leds[led_number].set(1)
        led_delay = 0

    left_wheel.setVelocity(speed[0])
    right_wheel.setVelocity(speed[1])

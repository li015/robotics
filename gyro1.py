from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor, GyroSensor
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.media.ev3dev import Image, ImageFile, SoundFile
from pybricks.tools import wait, StopWatch


def gyro(self)
        gyro_sensor_value = self.gyro_sensor.speed()
        # Calibrate for sensitivity
         # This adds a small delay since we don't need to read these sensors
        # continuously. Reading once every 100 milliseconds is fast enough.
        self.gyro_timer.reset()
        while self.gyro_timer.time() < 100:
            yield
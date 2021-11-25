from camera import Camera
from enum import Enum
import time
import threading
import RPi.GPIO as GPIO

horizontal_servo_pin = 12
vertical_servo_pin = 13
laInput1Pin = 22
laInput2Pin = 27

class LinearAcuatorDirection(Enum):
  FORWARD = "FORWARD"
  BACKWARD = "BACKWARD"
  STOPPED = "STOPPED"

def convert_angle_to_duty_cycle(angle):
  # Convert the angle to duty cycle -90 -> 2.5 and 90 -> 12.5
  return (angle + 90) * (12.5 / 90) / 2


class NerfBlaster:
  def __init__(self):
    self.__camera = Camera()
    GPIO.setmode(GPIO.BCM)
    
    # horizontal servo
    GPIO.setup(horizontal_servo_pin, GPIO.OUT)
    self.horizontal_servo_pwm = GPIO.PWM(horizontal_servo_pin, 50)
    self.horizontal_servo_pwm.start(convert_angle_to_duty_cycle(0))

    # vertical servo
    GPIO.setup(vertical_servo_pin, GPIO.OUT)
    self.vertical_servo_pwm = GPIO.PWM(vertical_servo_pin, 50)
    self.vertical_servo_pwm.start(convert_angle_to_duty_cycle(0))

    # fire controller
    self.__fire_requested = False
    GPIO.setup(laInput1Pin, GPIO.OUT)
    GPIO.setup(laInput2Pin, GPIO.OUT)
    threading.Thread(target=self.__fire_controler, args=()).start()

  def set_horizontal_angle(self, angle):
    angle = min(max(-45, angle), 45)
    self.horizontal_servo_pwm.ChangeDutyCycle(convert_angle_to_duty_cycle(angle))
    return angle

  def set_vertical_angle(self, angle):
    angle = min(max(-25, angle), 20)
    self.vertical_servo_pwm.ChangeDutyCycle(convert_angle_to_duty_cycle(angle))
    return angle
  
  def get_image(self):
    return self.__camera.get_image()

  def set_linear_acuator_direction(self, direction):
    if direction is LinearAcuatorDirection.FORWARD:
      GPIO.output(laInput1Pin, GPIO.HIGH)
      GPIO.output(laInput2Pin, GPIO.LOW)
    elif direction is LinearAcuatorDirection.BACKWARD:
      GPIO.output(laInput1Pin, GPIO.LOW)
      GPIO.output(laInput2Pin, GPIO.HIGH)
    else:
      GPIO.output(laInput1Pin, GPIO.LOW)
      GPIO.output(laInput2Pin, GPIO.LOW)

  def fire(self):
    self.__fire_requested = True

  def __fire_controler(self):
    while True:
      print("Reloading 1")
      self.set_linear_acuator_direction(LinearAcuatorDirection.BACKWARD)
      time.sleep(6)
      self.set_linear_acuator_direction(LinearAcuatorDirection.STOPPED)
      time.sleep(0.25)
      
      print("Reloading 2")
      self.set_linear_acuator_direction(LinearAcuatorDirection.FORWARD)
      time.sleep(4)
      self.set_linear_acuator_direction(LinearAcuatorDirection.STOPPED)
      self.__fire_requested = False

      print("Ready")
      while not self.__fire_requested:
        pass

      print("Firing")
      self.set_linear_acuator_direction(LinearAcuatorDirection.FORWARD)
      time.sleep(3)

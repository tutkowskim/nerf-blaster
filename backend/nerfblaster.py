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
    self.camera = Camera()
    GPIO.setmode(GPIO.BCM)
    
    # horizontal servo
    GPIO.setup(horizontal_servo_pin, GPIO.OUT)
    self.horizontal_servo_pwm = GPIO.PWM(horizontal_servo_pin, 50)
    self.horizontal_servo_pwm.start(convert_angle_to_duty_cycle(0))
    time.sleep(0.05)
    self.horizontal_servo_pwm.ChangeDutyCycle(0)
    self.horizontal_angle = 0 

    # vertical servo
    GPIO.setup(vertical_servo_pin, GPIO.OUT)
    self.vertical_servo_pwm = GPIO.PWM(vertical_servo_pin, 50)
    self.vertical_servo_pwm.start(convert_angle_to_duty_cycle(0))
    time.sleep(0.05)
    self.vertical_servo_pwm.ChangeDutyCycle(0)
    self.vertical_angle = 0 

    # fire controller
    self.__fire_requested = False
    self.fire_controller_status = ''
    GPIO.setup(laInput1Pin, GPIO.OUT)
    GPIO.setup(laInput2Pin, GPIO.OUT)
    threading.Thread(target=self.__fire_controller, args=()).start()

    # tracking controller
    self.tracking_enabled = True
    threading.Thread(target=self.__tracking_controller, args=()).start()

  def set_horizontal_angle(self, angle):
    angle = min(max(-45, angle), 45)
    self.horizontal_servo_pwm.ChangeDutyCycle(convert_angle_to_duty_cycle(angle))
    time.sleep(0.05)
    self.horizontal_servo_pwm.ChangeDutyCycle(0)
    self.horizontal_angle = angle
    return angle

  def set_vertical_angle(self, angle):
    angle = min(max(-25, angle), 20)
    self.vertical_servo_pwm.ChangeDutyCycle(convert_angle_to_duty_cycle(angle))
    time.sleep(0.05)
    self.vertical_servo_pwm.ChangeDutyCycle(0)
    self.vertical_angle = angle
    return angle

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

  def __fire_controller(self):
    while True:
      self.fire_controller_status = 'Reloading 1'
      self.set_linear_acuator_direction(LinearAcuatorDirection.BACKWARD)
      time.sleep(6)
      self.set_linear_acuator_direction(LinearAcuatorDirection.STOPPED)
      time.sleep(0.25)
      
      self.fire_controller_status = 'Reloading 2'
      self.set_linear_acuator_direction(LinearAcuatorDirection.FORWARD)
      time.sleep(4)
      self.set_linear_acuator_direction(LinearAcuatorDirection.STOPPED)
      self.__fire_requested = False

      self.fire_controller_status = 'Ready'
      while not self.__fire_requested:
        pass

      self.fire_controller_status = 'Firing'
      self.set_linear_acuator_direction(LinearAcuatorDirection.FORWARD)
      time.sleep(3)

  def __tracking_controller(self):
    last_updated = time.time()
    while True:
      while not self.tracking_enabled:
        pass
      if self.camera.last_updated < last_updated:
        continue
      if len(self.camera.detections) <= 0:
        continue

      detection = self.camera.detections[0]
      detectionCenterX = (detection.bounding_box.right + detection.bounding_box.left) / 2.0
      detectionCenterY = (detection.bounding_box.bottom + detection.bounding_box.top) / 2.0

      print(detection.bounding_box)
      print("Person detected at ({0},{1})".format(detectionCenterX, detectionCenterY))

      if (self.camera.FRAME_HEIGHT / 2.0) - 50 > detectionCenterY:
        self.set_vertical_angle(self.vertical_angle - 1)
        print("shifting down")
      elif (self.camera.FRAME_HEIGHT / 2.0) + 50 < detectionCenterY:
        self.set_vertical_angle(self.vertical_angle + 1)
        print("shifting up")

      if (self.camera.FRAME_WIDTH / 2.0) - 10 > detectionCenterX:
        self.set_horizontal_angle(self.horizontal_angle - 1)
        print("shifting right")
      elif (self.camera.FRAME_WIDTH / 2.0) + 10 < detectionCenterX:
        self.set_horizontal_angle(self.horizontal_angle + 1)
        print("shifting left")

      last_updated = time.time()
      time.sleep(0.125)

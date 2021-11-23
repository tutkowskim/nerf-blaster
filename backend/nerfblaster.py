from camera import Camera
import RPi.GPIO as GPIO

horizontal_servo_pin = 12
vertical_servo_pin = 13


def convert_angle_to_duty_cycle(angle):
  # Convert the angle to duty cycle -90 -> 2.5 and 90 -> 12.5
  return (angle + 90) * (12.5 / 90) / 2


class NerfBlaster:
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    self.__camera = Camera()
    
    # horizontal servo
    GPIO.setup(horizontal_servo_pin, GPIO.OUT)
    self.horizontal_servo_pwm = GPIO.PWM(horizontal_servo_pin, 50)
    self.horizontal_servo_pwm.start(convert_angle_to_duty_cycle(0))

    # vertical servo
    GPIO.setup(vertical_servo_pin, GPIO.OUT)
    self.vertical_servo_pwm = GPIO.PWM(vertical_servo_pin, 50)
    self.vertical_servo_pwm.start(convert_angle_to_duty_cycle(0))

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

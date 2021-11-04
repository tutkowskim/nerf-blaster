from camera import Camera
import RPi.GPIO as GPIO

ledPin = 2 # GPIO number not pin number

class NerfBlaster:
  def __init__(self):
    self.__camera = Camera()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW) # initial state

  def turn_on_led(self):
    GPIO.output(ledPin, GPIO.LOW)

  def turn_off_led(self):
    GPIO.output(ledPin, GPIO.HIGH)
  
  def get_image(self):
    return self.__camera.get_image()

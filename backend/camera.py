from io import BytesIO
from picamera import PiCamera

class Camera:
  def __init__(self):
    self.__camera = PiCamera(resolution=(640, 480), framerate=10)
    self.__camera.start_preview()

  def get_image(self):
    stream = BytesIO()
    self.__camera.capture(stream, format='jpeg', use_video_port=True)
    return stream.getvalue()

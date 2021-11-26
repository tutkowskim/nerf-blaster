import cv2
import threading
import time
from tensorflow_example.object_detector import ObjectDetector, ObjectDetectorOptions
from tensorflow_example.utils import visualize

model = 'tensorflow_example/efficientdet_lite0_edgetpu.tflite'

class Camera():
  def __init__(self):
    self.image = None
    self.detections = []
    self.fps = -1
    self.FRAME_WIDTH = 640
    self.FRAME_HEIGHT = 480
    self.last_updated = time.time()
    
    self.cap = cv2.VideoCapture(0)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.FRAME_WIDTH)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)
  
    options = ObjectDetectorOptions(
      num_threads=3,
      score_threshold=0.3,
      max_results=1,
      label_allow_list=['person'],
      enable_edgetpu=True)
    self.detector = ObjectDetector(model_path=model, options=options)
    threading.Thread(target=self.update, args=()).start()

  def __del__(self):
    self.cap.release()

  def update(self):
    while True:
      start_time = time.time()

      success, image = self.cap.read()
      image = cv2.rotate(image, cv2.ROTATE_180)
      image = cv2.flip(image, 1)
      self.detections = self.detector.detect(image)
      image = visualize(image, self.detections)
      success, im_buf_arr = cv2.imencode(".jpg", image)
      self.image = im_buf_arr.tobytes()
      
      end_time = time.time()
      self.fps = 1 / (end_time - start_time)
      self.last_updated = end_time

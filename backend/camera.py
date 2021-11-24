import cv2
from tensorflow_example.object_detector import ObjectDetector, ObjectDetectorOptions
from tensorflow_example.utils import visualize

model = 'tensorflow_example/efficientdet_lite0_edgetpu.tflite'

class Camera():
  def __init__(self):
    self.image = None
    self.cap = cv2.VideoCapture(0)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    options = ObjectDetectorOptions(
      num_threads=3,
      score_threshold=0.3,
      max_results=3,
      label_allow_list=['person'],
      enable_edgetpu=True)
    self.detector = ObjectDetector(model_path=model, options=options)

  def __del__(self):
    self.cap.release()

  def get_image(self):
    success, image = self.cap.read()
    image = cv2.rotate(image, cv2.ROTATE_180)
    image = cv2.flip(image, 1)
    detections = self.detector.detect(image)
    image = visualize(image, detections)
    success, im_buf_arr = cv2.imencode(".jpg", image)
    self.image = im_buf_arr.tobytes()
    return self.image

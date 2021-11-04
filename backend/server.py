from gevent import monkey; monkey.patch_all()
from flask import (Flask, send_from_directory, Response)
from time import sleep
from nerfblaster import NerfBlaster

app = Flask(__name__)
nerfBlaster = NerfBlaster()

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./static', path)


@app.route('/')
def root():
  return send_from_directory('./static', './index.html')

@app.route("/api/led_on", methods = ['POST'])
def led_on():
  nerfBlaster.turn_on_led()
  return 'ok', 200

@app.route("/api/led_off", methods = ['POST'])
def led_off():
  nerfBlaster.turn_off_led()
  return 'ok', 200

@app.route("/api/image", methods = ['GET'])
def get_image():
  return nerfBlaster.get_image(), 200, {'Content-Type': 'image/jpeg' }

@app.route("/api/video", methods = ['GET'])
def car_get_video():
  # Inspired to use multipart messages for streaming by https://blog.miguelgrinberg.com/post/video-streaming-with-flask
  def gen():
    while True:
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + nerfBlaster.get_image() + b'\r\n')
        sleep(0) # Give other requests a chance to process
  return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.errorhandler(500)
def server_error(e):
  return 'An internal error occurred [main.py] %s' % e, 500

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)

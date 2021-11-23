from gevent import monkey; monkey.patch_all()
from flask import (Flask, send_from_directory, Response, request)
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

@app.route("/api/set_horizontal_angle", methods = ['POST'])
def set_horizontal_angle():
  angle = nerfBlaster.set_horizontal_angle(float(request.data))
  return str(angle), 200

@app.route("/api/set_vertical_angle", methods = ['POST'])
def set_vertical_angle():
  angle = nerfBlaster.set_vertical_angle(float(request.data))
  return str(angle), 200

@app.route("/api/image", methods = ['GET'])
def get_image():
  return nerfBlaster.get_image(), 200, {'Content-Type': 'image/jpeg' }

@app.route("/api/video", methods = ['GET'])
def car_get_video():
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
  app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

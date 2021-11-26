from flask import (Flask, stream_with_context, send_from_directory, Response, request, jsonify)
from time import sleep
from nerfblaster import NerfBlaster

app = Flask(__name__)
nerfBlaster = NerfBlaster()

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./static', path)

@app.route('/')
@app.route('/home')
@app.route('/debug')
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

@app.route("/api/fire", methods = ['POST'])
def fire_request():
  nerfBlaster.fire()
  return 'fire requested', 200

@app.route("/api/enable_tracking", methods = ['POST'])
def enable_tracking():
  nerfBlaster.tracking_enabled = True
  return 'tracking enabled', 200

@app.route("/api/disable_tracking", methods = ['POST'])
def disable_tracking():
  nerfBlaster.tracking_enabled = False
  return 'tracking disabled', 200

@app.route("/api/image", methods = ['GET'])
def get_image():
  return nerfBlaster.camera.image, 200, {'Content-Type': 'image/jpeg' }

@app.route("/api/video", methods = ['GET'])
def get_video():
  @stream_with_context
  def gen():
    while True:
      yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + nerfBlaster.camera.image + b'\r\n')
      sleep(0.05) # Give other requests a chance to process
  return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status', methods = ['GET'])
def get_status():
  return jsonify(
        verticalAngle=nerfBlaster.horizontal_angle,
        horizontalAngle=nerfBlaster.horizontal_angle,
        fireControllerStatus=nerfBlaster.fire_controller_status,
        cameraFps=nerfBlaster.camera.fps,
        trackingEnabled=nerfBlaster.tracking_enabled
    )

@app.errorhandler(500)
def server_error(e):
  return 'An internal error occurred [main.py] %s' % e, 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

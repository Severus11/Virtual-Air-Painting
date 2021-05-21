from flask import Flask, render_template, Response  
from cam import VideoCamera
app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')
def gen ():
    while True:

        
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2
import face_recognition
import pickle
import os


app = Flask(__name__)

UPLOAD_FOLDER = './known_faces'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UNKNOWN_FOLDER'] = './unknown'

@app.route('/')
def index():
    return render_template('index1.html')	
    

@app.route('/register',methods=['GET'])
def index1():
    return render_template('register.html')	

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   
@app.route('/reg',methods=['POST','GET'])
def register():
    username = request.form[username]
    print(username)
    if 'file' not in request.files:
        return "no file"
    file = request.files['file']
    if file.filename == '':
        return "no file"
    if file and allowed_file(file.filename):
        name = username+'.'+file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        return "success"
    return "failure"

@app.route('/login',methods=['GET'])
def index2():
    return render_template('login.html')	

@app.route('/log',methods=['POST','GET'])
def login():
    username = request.form['username']
    names = os.listdir('./known_faces')
    if username+'.jpg' not in names:
        return "you are not registered"
    if 'file' not in request.files:
        return "no file"
    file = request.files['file']
    if file.filename == '':
        return "no file"
    if file and allowed_file(file.filename):
        fname= os.path.join(app.config['UNKNOWN_FOLDER'], file.filename)
        file.save(fname)
        image_to_be_matched = face_recognition.load_image_file(fname)

        image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]

        current_image = face_recognition.load_image_file("./known_faces/" + username+'.jpg')
        current_image_encoded = face_recognition.face_encodings(current_image)[0]
        result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
        if result[0] == True:
            return "you are logged in!"
        else:
            return "invalid user"
    return "false"
    						
                            
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
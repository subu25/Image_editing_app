
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")

    img = cv2.imread(f"uploads/{filename}")


    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"output/{filename}"
            cv2.imwrite(newFilename, imgProcessed) 
            imS = cv2.resize(imgProcessed, (960, 540))
            cv2.imshow('GrayScale Image', imS)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return newFilename
        
        case "crot":
            imgProcessed = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            newFilename = f"output/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            imS = cv2.resize(imgProcessed, (960, 540))
            cv2.imshow('90 Degree rotated image', imS)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return newFilename
        
        case "cedge":
            imgProcessed = cv2.Canny(img,100,100)
            newFilename = f"output/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            imS = cv2.resize(imgProcessed, (960, 540))
            cv2.imshow('Edge detection', imS)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return newFilename
    pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get("operation")
       
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")


app.run(debug=True)
 
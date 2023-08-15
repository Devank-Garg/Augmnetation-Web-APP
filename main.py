from flask import Flask, render_template, request,url_for, flash
import os
import cv2

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'mysecretkey1234567890'


UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def imageprocess(filename):
    img=cv2.imread(f'static/uploads/{filename}')
    processed_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    processed_filename = 'processed_' + filename
    cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], processed_filename), processed_img)
    print(processed_filename)
    return processed_filename


@app.route('/')

def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/edit', methods=['GET', 'POST'])

def edit():
    if request.method=='POST':
        
        if 'file' not in request.files:
            flash('No file part')
            return 'File not present'
        file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'File not selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processed_filename = imageprocess(filename)
            processed_image_path = 'static/processed/' + processed_filename
            uploaded_image_path = 'static/uploads/' + filename
            return render_template('tool.html', uploaded_image_path=uploaded_image_path, processed_image_path=processed_image_path)



if __name__ == "__main__":
    app.run(debug=True)

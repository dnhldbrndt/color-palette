import numpy as np 
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

print("Ready.")

def get_colors ():
    return 


# Home Route
@app.route('/', methods=['GET', 'POST'])
def go_home():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('home.html', img=img)
    return render_template('home.html')


# Upload Image   
def upload_file():
    file = request.files['img']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD'], filename))
    img = os.path.join(app.config['UPLOAD'], filename)
    return img
   
   
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
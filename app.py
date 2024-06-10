import numpy as np 
import os
 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from numpy import asarray

app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

print("Ready.")

# Get color palette
def get_colors (filename, min_distance=15):
    color_list = []
    color_dict = {}
    
    img_array = Image.open("static/uploads/" + filename)
    np_img_array = np.array(img_array)
    print(type(np_img_array))
    print(np_img_array.shape)
    
    for column in np_img_array: 
        for rgb in column: 
            t_rgb = tuple(rgb) 
            if t_rgb not in color_dict: 
                color_dict[t_rgb] = 0
            if t_rgb in color_dict: 
                color_dict[t_rgb] += 1
    # print(color_dict)
    sorted_colors = dict(sorted(color_dict.items(), key=lambda x: x[1], reverse=True))
    sorted_colors = list(sorted_colors.keys())
    
    
    for color in sorted_colors:
        if not color_list:
            color_list.append(color)
        else:
            if all(color_distance(color, existing_color) >= min_distance for existing_color in color_list):
                color_list.append(color)
            if len(color_list) >= 10:
                break
    color_list = color_list[0:10]
    print(color_list)
    return color_list

# Convert RGB to Hex
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
# Function to calculate Euclidean distance between two RGB colors
def color_distance(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

# Home Route
@app.route('/', methods=['GET', 'POST'])
def go_home():
    if request.method == 'POST':
        tuple_img = upload_file()
        img = tuple_img[0]
        filename = tuple_img[1]
        colors_list = get_colors(filename)
        hex_list = []
        render_colors = []
        for color in colors_list:
            hex_value = rgb_to_hex(color)
            tmp_color = {'rgb': color, 'hex':hex_value}
            hex_list.append(hex_value) 
            render_colors.append(tmp_color)
        return render_template('home.html', img=img, colors_list=colors_list, render_colors=render_colors, hex_list=hex_list )
    return render_template('home.html')


# Upload Image   
def upload_file():
    file = request.files['img']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD'], filename))
    img = os.path.join(app.config['UPLOAD'], filename)  
    return tuple([img, filename])
   
   
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
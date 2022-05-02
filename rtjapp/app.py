# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 15:02:52 2022

@author: cazen
"""

# -*- coding: utf-8 -*-
from flask import Flask, render_template
import os

IMG_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMG_FOLDER


@app.route("/index/")
def index():
    return render_template("index.html")
@app.route("/djoe/")
def djoe():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'djoe.jpg')
    return render_template("djoe.html", user_image = full_filename)

if __name__ == "__main__":
    app.run(debug=True)
# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GL-M0Jqk99KgHgHDa8Fx6U6bG2hcI-7W
"""

# coding=utf-8
import sys
import os
import numpy as np
from flask_ngrok import run_with_ngrok

# Keras
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)
run_with_ngrok(app)

# Model saved with Keras model.save()
MODEL_PATH = 'my_cifar10_model.h5'

global model
# Load your trained model
model = load_model(MODEL_PATH)      # Necessary
# print('Model loaded. Start serving...')
print('Model loaded. Check http://127.0.0.1:5000/')

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>') 
def prediction(filename):
    #Step 1
    my_image = plt.imread(os.path.join('uploads', filename))
    #Step 2
    my_image_re = resize(my_image, (32,32,3))
    
    #Step 3
    probabilities = model.predict(np.array( [my_image_re,] ))[0,:]
    print(probabilities)
    #Step 4
    number_to_class = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 
'truck']
    index = np.argsort(probabilities)
    predictions = {
      "class1":number_to_class[index[9]],
      "class2":number_to_class[index[8]],
      "class3":number_to_class[index[7]],
      "prob1":probabilities[index[9]],
      "prob2":probabilities[index[8]],
      "prob3":probabilities[index[7]],
    }
    #Step 5
    return render_template('predict.html', predictions=predictions)


app.run()


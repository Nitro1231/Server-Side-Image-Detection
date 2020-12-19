import os
import imutils
import cv2 as cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from matplotlib import pyplot as plt

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            if file.filename == '':
                return redirect(redirect.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item_search(f'./uploads/{filename}')

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=files[] multiple="">
      <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def item_search(target_image):
    threshold = 0.9
    image_o = cv2.imread(target_image)
    image = cv2.cvtColor(image_o, cv2.COLOR_BGR2GRAY)

    for temp in os.listdir('./items'):
        t = f'./items/{temp}'
        #t = f'./items/Fowl.png'
        print(t)

        template = cv2.imread(t, cv2.IMREAD_UNCHANGED)
        #noise = np.zeros(template.shape, dtype=np.uint8)
        #noise = cv2.randu(noise, 0, 255)
        #new = cv2.add(noise, template)
        #cv2.imshow("t", new)
    
        #cv2.imshow('t', template)
        th, tw, c = template.shape
        template = template[int(tw/3):int(tw/3*2), int(th/3):int(th/3*2)]
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        cv2.imshow('Temp', template)
        
        loc = False
        w, h = template.shape[::-1]
        for scale in np.linspace(0.4, 0.8, 20)[::-1]:
            resized = imutils.resize(template, width = int(template.shape[1] * scale))
            w, h = resized.shape[::-1]
            res = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)

            loc = np.where( res >= threshold)
            if len(list(zip(*loc[::-1]))) > 0:
                break

        if loc and len(list(zip(*loc[::-1]))) > 0:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(image_o, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                break

        break
    
    cv2.imshow('Output', image_o)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
   app.run(debug = True)
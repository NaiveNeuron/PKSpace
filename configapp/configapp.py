import os
import json

from flask import (Flask, render_template, send_from_directory, request,
                   redirect, url_for)

app = Flask(__name__)
app.config.from_object('configapp.default_settings')

filedir = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(filedir, app.config['IMAGE_PATH'])
dataset_dir = os.path.join(filedir, app.config['DATASET_PATH'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/marker', methods=['GET', 'POST'])
def marker():
    if request.method == 'POST':
        if 'output' in request.form:
            polygons = request.form.get('output')
            with open(os.path.join(filedir, 'polygons.json'), 'w+') as f:
                f.write(polygons)
            return redirect(url_for('labeler'))

    files = []
    listdir = os.listdir(directory)
    for f in listdir:
        if f.endswith(app.config['IMAGE_SUFFIX']):
            files.append(f)

    return render_template('marker.html', images=files)
    

@app.route('/labeler', methods=['GET', 'POST'])
def labeler():
    try:
        with open(os.path.join(filedir, 'polygons.json')) as f:
            data = json.load(f)
        polygons = data['polygons']
    except IOError:
        return render_template('labeler.html', nojson=True)

    data = []
    # we assume that directory walked contains DATE/TIME.png files
    # othewise it may crash -- needs some testing
    subdirs = [d for d in os.listdir(dataset_dir)
                    if os.path.isdir(os.path.join(dataset_dir, d))]
            
    for subdir in subdirs:
        for f in os.listdir(os.path.join(dataset_dir, subdir)):
            if f.endswith(app.config['IMAGE_SUFFIX']):
                data.append(os.path.join(subdir, f))

    return render_template('labeler.html', imgs=data)


@app.route('/image/<path:filename>')
def data_image(filename):
    return send_from_directory(directory, filename)


@app.route('/datasetimg/<path:img>')
def dataset_image(img):
    img = img.split('/')
    return send_from_directory(os.path.join(dataset_dir, img[0]), img[1])


if __name__ == '__main__':
    app.run()

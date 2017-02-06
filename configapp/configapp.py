import os
import json
import datetime

from flask import (Flask, render_template, send_from_directory, request,
                   redirect, url_for, jsonify)

app = Flask(__name__)
app.config.from_object('configapp.default_settings')

filedir = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(filedir, app.config['IMAGE_PATH'])
dataset_dir = os.path.join(filedir, app.config['DATASET_PATH'])
mask_dir = os.path.join(filedir, app.config['MASK_PATH'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/live')
def live():
    return render_template('live.html')


@app.route('/marker/mask/<path:filename>')
def get_mask(filename):
    mask = os.path.join(mask_dir, filename)
    if os.path.isfile(mask):
        with open(mask) as f:
            polygons = json.load(f)['polygons']
        return jsonify(result='OK', polygons=polygons)
    return jsonify(result='FAIL')


@app.route('/marker', methods=['GET', 'POST'])
def marker():
    if request.method == 'POST':
        if 'output' in request.form:
            polygons = request.form.get('output')
            filename = request.form.get('filename')
            if filename == '':
                filename = str(datetime.datetime.now())

            filename += '.json'
            with open(os.path.join(mask_dir, filename), 'w+') as f:
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
    masks = []
    for f in os.listdir(mask_dir):
        if f.endswith('.json'):
            masks.append(f)

    if not masks:
        return render_template('labeler.html', nojson=True)

    data = {}
    # we assume that directory walked contains DATE/TIME.png files
    # othewise it may crash -- needs some testing
    subdirs = [d for d in os.listdir(dataset_dir)
                    if os.path.isdir(os.path.join(dataset_dir, d))]
            
    for subdir in subdirs:
        data[subdir] = []
        for f in os.listdir(os.path.join(dataset_dir, subdir)):
            img = os.path.join(subdir, f)
            js = os.path.join(dataset_dir,
                              img[:-len(app.config['IMAGE_SUFFIX'])+1]+'json')
            
            labeled = False
            if os.path.isfile(js):
                labeled = True

            if f.endswith(app.config['IMAGE_SUFFIX']):

                data[subdir].append({'src': os.path.join(subdir, f),
                                     'labeled': labeled})

    return render_template('labeler.html', imgs=data, tabs=subdirs,
                           masks=masks)


@app.route('/savelabel/<path:filename>', methods=['GET', 'POST'])
def savelabel(filename):
    if request.method == 'POST':
        js = os.path.join(dataset_dir,
                          filename[:-len(app.config['IMAGE_SUFFIX'])+1]+'json')

        with open(js, 'w+') as f:
            f.write(json.dumps(request.json['labeled']))
        return jsonify(result='OK', imgid=filename)


@app.route('/image/<path:filename>')
def data_image(filename):
    return send_from_directory(directory, filename)


@app.route('/datasetimg/<path:img>')
def dataset_image(img):
    img = img.split('/')
    return send_from_directory(os.path.join(dataset_dir, img[0]), img[1])


if __name__ == '__main__':
    app.run()

import os

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
app.config.from_object('configapp.default_settings')


@app.route('/')
def index():
    files = []
    for f in os.listdir(os.path.expanduser(app.config['IMAGE_PATH'])):
        if f.endswith(app.config['IMAGE_SUFFIX']):
            files.append(f)

    return render_template('index.html', images=files)


@app.route('/image/<path:filename>')
def data_image(filename):
    directory = os.path.expanduser(app.config['IMAGE_PATH'])
    return send_from_directory(directory, filename)

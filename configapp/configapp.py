import os

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
app.config.from_object('configapp.default_settings')

filedir = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(filedir, app.config['IMAGE_PATH'])


@app.route('/')
def index():
    files = []
    listdir = os.listdir(directory)
    for f in listdir:
        if f.endswith(app.config['IMAGE_SUFFIX']):
            files.append(f)

    return render_template('index.html', images=files)


@app.route('/image/<path:filename>')
def data_image(filename):
    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run()

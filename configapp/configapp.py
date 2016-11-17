from flask import Flask, render_template

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True
))


@app.route('/')
def index():
    return render_template('index.html')

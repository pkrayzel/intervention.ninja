from flask import Flask, render_template
import os

template_dir = os.path.abspath('../website/templates')
static_dir = os.path.abspath('../website/static')
app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)


@app.route('/index.html')
def home():
    return render_template('index.html')


@app.route('/sent.html')
def sent():
    return render_template('sent.html')


@app.route('/sent_general_error.html')
def sent_general_error():
    return render_template('sent_general_error.html')


@app.route('/sent_limit_exceeded.html')
def sent_limit_exceeded():
    return render_template('sent_limit_exceeded.html')

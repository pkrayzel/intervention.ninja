from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index.html')
def home():
    return render_template('index.html')


@app.route('/sent.html')
def sent():
    return render_template('sent.html')


@app.route('/emails/smell.html')
def email_smell():
    return render_template('emails/smell.html')


@app.route('/emails/drink.html')
def email_drink():
    return render_template('emails/drink.html')


@app.route('/emails/smell.txt')
def email_smell_text():
    return render_template('emails/smell.txt')


@app.route('/emails/drink.txt')
def email_drink_text():
    return render_template('emails/drink.txt')


from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask import jsonify
from logging import config
import logging

# constants
HOME_PAGE = 'index.html'
SENT = 'sent.html'
DRINK = 'drink'
SMELL = 'smell'

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)

config.fileConfig('logging.conf')


@app.route('/')
def home():
    return render_template(HOME_PAGE)


@app.route('/healthcheck')
def health_check():
    logging.info('Health check - available...')
    response = jsonify({
        "version": app.config["VERSION"],
        "status": 'AVAILABLE'
    })
    response.status_code = 200
    return response


@app.route('/send', methods=["POST"])
def send_email():
    email = request.form['email']
    template = request.form['template']

    msg = Message('Hello', sender='intervention.ninja@gmail.com', recipients=email.split(','))

    if template == DRINK:
        msg.body = "Hey, could you please stop drinking so much? Cheers!"
    elif template == SMELL:
        msg.body = "Hey, have you ever seen shower? Someone thinks that you smell like sh*t! Cheers!"

    logging.info('Sending email to recipient: {} with template: {}'.format(email, template))
    mail.send(msg)

    return render_template(SENT)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=app.config['THREADED'], debug=app.config['DEBUG'])

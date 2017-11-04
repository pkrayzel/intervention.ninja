from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask import jsonify
from logging import config
import logging

# constants
HOME_PAGE = 'index.html'
SENT = 'sent.html'
KEY_EMAIL = 'email'
KEY_TEMPLATE = 'template'
SUPPORTED_TEMPLATES = ['drink', 'smell']

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
    if KEY_EMAIL not in request.form \
            or KEY_TEMPLATE not in request.form:
        return construct_error_response(400, "Bad request. All required input parameters should be provided.")

    email = request.form[KEY_EMAIL]
    template = request.form[KEY_TEMPLATE]

    if template not in SUPPORTED_TEMPLATES:
        return construct_error_response(400, "Given template value is not supported.")

    msg = Message('Intervention Ninja - personal message',
                  sender='intervention.ninja@gmail.com',
                  recipients=email.split(','))
    msg.body = render_template('emails/{}.txt'.format(template))
    msg.html = render_template('emails/{}.html'.format(template))

    logging.info('Sending email to recipient: {} with template: {}'.format(email, template))
    mail.send(msg)

    return render_template(SENT)


def construct_error_response(message, status_code):
    response = jsonify({
        "code": status_code,
        "message": message
    })
    response.status_code = status_code
    return response


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=app.config['THREADED'], debug=app.config['DEBUG'])

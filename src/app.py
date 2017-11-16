from flask import Flask, render_template, request
from flask import jsonify
from logging import config
import logging
import os
from services import dao, common

# constants
HOME_PAGE = 'index.html'
SENT = 'sent.html'

app = Flask(__name__)
app.config.from_object('config')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

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
    try:
        logging.info("flask_app send handler: {}".format(request.form))

        body = request.form
        context = dict(source_ip=request.remote_addr)
        common.validate_send_email(body, context)
    except Exception as e:
        logging.error('Exception during sending email', e)
    return render_template(SENT)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=app.config['THREADED'], debug=app.config['DEBUG'])

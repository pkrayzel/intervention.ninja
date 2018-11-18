from flask import Flask, render_template, make_response, jsonify
from logging import config
import logging
import os

app = Flask(__name__)

config.fileConfig('logging.conf')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/_health')
def health_check():
    return make_response(
        jsonify({
            "version": os.environ.get('VERSION', 'N/A'),
            "status": 'AVAILABLE'
        }),
        200
    )


@app.route('/send', methods=["POST"])
def send_email():
    logging.info('Pretending to sent email...')
    return render_template('sent.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

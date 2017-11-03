# import the Flask class from the flask module
from flask import Flask, render_template, request

# create the application object
app = Flask(__name__)
HOME_PAGE = 'index.html'


# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template(HOME_PAGE)


@app.route('/send', methods=["POST"])
def send_email():
    email = request.form['email']
    return 'Send email: %s' % email


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
# import the Flask class from the flask module
from flask import Flask, render_template

# create the application object
app = Flask(__name__)
HOME_PAGE = 'index.html'


# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template(HOME_PAGE)


@app.route('/<email>', methods=["POST"])
def send(email):
    # TODO - send email
    print('Sending an email to: {}'.format(email))

    return render_template(HOME_PAGE)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

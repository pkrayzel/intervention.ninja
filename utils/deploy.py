from flask_frozen import Freezer
from generate_static import app
import time
import os

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()

    time.sleep(5)

    os.system('aws s3 cp build/ s3://www.intervention.ninja/ --recursive')
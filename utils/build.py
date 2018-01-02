from flask_frozen import Freezer
from generate_static import app
import time
import os
import boto3
import argparse
from datetime import datetime

freezer = Freezer(app)


if __name__ == '__main__':
    freezer.freeze()
    time.sleep(5)
    os.system('open build/index.html')

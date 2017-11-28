from src import intervention_ninja
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def test_simple():
    event = {"email": "pkrayzel@gmail.com", "template": "smell", "source-ip": "127.0.0.1"}
    context = None
    expected = ''

    real = intervention_ninja.lambda_handler(event, context)

    assert expected == real

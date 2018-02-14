import os
import sys
from src.services import dao_batch
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def test_store_values():
    result = dao_batch('pkrayzel@gmail.com', 'smell', '127.0.0.1')
    assert result is True


def test_get_counts():
    ip_item, email_item = dao_batch.get_items('pkrayzel@gmail.com', '127.0.0.1')
    assert ip_item is not None
    assert email_item is not None

    time.sleep(1)
    ip_item, email_item = dao_batch.get_items('pkrayzel@gmail.com', '127.0.0.1')
    assert ip_item is None
    assert email_item is None

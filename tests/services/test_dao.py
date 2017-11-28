import os
import sys
from src.services import dao
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def test_store_email():
    result = dao.store_email('pkrayzel@gmail.com', 'smell')
    assert result is True


def test_store_ip_address():
    result = dao.store_ip_address('127.0.0.1')
    assert result is True


def test_get_count_for_email():
    time_period = 10 * 60 * 1000
    count = dao.get_count_for_email('pkrayzel@gmail.com', time_period)
    assert count > 0

    time.sleep(1)
    time_period = 1000
    count = dao.get_count_for_email('pkrayzel@gmail.com', time_period)
    assert count == 0


def test_get_count_for_ip_address():
    time_period = 10 * 60 * 1000
    count = dao.get_count_for_ip_address('127.0.0.1', time_period)
    assert count > 0

    time.sleep(1)
    time_period = 1000
    count = dao.get_count_for_ip_address('127.0.0.1', time_period)
    assert count == 0
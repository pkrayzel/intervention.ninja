import os
import sys
import pytest
from src.services.mail import MailService
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

@pytest.fixture()
def mail_service():
    return MailService()


def test_send_email(mail_service):
    result = mail_service.send_mail(subject='subject',
                                    sender='intervention.ninja@gmail.com',
                                    recipient='pkrayzel@gmail.com',
                                    body_html='<html><body>Hello</body></html>')
    assert result is True

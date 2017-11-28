import os
import sys
import pytest
from src.services.template import TemplateService, TemplateServiceS3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

TITLE_FROM_BASE = 'Intervention Ninja - See it, Say it, Sorted!'
JINJA_TEMPLATE_UNESCAPED = '{% extends "common/base.html" %}'
FACEBOOK = 'Facebook'
TWITTER = 'Twitter'
LINKEDIN = 'Linkedin'
SOCIAL_NETWORK_TEMPLATE = '<span class="network-name">{}</span>'

HOME_PAGE = 'index.html'
SENT = 'sent.html'
EMAIL_DRINK = 'emails/drink.html'
EMAIL_SMELL = 'emails/smell.html'

TEMPLATES_TO_CHECK = [
    HOME_PAGE,
    SENT,
    EMAIL_DRINK,
    EMAIL_SMELL
]


@pytest.fixture
def template_service_local():
    return TemplateService('{}/src/templates/'.format(os.getcwd()))


@pytest.fixture
def template_service_s3():
    return TemplateServiceS3('www.intervention.ninja', '')


def test_render_template_locally(template_service_local):
    for template_name in TEMPLATES_TO_CHECK:
        template_test_helper(template_service_local, template_name)


def test_render_template_s3(template_service_s3):
    for template_name in TEMPLATES_TO_CHECK:
        template_test_helper(template_service_s3, template_name)


def template_test_helper(template_service, template_name):
    result = template_service.render_template(template_name)
    check_template(template_name, result)


def check_template(template_name, result):
    if template_name == HOME_PAGE:
        check_home_page(result)
    elif template_name == SENT:
        check_sent(result)
    elif template_name == EMAIL_DRINK:
        check_email_drink(result)
    elif template_name == EMAIL_SMELL:
        check_email_smell(result)


def check_home_page(result):
    assert result is not None
    assert result.find('Does your friend drink too much?') > -1
    assert result.find('Do you have a colleague, who smells like sh*t?') > -1
    assert result.find('<form action="') > -1
    assert result.find(TITLE_FROM_BASE) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(FACEBOOK)) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(FACEBOOK)) !=\
        result.rfind(SOCIAL_NETWORK_TEMPLATE.format(FACEBOOK))
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(TWITTER)) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(TWITTER)) !=\
        result.rfind(SOCIAL_NETWORK_TEMPLATE.format(TWITTER))
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(LINKEDIN)) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(LINKEDIN)) !=\
        result.rfind(SOCIAL_NETWORK_TEMPLATE.format(LINKEDIN))
    assert result.find(JINJA_TEMPLATE_UNESCAPED) == -1


def check_sent(result):
    assert result is not None
    assert result.find('Let\'s send another') > -1
    assert result.find('Done!') > -1
    assert result.find(TITLE_FROM_BASE) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(FACEBOOK)) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(TWITTER)) > -1
    assert result.find(SOCIAL_NETWORK_TEMPLATE.format(LINKEDIN)) > -1
    assert result.find(JINJA_TEMPLATE_UNESCAPED) == -1


def check_email_drink(result):
    assert result is not None
    assert result.find('users thinks, <strong>that you drink too much!</strong>') > -1


def check_email_smell(result):
    assert result is not None
    assert result.find('users thinks, <strong>that you might have a problem with hygiene...</strong>') > -1

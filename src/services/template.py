import logging
from jinja2 import Environment, FileSystemLoader
from jinja2_s3loader import S3loader

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class TemplateService:
    def __init__(self, template_path):
        logger.info('template path: {}'.format(template_path))
        self.template_loader = Environment(
            loader=FileSystemLoader(template_path)
        )

    def render_template(self, template_name, **context):
        logger.info('Rendering template: {}'.format(template_name))
        return self.template_loader.get_template(template_name).render(context)


class TemplateServiceS3(TemplateService):
    def __init__(self, bucket_name, template_path):
        logger.info('template path: {}'.format(template_path))
        self.template_loader = Environment(
            loader=S3loader(bucket_name, template_path)
        )
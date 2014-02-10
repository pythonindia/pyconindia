"""Mail sending for publicity

This program can be invoked like this::

$ publicitymail

"""
import os
import sys
import argparse
import ConfigParser

from envelopes import Envelope, GMailSMTP
from jinja2 import Template

from .log import get_logger, set_file_handler

logger = get_logger()

if os.environ.get('PUBLICITY_DO_NOT_SEND'):
    publicity_do_not_send = True
else:
    publicity_do_not_send = False


def send_mail(username, password, from_email, from_name,
                to_addresses, subject, body_template, config_path):
    gmail = GMailSMTP(username, password)
    for to_email, to_name in to_addresses:
        properties = parse_config(config_path, to_email)
        body = body_template.render(**properties)
        envelope = Envelope(
            from_addr=(from_email, from_name),
            to_addr=(to_email, to_name),
            subject=subject,
            text_body=body
        )

        logger.info(str(envelope))
        if not publicity_do_not_send:
            gmail.send(envelope)


def parse_config(config_path, section='main'):

    cp = ConfigParser.SafeConfigParser()
    cp.read(config_path)
    config = dict(cp.items(section))
    for key, value in config.items():
        env_key = "PUBLICITY_" + section.upper() + "_" + key.upper()
        config[key] = os.environ.get(env_key, value)
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Configguration file")
    parser.add_argument("-s", "--subject", help="Mail subject")
    parser.add_argument("-t", "--template", help="Mail body template")
    args = parser.parse_args()

    if not args.config:
        parser.print_help()
        sys.exit(1)
    if not args.subject:
        parser.print_help()
        sys.exit(1)
    if not args.template:
        parser.print_help()
        sys.exit(1)

    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        logger.error("Configuration doesn't exist: %s" % config_path)
        sys.exit(1)
    template_path = os.path.abspath(args.template)
    if not os.path.exists(template_path):
        logger.error("Template doesn't exist: %s" % template_path)
        sys.exit(1)
    subject = args.subject
    assert len(subject) >= 7, 'Very small subject'
    main_config = parse_config(config_path, 'main')
    username = main_config['username']
    password = main_config['password']
    from_email = main_config['from_email']
    from_name = main_config['from_name']
    to_addresses = parse_config(config_path, 'to_addresses').items()
    body_template = Template(open(template_path).read())
    send_mail(username, password, from_email, from_name,
                to_addresses, subject, body_template, config_path)

# -*- coding: utf-8 -*-
# Version: 1.0.0

__author__ = 'John Lampe'
__email__ = 'dmitry.chan@gmail.com'


import yaml
import logging
import os
import argparse
import pdb
from logging.handlers import TimedRotatingFileHandler
import sslmate


def main(myclient):
    """
    Main entry point into code
    :param myclient: sslmate client object
    :return: None
    """
    
    if myclient:
        print("Connected up. Onward and upward")
    else:
        print("You messed something up...you always do...try better")

    foo = myclient.get_cert('www.infosecog.com')
    print(foo)


def configure_logging(log_path, date_format, log_format,
                      log_file_name, retention, log_level='INFO'):
    """
    Configures logging based on the pathing, log level, and formatting provided
    :param retention: Number of days to retain the log
    :param log_file_name: Name of the log file
    :param log_path: Path where the log file will be written
    :param date_format: Format the date will appear as in the log file
    :param log_format: Format the entire log message will appear as in the log
    file
    :param log_level: INFO by default, DEBUG if -v argument is given during
    execution
    :return:
    """

    log_file = os.path.join(log_path, log_file_name)

    if not os.path.isdir(log_path):
        os.mkdir("{}".format(log_path))

    rotate_handler = TimedRotatingFileHandler(filename=log_file,
                                              when='midnight',
                                              interval=1,
                                              backupCount=retention)
    # Will be appended to the rotated log: 20190525
    rotate_suffix = "%Y%m%d"
    rotate_handler.suffix = rotate_suffix

    # Attach formatter
    rotate_handler.setFormatter(logging.Formatter(fmt=log_format,
                                                  datefmt=date_format))

    # noinspection PyArgumentList
    logging.basicConfig(handlers=[rotate_handler],
                        level=log_level)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='sslmate API check')
    parser.add_argument('-c', action='store', dest='config_path', help='config file', required=True)
    parser.add_argument('-v', action='store_true', dest='verbosity', help='set script verbosity')
    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        raise RuntimeError('Configuration file provided does not exist')

    with open(args.config_path) as c:
        config = yaml.safe_load(c)

    logging_conf = config['logging']
    if args.verbosity:
        level = "DEBUG"
    else:
        level = "INFO"

    configure_logging(log_path=logging_conf['path'],
                      date_format=logging_conf['date_format'],
                      log_format=logging_conf['log_format'],
                      log_file_name='find_new_domains.log',
                      log_level=level,
                      retention=logging_conf['retention'])


    logging.info('Executing Script: {0}'.format(__file__))

    try:
        token = config['sslmate']['api_key']
    except:
        logging.error("No key defined in yaml. Exiting")
        exit(0)

    try:
        endpoint = config['sslmate']['api_endpoint']
    except:
        logging.error("No endpoint defined. Exiting")
        exit(0)

    try:
        approval_proxy = config['sslmate']['api_approval_proxy']
    except:
        logging.error("No approval proxy. Continuing on without one")
        approval_proxy = ''

    myclient = sslmate.sslMateClient(endpoint, token, approval_proxy)

    main(myclient)

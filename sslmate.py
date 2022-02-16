# -*- coding: utf-8 -*-
# Version: 1.0.0
# Class file for sslmate API

__author__ = 'John Lampe'
__email__ = 'dmitry.chan@gmail.com'

import requests
import json
import re
import pdb
import logging


class sslMateClient:
    def __init__(self, base_url, key, approval_proxy='', verify=True):
        """
        Main entry-point into class
        :param token: A valid Calendly API Token
        :param verify: defaults to True for verify TLS/SSL certs
        """
        self.base_url = base_url
        self.token = key
        self.approval_proxy = approval_proxy
        self.session = requests.Session()
        self.session.verify = verify
        if not self.token:
            logging.error("No key was presented. Exiting")
            exit(0)

        self.session.headers = {"Content-Type": "application/json", "Accept": "application/json",
                                "Authorization": "Bearer {}".format(self.token)}



    def get_cert(self, domain):
        """
        retrieve Cert info from sslmate
        :param domain: string, the domain to be queried
        :return: dict
        """
        ret = {}
        try:
            request_url = "{}?domain={}&expand=dns_names&expand=issuer&expand=cert".format(self.base_url, domain)
            http_response = self.session.get(request_url)
            logging.info("Issuing GET {}".format(request_url))

            if http_response and http_response.json():
                return http_response.json()
            else:
                logging.error("Failed to retrieve {}".format(request_url))
                return ret
        except Exception as e:
            logging.error("Failed to retrieve domain cert info for {}. Error: {}".format(domain, e))
            return ret

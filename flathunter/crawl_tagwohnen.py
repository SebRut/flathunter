"""Expose crawler for TAG wohnen"""
import logging
import re
import datetime
from flathunter.abstract_crawler import Crawler
import json
import requests

class CrawlTagWohnen(Crawler):
    """Implementation of Crawler interface for TAG wohnen (https://tag-wohnen.de)."""

    __log__ = logging.getLogger("flathunt")
    URL_PATTERN = re.compile(r'https://tag-wohnen\.de')

    HEADERS = {
            'Authorization': 'Basic cnNtOnJzbTIwMTk='
        }

    def __init__(self, config):
        logging.getLogger('requests').setLevel(logging.WARNING)
        self.config = config

    def get_page(self, url):
        self.rotate_user_agent()
        filter = url.replace("https://tag-wohnen.de/immosuche", '')
        response = requests.get('https://immo.isp-10130-1.domservice.de/properties' + filter)
        print(response)
        if response.status_code != 200:
            self.__log__.debug("Fetching exposes failed")
        return response.text

    def extract_data(self, text):
        entries = list()

        parsed_json = json.loads(text)
        
        try:
            results = parsed_json['response']['results']
        except ArithmeticError:
            self.__log__.debug("response contained no results")
            return entries
        for result in results:
            raw_id = result['id']
            entry = {
                'id' : int(raw_id.replace('/','')),
                'url' : 'https://tag-wohnen.de/immosuche/expose?object_id=' + raw_id,
                'image': result['image_url'],
                'title': result['title'],
                'address': result['address'],
                'crawler': self.get_name(),
                'price': str(result['overall_warm']),
                'size': str(result['living_space']),
                'rooms': str(result['number_of_rooms']) 
            }

            print(entry)

            entries.append(entry)

        return entries

        
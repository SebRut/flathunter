import unittest
import pytest
from flathunter.crawl_tagwohnen import CrawlTagWohnen
from flathunter.config import Config


TEST_URL = 'https://tag-wohnen.de/immosuche?filters%5Bfittings%5D[]=Balkon&filters%5Bproperty_city%5D[]=Neubrandenburg&living_space%5Bmin%5D=23&price%5Bmin%5D=123&rooms%5Bmin%5D=2&size=10&view=LIST'
DUMMY_CONFIG = """
capcha:
  driver_path: /usr/bin/chromedriver
  driver_arguments:
    - "--headless"
urls:
    - https://tag-wohnen.de/immosuche?filters%5Bfittings%5D[]=Balkon&filters%5Bproperty_city%5D[]=Neubrandenburg&living_space%5Bmin%5D=23&price%5Bmin%5D=123&rooms%5Bmin%5D=2&size=10&view=LIST
"""

@pytest.fixture
def crawler():
    return CrawlTagWohnen(Config(string=DUMMY_CONFIG))

def test_crawler(crawler):
    soup = crawler.get_page(TEST_URL)
    assert soup is not None
    entries = crawler.extract_data(soup)
    assert entries is not None
    assert len(entries) > 0
    assert entries[0]['id'] > 0
    assert entries[0]['url'].startswith("https://tag-wohnen.de/immosuche/expose?")
    for attr in [ 'title', 'price', 'size', 'rooms', 'address' ]:
        assert entries[0][attr] is not None

def test_process_expose_fetches_details(crawler):
    text = crawler.get_page(TEST_URL)
    assert text is not None
    entries = crawler.extract_data(text)
    assert entries is not None
    assert len(entries) > 0
    updated_entries = [ crawler.get_expose_details(expose) for expose in entries ]
    for expose in updated_entries:
        print(expose)
        for attr in [ 'title', 'price', 'size', 'rooms', 'address' ]:
            assert expose[attr] is not None
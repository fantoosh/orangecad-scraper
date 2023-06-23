import json
import pkgutil

import scrapy
import pandas as pd
from urllib.parse import urlencode


df = pd.read_csv('map_id.csv')
map_ids = df.map_id.to_list()
base_url = "https://gis.bisclient.com/maps03/rest/services/OrangePropertySearch/MapServer/0/query"


querystrings = []
for map_id in map_ids:
    querystring = {"f": "json",
                   "where": f"map_id = '{str(map_id)}'",
                   "returnGeometry": "False",
                   "spatialRel": "esriSpatialRelIntersects",
                   "outFields": "*",
                   "outSR": "102100"}
    querystrings.append(querystring)

queries = []
for querystring in querystrings:
    query_params = urlencode(querystring)
    url = f"{base_url}?{query_params}"
    queries.append(url)


class OrangecadApiScraperSpider(scrapy.Spider):
    name = "orangecad"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://esearch.orangecad.net",
        "Referer": "https://esearch.orangecad.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
    }

    def start_requests(self):
        yield scrapy.Request('https://esearch.orangecad.net', headers=self.headers)

    def parse(self, response, **kwargs):
        urls = queries[:64]
        print(querystring)
        yield from response.follow_all(urls, callback=self.parse_raw_json, headers=self.headers)

    def parse_raw_json(self, response, **kwargs):
        raw_json = response.json()
        features = raw_json.get('features')
        attributes = features[0].get('attributes') if features else {}
        attributes.update({'url': response.url})
        yield attributes


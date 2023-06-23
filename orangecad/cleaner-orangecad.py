import pkgutil

import requests
import csv
import pandas as pd
from urllib.parse import urlencode


df = pd.read_csv('../map_id.csv')
map_ids = df.map_id.to_list()
base_url = "https://gis.bisclient.com/maps03/rest/services/OrangePropertySearch/MapServer/0/query"

data = pkgutil.get_data("orangecad", "resources/urls.txt")
print(data)
if data:
    content = data.decode('utf-8')
    urls = content.splitlines()

    print(urls)

querystrings = []
for map_id in map_ids:
    querystring = {"f": "json",
                   "where": f"map_id = '{map_id}'",
                   "returnGeometry": "False",
                   "spatialRel": "esriSpatialRelIntersects",
                   "outFields": "*",
                   "outSR": "102100"}
    querystrings.append(querystring)


headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    # "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://esearch.orangecad.net",
    # "Pragma": "no-cache",
    "Referer": "https://esearch.orangecad.net/",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
}

data = []
for querystring in querystrings:
    query_params = urlencode(querystring)
    url = f"{base_url}?{query_params}"
    data.append(url)

# with open('urls.csv', 'w', newline='') as f:
#     csvwriter = csv.writer(f)
#     f.writelines(data)

# df = pd.DataFrame({'urls': data})
# print(df)
# df.to_csv('urls.txt', index=False)

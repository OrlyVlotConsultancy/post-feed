#!/usr/bin/env python
import json, requests, pathlib

API = "https://orlyvlot.nl/wp-json/wp/v2/posts"
PER_PAGE = 100

def all_wp_urls():
    page, urls = 1, []
    while True:
        r = requests.get(API, params={"per_page": PER_PAGE, "page": page}, timeout=30)
        if r.status_code == 400 or not r.json():
            break
        urls += [p["link"] for p in r.json()]
        page += 1
    return urls

# schrijf het bestand in de root ( NIET in een map )
json.dump({"urls": all_wp_urls()}, open("posts.json", "w"), indent=2)

#!/usr/bin/env python
import json, requests

API = "https://orlyvlot.nl/wp-json/wp/v2/posts"
PER_PAGE = 100

def all_posts(api=API):
    page, urls = 1, []
    while True:
        r = requests.get(api, params={"per_page": PER_PAGE, "page": page}, timeout=30)
        if r.status_code == 400 or not r.json():
            break
        urls.extend(p["link"] for p in r.json())
        page += 1
    return urls

json.dump({"urls": all_posts()}, open("posts.json", "w"), indent=2)

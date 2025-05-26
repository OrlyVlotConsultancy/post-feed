#!/usr/bin/env python
import json, requests, xml.etree.ElementTree as ET

INDEX = "https://orlyvlot.nl/post-sitemap.xml"
HEAD  = {"User-Agent": "Mozilla/5.0 (compatible; PostFeedBot/1.0)"}

def locs(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    return [loc.text.strip() for loc in root.iter("{*}loc")]

def fetch(url: str) -> str:
    return requests.get(url, headers=HEAD, timeout=30).text

def all_posts(index_url=INDEX) -> list[str]:
    posts = []
    for sm_url in locs(fetch(index_url)):          # eerste laag (sub-sitemaps)
        if not sm_url.endswith(".xml"):
            continue                               # veiligheidscheck
        for url in locs(fetch(sm_url)):            # tweede laag (post-URL’s)
            if not url.endswith(".xml"):
                posts.append(url)
    return posts

json.dump({"urls": all_posts()}, open("posts.json", "w"), indent=2)

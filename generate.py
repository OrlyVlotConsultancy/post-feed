#!/usr/bin/env python
import json, requests, xml.etree.ElementTree as ET

INDEX = "https://orlyvlot.nl/post-sitemap.xml"

def urls_from_sitemap(xml_text):
    root = ET.fromstring(xml_text)
    return [loc.text.strip() for loc in root.iter("{*}loc")]

def all_post_urls(index_url=INDEX) -> list[str]:
    urls = []
    xml = requests.get(index_url, timeout=20).text
    for loc in urls_from_sitemap(xml):
        if loc.endswith(".xml"):                      # sub-sitemap
            sub_xml = requests.get(loc, timeout=20).text
            urls.extend(urls_from_sitemap(sub_xml))   # echte post-URL’s
        else:
            urls.append(loc)                          # (komt zelden voor)
    return urls

posts = {"urls": all_post_urls()}

with open("posts.json", "w") as f:
    json.dump(posts, f, indent=2)

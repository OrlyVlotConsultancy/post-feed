#!/usr/bin/env python
import json, requests, xml.etree.ElementTree as ET

START = "https://orlyvlot.nl/post-sitemap.xml"

def collect(url):
    """Geeft alle <loc>-links binnen één sitemap-bestand."""
    xml = requests.get(url, timeout=20).text
    root = ET.fromstring(xml)
    return [loc.text.strip() for loc in root.iter("{*}loc")]

def all_posts(index_url=START):
    """Doorloopt sitemap-index → subsitemap(s) → echte post-URL’s."""
    posts = []
    for link in collect(index_url):
        if link.endswith(".xml"):          # nog een subsitemap
            # loop door de tweede laag – verwacht hier <urlset> met posts
            posts.extend([u for u in collect(link) if not u.endswith(".xml")])
        else:                              # directe post-URL (komt zelden voor)
            posts.append(link)
    return posts

json.dump({"urls": all_posts()}, open("posts.json", "w"), indent=2)

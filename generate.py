#!/usr/bin/env python
import json, requests, xml.etree.ElementTree as ET

SITE = "https://orlyvlot.nl/post-sitemap.xml"
xml = requests.get(SITE, timeout=20).text
root = ET.fromstring(xml)
urls = [loc.text.strip() for loc in root.iter("{*}loc")]

with open("posts.json", "w") as f:
    json.dump({"urls": urls}, f, indent=2)

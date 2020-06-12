#import lxml.etree as ET
import xml.etree.ElementTree as ET
import urllib.request, urllib.parse, urllib.error
import sys

if __name__ == "__main__":
    for i in sys.argv[1:]:
        t = ET.parse(i).getroot()
        label = '"<li>'
        url = t.attrib.get('url')
        if url:
            label += "<a href='" + urllib.parse.quote_plus(urllib.parse.unquote(url),":/") + "'>"
        label += t.attrib.get('title')
        if url:
            label += "</a>"

        original_title = t.attrib.get('original_title')
        if original_title:
            label += " (" + original_title + ")"
        label += '</li>",'
        print(label.encode('utf-8'))

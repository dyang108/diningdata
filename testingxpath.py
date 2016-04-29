import os
import urllib
import ast
import re
from lxml import html
from pymongo import MongoClient

if __name__ == "__main__":
    notParsable = []
    inserted = []
    numarr = []
    with open(os.path.expanduser("validrecipes.txt")) as f:
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                numarr.append(line[0])

    for i in numarr:
        index = str(i).zfill(6)
        page = urllib.urlopen("http://menus.tufts.edu/foodpro/label.asp?locationNum=09&RecNumAndPort="+index)
        htmlSource = page.read()
        page.close()
        tree = html.fromstring(htmlSource)
        element = tree.xpath("/html/body")
        print element
        print element.text_content()
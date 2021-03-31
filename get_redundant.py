import os
import urllib
import json

bset = set()
lset = set()
dset = set()
halls = ["dewick", "carm"]
for i in range(1, 28):
    for j in range(1, 2):
        page = urllib.request.urlopen("https://tuftsdiningdata.herokuapp.com/menus/" + halls[0] + "/" + str(i) + "/" + str(j) + "/2018")
        htmlSource = page.read()
        page.close()
        menu_obj = json.loads(htmlSource)
        if "data" in menu_obj:
            print menu_obj["menu-id"]
            print bset
            print lset
            print dset
            if "Breakfast" in menu_obj["data"]:
                b = []
                for k, v in menu_obj["data"]["Breakfast"].iteritems():
                    b = b + v
                if len(b) > 0:
                    if len(bset) == 0:
                        print 0
                        bset = set(b)
                    else:
                        bset = bset.intersection(set(b))
            if "Lunch" in menu_obj["data"]:
                l = []
                for k, v in menu_obj["data"]["Lunch"].iteritems():
                    l = l + v
                if len(l) > 0:
                    if len(lset) == 0:
                        print 0
                        lset = set(l)
                    else:
                        lset = lset.intersection(set(l))
            if "Dinner" in menu_obj["data"]:
                d = []
                for k, v in menu_obj["data"]["Dinner"].iteritems():
                    d = d + v
                if len(d) > 0:
                    if len(dset) == 0:
                        print 0
                        dset = set(d)
                    else:
                        dset = dset.intersection(set(d))

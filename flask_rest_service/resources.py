import json
import urllib
import xml.etree.ElementTree as ET
from lxml import html
from flask import request, abort
from flask.ext import restful
from flask.ext.restful import reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId

class ReadingList(restful.Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('reading', type=str)
        super(ReadingList, self).__init__()

    def get(self):
        return  [x for x in mongo.db.readings.find()]

    def post(self):
        args = self.parser.parse_args()
        if not args['reading']:
            abort(400)

        jo = json.loads(args['reading'])
        reading_id =  mongo.db.readings.insert(jo)
        return mongo.db.readings.find_one({"_id": reading_id})


class Reading(restful.Resource):
    def get(self, reading_id):
        return mongo.db.readings.find_one_or_404({"_id": reading_id})

    def delete(self, reading_id):
        mongo.db.readings.find_one_or_404({"_id": reading_id})
        mongo.db.readings.remove({"_id": reading_id})
        return '', 204


class Root(restful.Resource):
    def get(self):
        page = urllib.urlopen("http://menus.tufts.edu/foodpro/shortmenu.asp?sName=Tufts+Dining&locationNum=09&locationName=Carmichael+Dining+Center&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=3%2F28%2F2016")
        #http://menus.tufts.edu/foodpro/shortmenu.asp?sName=Tufts+Dining&locationNum=09&locationName=Carmichael+Dining+Center&naFlag=1
        htmlSource = page.read()
        tree = html.fromstring(htmlSource)
        jsondata = {}
        for meal in tree.findall(".//*[@class='shortmenumeals']"):
            curr_meal = meal.text
            jsondata[curr_meal] = {}
            mealparent = meal.find("../../../../../../..")
            for foodtype in mealparent.findall(".//*[@class='shortmenucats']/span"):
                curr_foodtype = foodtype.text[3:-3]
                jsondata[curr_meal][curr_foodtype] = []
                for food in foodtype.xpath("../../../following-sibling::tr"):
                    if food.find(".//*[@name='Recipe_Desc']") is None:
                        break
                    jsondata[curr_meal][curr_foodtype].append(food.find(".//*[@name='Recipe_Desc']").text)
        return jsondata

api.add_resource(Root, '/')
api.add_resource(ReadingList, '/readings/')
api.add_resource(Reading, '/readings/<ObjectId:reading_id>')

import json
import urllib
from lxml import html
from flask import request, abort
from flask.ext import restful
from flask.ext.restful import reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId

dining_halls = {
    "dewick": "11&locationName=Dewick-MacPhie+Dining+Center",
    "carm": "09&locationName=Carmichael+Dining+Center",
    "commons": "55&locationName=The+Commons+Marketplace",
    "paxetlox": "27&locationName=Pax+et+Lox+Glatt+Kosher+Deli",
    "brownandbrew": "04&locationName=Brown+%26+Brew+Coffee+House",
    "hodgdon": "14&locationName=Hodgdon+Food+On-the-Run++",
    "mugar": "15&locationName=Mugar+Cafe",
    "tower": "07&locationName=Tower+Cafe"
}

ERROR = { "error": "Resource not found. Invalid dining hall." }

class Menu(restful.Resource):
    def get(self, hall, day, month, year):
        hallarg = dining_halls.get(hall.lower())
        if hallarg is None:
            return ERROR
        menuid = hall + "-" + day + "-" + month + "-" + year
        indb = mongo.db.meals.find_one({"menu-id": menuid})
        if indb is not None:
            if indb["data"].get("Breakfast") or indb["data"].get("Lunch") or indb["data"].get("Dinner"):
                return indb

        page = urllib.urlopen("http://menus.tufts.edu/foodpro/shortmenu.asp?sName=Tufts+Dining&locationNum=" + hallarg + "&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + month + "%2F" + day + "%2F" + year)
        htmlSource = page.read()
        page.close()
        tree = html.fromstring(htmlSource)
        daymenus = self.getdata(tree)

        dbobj = { "data": daymenus, "menu-id": menuid, "credit": "https://github.com/dyang108/diningdata" }
        mongo.db.meals.update({ "menu-id": menuid }, dbobj, True)
        return dbobj

    def getdata(self, tree):
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

class Ingredients(restful.Resource):
    def get(self, food):
        food = food.replace('+', ' ').lower()
        indb = mongo.db.ingdata.find_one({"name": food})
        if indb is not None:
            return indb
        else:
            return {"error": "Food not found."}

api.add_resource(Menu, '/menus/<hall>/<day>/<month>/<year>')
api.add_resource(Ingredients, '/ingredients/<food>')
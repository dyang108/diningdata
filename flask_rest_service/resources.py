import json
import urllib
import cgi
from lxml import html
from flask import request, abort
from flask_rest_service import Resource, app, api, mongo
from bson.objectid import ObjectId
from flask_rest_service.consts import *

class Menu(Resource):
    def get(self, hall, day, month, year):
        hallarg = dining_halls.get(hall.lower())
        if hallarg is None:
            return ERROR
        menuid = hall + "-" + day + "-" + month + "-" + year
        indb = mongo.db.meals.find_one({"menu-id": menuid})
        if indb is not None:
            if indb["data"].get("Breakfast") or indb["data"].get("Lunch") or indb["data"].get("Dinner"):
                return indb
        url = "http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=Tufts+Dining&locationNum=" + hallarg + "&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + month + "%2F" + day + "%2F" + year
        print(url)
        page = urllib.request.urlopen(url)
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
                    newname = food.find(".//*[@name='Recipe_Desc']").text
                    if newname:
                        jsondata[curr_meal][curr_foodtype].append(cgi.escape(newname))
        return jsondata

# these two classes are really very similar, ideally we would inherit from Menu class.
class RelevantMenu(Resource):
    def get(self, hall, day, month, year):
        hallname = hall.lower()
        if hallname == "dewick" or hallname == "carm":
            return ERROR
        hallarg = dining_halls.get(hallname)
        menuid = hallname + "-" + day + "-" + month + "-" + year + "r"
        indb = mongo.db.meals.find_one({"menu-id": menuid})
        if indb is not None:
            if indb["data"].get("Breakfast") or indb["data"].get("Lunch") or indb["data"].get("Dinner"):
                return indb

        page = urllib.request.urlopen("http://menus.tufts.edu/foodpro/shortmenu.asp?sName=Tufts+Dining&locationNum=" + hallarg + "&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + month + "%2F" + day + "%2F" + year)
        htmlSource = page.read()
        page.close()
        tree = html.fromstring(htmlSource)
        daymenus = self.getdata(tree, hall)

        dbobj = { "data": daymenus, "menu-id": menuid, "credit": "https://github.com/dyang108/diningdata" }
        mongo.db.meals.update({ "menu-id": menuid }, dbobj, True)
        return dbobj

    def getdata(self, tree, hallname):
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
                    newname = food.find(".//*[@name='Recipe_Desc']").text
                    if newname:
                        if newname not in regulars[hallname][curr_meal]:
                            jsondata[curr_meal][curr_foodtype].append(cgi.escape(newname))
        return jsondata

class Ingredients(Resource):
    def get(self, food):
        food = food.replace('+', ' ').lower()
        indb = mongo.db.ingredients.find_one({"name": food})
        if indb is not None:
            return indb
        else:
            return {"error": "Food not found."}

api.add_resource(Menu, '/menus/<hall>/<day>/<month>/<year>')
api.add_resource(RelevantMenu, '/rmenus/<hall>/<day>/<month>/<year>')
api.add_resource(Ingredients, '/ingredients/<food>')
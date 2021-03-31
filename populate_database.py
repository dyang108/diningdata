import os
from urllib import request
import ast
from lxml import html
from pymongo import MongoClient

connection = MongoClient("mongodb+srv://derickwyang:IAtC7S9wR24kvq*XKOw@diningdata.hsrhe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = connection.rest

def notValidFood(tree):
    return tree.find_class('labelnotavailable')

def getIngredients(tree):
    ingElement = tree.find_class('labelingredientsvalue')
    try:
        ingString = ingElement[0].text_content()
    except:
        return "Ingredients not parsable"
    ingString = "[{\"name\": \"" + ingString + "\"}]"
    ingString = ingString.replace(")", "\"}]!")
    ingString = ingString.replace(", ", "\"}, {\"name\": \"")
    ingString = ingString.replace("(", "\", \"subingredients\": [{\"name\": \"")
    ingString = ingString.replace("!\"", "")
    try:
        return ast.literal_eval(ingString)
    except:
        return "Ingredients not parsable"

def getAllergens(tree):
    allergens = tree.find_class('labelallergensvalue')
    try:
        allergenString = allergens[0].text_content()
    except:
        return "Allergens not parseable"
    allergenList = allergenString.split(', ')
    return allergenList

def getCalories(html):
    try:
        string1 = "Calories&nbsp;"
        string2 = "</b>"
        start = html.index(string1) + len(string1)
        end = html.index(string2,start)
        return int(html[start:end])
    except:
        return -1



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
        try:
            index = str(i).zfill(6)
            # brute force all the files, using the base url for all of the foods
            url = "http://menus.tufts.edu/FoodPro%203.1.NET/label.aspx?locationNum=09&RecNumAndPort=" + index
            page = request.urlopen(url)
            htmlSource = page.read()
            page.close()
            tree = html.fromstring(htmlSource)

            if (notValidFood(tree)):
                page = request.urlopen("http://menus.tufts.edu/FoodPro%203.1.NET/label.aspx?locationNum=11&RecNumAndPort=" + index)
                htmlSource = page.read()
                page.close()
                tree = html.fromstring(htmlSource)
                if (notValidFood(tree)):
                    print('not valid: ' + index)
                    continue

            foodname = tree.find_class('labelrecipe')[0].text_content().strip(' ').lower()

            if db.ingredients.find_one({"name": foodname}) is not None:
                print('already in db: ' + index)
                continue

            toAddIng = { "ingredients": getIngredients(tree), "name": foodname, "allergens": getAllergens(tree), "calories": getCalories(htmlSource)}

            if toAddIng["ingredients"] == "Ingredients not parsable":
                print('ingredients not parsable: ' + index)
                notParsable.append(i)

            print('inserting: ' + index)
            db.ingredients.insert_one(toAddIng)
            inserted.append(i)
        except IOError:
            print('error: ' + str(i))
            continue

    db.urldata.insert_one({"notParsable": notParsable, "inserted": inserted})
    # toAddNutrition = { "nutrition": getNutrition(tree), "name": foodname}
    # ingdata collection has allergen information, ingredients does not
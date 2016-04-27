import os
import urllib
import ast
import re
from lxml import html
from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017/")

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

def getCalories(tree):
    calorie_elem = tree.xpath(/html/body/table[1]/tbody/tr/td/table/tbody/tr[1]/td[1]/font[4]/b)
    try:
       calorie_str = calorie_elem.text_content()
    except:
        return "Calories not parsable"
    return int(re.search(r'\d+', string1).group())




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
            page = urllib.urlopen("http://menus.tufts.edu/foodpro/label.asp?locationNum=09&RecNumAndPort=" + index)
            htmlSource = page.read()
            page.close()
            tree = html.fromstring(htmlSource)

            if (notValidFood(tree)):
                page = urllib.urlopen("http://menus.tufts.edu/foodpro/label.asp?locationNum=11&RecNumAndPort=" + index)
                htmlSource = page.read()
                page.close()
                tree = html.fromstring(htmlSource)
                if (notValidFood(tree)):
                    print 'not valid: ' + index
                    continue

            foodname = tree.find_class('labelrecipe')[0].text_content().strip(' ').lower()

            if db.ingdata.find_one({"name": foodname}) is not None:
                print 'already in db: ' + index
                continue

            toAddIng = { "ingredients": getIngredients(tree), "name": foodname, "allergens": getAllergens(tree), "calories": getCalories(tree)}

            if toAddIng["ingredients"] == "Ingredients not parsable":
                print 'ingredients not parsable: ' + index
                notParsable.append(i)

            print 'inserting: ' + index
            db.ingdata.insert(toAddIng)
            inserted.append(i)
        except IOError:
            print 'error: ' + str(i)
            continue

    db.urldata.insert({"notParsable": notParsable, "inserted": inserted})
    # toAddNutrition = { "nutrition": getNutrition(tree), "name": foodname}
    # ingdata collection has allergen information, ingredients does not
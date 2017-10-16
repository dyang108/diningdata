# Dining Data
A RESTful API that pulls dining data from Tufts dining websites, using Python page scraping, a Flask framework, and MongoDB. Hosted on Heroku with a database on mlab.com. This is a CORS-enabled API, using a simple GET request should work.

### Methods:
In order to use the API, call an HTTP GET request on the URL, like so:
```
GET https://tuftsdiningdata.herokuapp.com/menus/[hall]/[day]/[month]/[year]
```
where the date is not padded by zeros, and [hall] is one of the following strings: "dewick", "carm", "commons", "paxetlox", "brownandbrew", "hodgdon", "mugar", "tower"

Eg: `GET https://tuftsdiningdata.herokuapp.com/menus/carm/29/3/2016`

There's also an ingredients endpoint: `GET https://tuftsdiningdata.herokuapp.com/ingredients/[foodname]`

Eg: `GET https://tuftsdiningdata.herokuapp.com/ingredients/Belgian%20Waffles`

If you could please credit me somehow in your project README, I would be very grateful.

##### For me:
To push changes to the Heroku app:
```
git add .
git commit -m "something here"
git push heroku master
```

##### Implementation notes:
How it works: On the first request for a menu on a given day, the site loads and parses data from the actual Tufts Dining website. On subsequent calls to the same data, menu data is loaded directly from the database.
Credit to Serafeim Papastefanos for a great [tutorial](http://spapas.github.io/2014/06/30/rest-flask-mongodb-heroku/) on building a REST API.

##### Collaborating on the API:
The first time I went through Tufts Dining recipes, I cycled through the 1000000 numeric combinations of the foods URL. The Tufts Menus server is prone to issues, so I used a number of try-except blocks to skip over pages that were difficult for Python to read.

The `validrecipes.txt` file has a list of all the indices where the following URL is valid:

`http://menus.tufts.edu/foodpro/label.asp?locationNum=09&RecNumAndPort=XXXXXX`

Before running the server, you will have to run the following command to install dependencies: `pip install -r requirements.txt`. To run the server, the command is `python runserver.py`

Running `python populate_database.py` will loop through all valid recipe URL's and add them to your local Mongo DB. MAKE SURE you have mongo running in the background before starting this script.

My app routes are in resources.py. I suggest you follow the tutorial above or inspect my code to figure out what it's doing. Essentially, the `api.add_resource` queries the specified class with the URL arguments.

I encourage you to use `populate_database.py` as a template for your attempted parses of the Tufts Menus sites. Please [make a pull request](https://github.com/dyang108/diningdata/compare) to this repository if you have a *working* Python scraping script.

As for getting the actual data into the API, [this](http://docs.mlab.com/migrating/) link should help you out. I'm going to suggest that you push your working scrapers to the repo so that I can run them, and then I can migrate the data into the mLab database. Alternatively, you can send me the .bson file or message me to be added as a collaborator on TuftsDiningData.

Note to self: put in documentation for how to migrate local database to mLab, once I have done it again.

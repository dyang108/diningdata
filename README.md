# Dining Data
A RESTful API that pulls dining data from Tufts dining websites, using Python page scraping, a Flask framework, and MongoDB. Hosted on Heroku with a database on mlab.com. This is a CORS-enabled API, using a simple GET request should work.

### Methods:
In order to use the API, call an HTTP GET request on the URL, like so:
```
GET https://tuftsdiningdata.herokuapp.com/menus/[hall]/[day]/[month]/[year]
```
where the date is not padded by zeros, and [hall] is one of the following strings: "dewick", "carm", "commons", "paxetlox", "brownandbrew", "hodgdon", "mugar", "tower"

Eg: `GET https://tuftsdiningdata.herokuapp.com/menus/carm/29/3/2016`

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

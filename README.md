# Dining Data
A RESTful API that pulls dining data from Tufts dining websites, using Python page scraping, a Flask framework, and MongoDB. Hosted on Heroku with a database on mlab.com.

### Methods:
In order to use the API, call an HTTP GET request on the URL, like so:
```
GET https://tuftsdiningdata.herokuapp.com/[hall]/[day]/[month]/[year]
```
where [hall] is the string 'carm' or 'dewick', and the date is not padded by zeros: 
Eg: `GET https://tuftsdiningdata.herokuapp.com/carm/29/3/2016`

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
Credit to [Serafeim Papastefanos](http://spapas.github.io/2014/06/30/rest-flask-mongodb-heroku/) for a great tutorial on building a REST API.

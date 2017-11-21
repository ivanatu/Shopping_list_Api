[![Coverage Status](https://coveralls.io/repos/github/ivanatu/Shopping_list_Api/badge.png?branch=master)](https://coveralls.io/github/ivanatu/Shopping_list_Api?branch=master)


[![Maintainability](https://api.codeclimate.com/v1/badges/cc4de24321a651891f87/maintainability)](https://codeclimate.com/github/ivanatu/Shopping_list_Api/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/cc4de24321a651891f87/test_coverage)](https://codeclimate.com/github/ivanatu/Shopping_list_Api/test_coverage)


# Shopping_list_Api

In this repo we are basically creating API . We are trying to implement end points fir our applicaton to run . The Application will be interacting with the persistent data from the database and this will help us use end points for GET, POST, PUT, DELETE. All the functionalities run with POstman App on the google apps.

About

This is an API for a shopping list application that allows users to record and share things they want to spend money on and keep track of their shopping lists.

Goal

The goal of this project is to provide a uniform API for both web and mobile frontend shopping list applications.

Features

With this API;

You can create a user account - Registration
You can login and log out - Authorization and Authentication
You can create, view, update, and delete a shopping list in your user account
You can create, view, update, and delete an item in your shopping list under your account
API Documentation

Documentation for this API can be found at http://127.0.0.1:5001, when you run the application locally or you can navigate to the heroku deployment and view the documentation

Tools

Tools used during the development of this API are;

Swagger - this is a tool for documenting the API
JWT - JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object
Flask - this is a python micro-framework
Postgresql - this is a database server
Requirements

Python 2.7.1x+. preferably use Python 3.x.x+
Tests

   $ cd app
   $ nosetest --with-coverage test_app.py
Running the application

To run this application on a linux box, execute the following command.

    $ cd shopping_list_api
    $ virtualenv virtenv
    $ source virtenv/bin/activate
    $ pip install -r requirements.txt
    $ python run.py db init
    $ python run.py db migrate
    $ python run.py db upgrade
    $ nohup python run.py runserver > logs/shop.log 2>&1>> logs/shop.log & disown
Base URL for the API

The base url for this api is https://app.swaggerhub.com/apis/ivanatu/shopping_list_API/1.0.0#/ in case you want to try out this API endpoints using curl or postman from your computer with out cloning this repository. For example, on linux commandline issue this curl command to login (you will need to first register to login, please see documentation).

#### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /auth/register | True | Create an account
POST | /auth/login | True | Login a user
POST | /auth/logout | False | Logout a user
POST | /auth/reset-password | False | Reset a user password


#### Endpoints to create, update, view and delete a shopping list
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /shoppinglists | False | Create a shopping list
GET | /shoppinglists | False | View all shopping lists
GET | /shoppinglists/id | False | View details of a shopping list
PUT | /shoppinglists/id | False | Updates a shopping list with a given id
DELETE | /shoppinglists/id | False | Deletes a shopping list with a given id

#### Endpoints to create, update, view and delete a shopping list item
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /shoppinglists/id/items | False | Add an Item to a shopping list
PUT | /shoppinglists/id/items/<item_id> | False | Update a shopping list item on a given list
DELETE | /shoppinglists/id/items/<item_id> | False | Delete a shopping list item from a given list

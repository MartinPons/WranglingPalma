# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 18:30:58 2015

@author: Martin
"""

# loading packages
from pymongo import MongoClient
import pprint

# set client
client = MongoClient('mongodb://localhost:27017/')

# loading data base
db = client.udacity

# ISSUES WITH THE DATA

# 1. Does address exists in amenities?
db.wrangling.find({"amenity": {"$exists":1}, "address":{"$exists":1}}).count()
db.wrangling.find({"amenity": {"$exists":1}, "address":{"$exists":0}}).count()
# The most part of amenities don't have the address attatch to them



for idx in q1:
    pprint.pprint(idx)

# Hepler fuction: print_query
def print_query(query):
    for idx in query:
        pprint.pprint(idx)
        
        
# Basic Statistics
        
# number of documents
db.wrangling.find().count()

# Unique users
unique_users = db.wrangling.aggregate([{"$group":{"_id":"created.user",
                                              "users": {"$addToSet":"$created.user"}}},
                                    {"$unwind":"$users"},
                                    {"$group":{"_id":"users", "count":{"$sum":1}}}])

len(db.wrangling.distinct("created.user"))
                                  
print_query(unique_users)
  
# Users distribution                                     
users_distribution = db.wrangling.aggregate([{"$group":{"_id": "$created.user"
                                                        , "count":{"$sum":1}}},
                                              {"$sort":{"count":1}}])
                                              
print_query(users_distribution)                                             

# number of nodes and ways
nodes_query = {"type":"node"}
db.wrangling.find(nodes_query).count()

ways_query = {"type":"way"}
db.wrangling.find(ways_query).count()

# Differnt types of restaurants
restaurants = db.wrangling.aggregate([{"$match":{"amenity":{"$regex":"restaurant|cafe|bar|fast_food"}}},
                                  {"$group": {"_id":"$amenity", "count":{"$sum":1}}},
                                    {"$sort":{"count":-1}}])
print_query(restaurants)
                                    
# restaurant distribution by postcode
rest_dist = db.wrangling.aggregate([{"$match":{"amenity":{"$regex":"restaurant|cafe|bar|fast_food"}}},
                                    {"$group":{"_id":"$address.postcode", 
                                              "count":{"$sum":1}}},
                                    {"$sort":{"count":-1}}])


print_query(rest_dist)
                          

# Numbers of different types of restaurants in palma and surroundings
restaurants = {"amenity": {"$regex": "restaurant|cafe|fast_food"}}

db.wrangling.find(restaurants).count()

## Schools in different cities
table = db.wrangling.aggregate([{"$match":{"amenity":{"$regex":"kindergarten|school"}}},
                                {"$group": {"_id": "$address.city",
                                            "count":{"$sum":1}}},
                                {"$sort":{"count":-1}}])

print_query(table)


## Visualization of population density dividing the city in postcodes
density = db.wrangling.aggregate([{"$group": {"_id": "$address.postcode", 
                                             "buildings":{"$sum":"$building"}}}])
print_query(density)
                                             
pr = db.wrangling.find({"building":{"$exists":1}})
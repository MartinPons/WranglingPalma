# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 18:46:41 2015

@author: Martin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 17:10:21 2015

@author: Martin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 20:15:50 2015

@author: Martin
"""

import xml.etree.cElementTree as ET
import os
import re
import lxml
from collections import defaultdict
import json

# load file

# load helpler funcions and mappings and process data functions
execfile('helpler_functions.py')
execfile('mappings.py')
execfile('process.py')

# parse data: Openstreetmap xml data from Palma de Mallorca and its surroundings
tree = ET.parse("data/palma_y_alrededores") # change for 'sample.oms' when appropiate
root = tree.getroot()

## Obtaining most frequent tags as a criteria for cleaning
sorted_tags = dict()
for child in root.iter():
    if child.tag == "tag":
        if child.get("k") not in sorted_tags:
            sorted_tags.update({child.get("k"):1})
        else:
            sorted_tags[child.get("k")] += 1

sorted_tags = sorted_tags.items()
sorted_tags = sorted(sorted_tags, key = lambda(item): item[1], reverse = True)
  
# 20 Most frequent tags          
sorted_tags[0:20]    

# To take a quick look at the names of the tags we'll execute the function "get_names"
# for each one

################################## highway #####################################
# http://wiki.openstreetmap.org/wiki/Key:highway
get_names("highway") #ok

################################## name ########################################
# http://wiki.openstreetmap.org/wiki/Key:name
get_names("name")

get_tag_types('^[aA-zZ0-9/]+', "name")[0:20]
# As we'll e later with the addr:street type we have some common firsts words
# like Carrer (Street) Avinguda (Avenue), Camí (way), etc.

# There is a mixture of catalan with spanish words as well as a mixture of lower
# cases and uppercases

# Updating names according to normalization specified in "mapping"
# (mainly, all Catalan and Capitaliztion)
for child in root.iter():
    if child.tag == "tag" and is_key(child, "name"):
        type_name = child.get("v")
        child.set("v", update_name(type_name, mapping))

    
################################## building ####################################
# http://wiki.openstreetmap.org/wiki/Buildings
get_names("building") #ok


################################## height ######################################
# http://wiki.openstreetmap.org/wiki/Key:height

# Values must be numbers interpreted in metters by default and with dot as decimal separator
get_names("height")

# All values are ok. No outliers have been found


################################# oneway #######################################
# http://wiki.openstreetmap.org/wiki/Key:oneway

# Allowed values: 'yes', 'no', and '-1'
get_names("oneway") #ok


################################ amenity #######################################
# http://wiki.openstreetmap.org/wiki/Key:amenity
get_names("amenity") #ok



################################ addr:street  ##################################
get_street_types('^[aA-zZ0-9/]+')

# A high number of street types begin with the word "Quarter". It seems to be some
# extra especification, not useful for our purposes.We'll remove it to set the typical
# names (Carrer, Avinguda...) of ways at the beggining of the name
types_with_quarter = get_street_types('^[aA-zZ0-9/]+')     

#### Remove 'Quarter ...' in street names
for child in root.iter():
    if child.tag == "tag" and is_street_name(child):
        street_name = child.get("v")
        child.set("v", re.sub("^Quarter [IXV]{1,4}, ", "", street_name))
        
types_without_quarter = get_street_types('^[aA-zZ0-9/]+')

# Checking for abbreviations at the beggining
get_street_types("^[aA-zZ0-9/]+\\.") 
# a few abbreviations for known types have been found. 
# They will be included in the mapping

# 'C.' is an ambiguous abbreviation, though. It could refer to "Carrer" (street)
# o (way) "Carretera"
# We check the entire name
get_street_types("^C\\..+")
# Saridakis is the name of a street

# Uptating street names according to 'mapping'
for child in root.iter():
    if child.tag == "tag" and is_street_name(child):
        street_name = child.get("v")
        child.set("v", update_name(street_name, mapping))
            

get_street_types('^[aA-zZ0-9\\/]+')  
get_street_types("^Cam.+")
get_street_types("carrer ")


################################# addr:housenumber #############################
# Can contain letters, dashes and other characters: http://wiki.openstreetmap.org/wiki/Key:addr


# Unify criterium: we want a number that canoptionally
#  be followed by a lowercase letter without separation
expected_numbers = "([0-9]{1,4})([aA-zZ])?"

# First, remove possible blank spaces
for child in root.iter():
    if child.tag == "tag" and child.get("k") == "addr:housenumber":
        housenumber = child.get("v")
        child.set("v", housenumber.lower())
        child.set("v", re.sub(" ", "", housenumber))
        
# Making all letters in 'addr:housenumber' lowercase                
for child in root.iter():
    if child.tag == "tag" and child.get("k") == "addr:housenumber":
        child.set("v", child.get("v").lower())
        child.set("v", re.sub(" ", "", child.get("v")))
        
get_names("addr:housenumber")    
 
# Getting not expected numbers with function "get_not_expected"
# (Actually, a building can have more than one number, we'll allow this situation)                

get_not_expected("addr:housenumber", "^(?![0-9]{1,3}[a-z]?$)")   
 
# We have different types of non-conforming numbers
# s/n. It is ok. Literally, it means w/n: without number. It is a possible numberhouse
# Strings referencing buildings: it's ok
# String with "bajos". It references the ground floor. It shoud be on the floor number. ir must be remove
# Strings referencing km points in roads. We must check that this nodes are outside of the city
# Letters before numbers. It must be an error. It should be reversed.


# Order invertion cleaning with helpler function 'invert_letter_number'
for child in root.iter():
    if child.tag == "tag" and child.attrib["k"] == "addr:housenumber":
        child.set("v", invert_letter_number(child.attrib["v"]))
   

# Removing bad names for housenumber according to mapping in 'housenumber_mapping'
for child in root.iter():
    if child.tag == "tag" and child.attrib["k"] == "addr:housenumber":
        child.set("v", update_name(child.attrib["v"], housenumber_mapping))
 

################################## addr: city ##################################
 
# City has to be one of Palma or a city belonging to its surroundings
get_names("addr:city")
 
# The main issues here are related with the city of Palma. We see lowercases and ambigouous
# denominations (both "Palma" and "Palma de Mallorca" are denominations frequently used by
# citizens and not citizens). There is also one instance with the name of the city together
# with the name of the region "Illes Balears". 
 
 
# Updating different versions for the city of Palma name according to 'palma_mapping' 
for child in root.iter():
     if child.tag == "tag" and child.attrib["k"] == "addr:city":
         child.set("v", update_name(child.attrib["v"], palma_mapping))
         
get_names("addr:city")
 

################################## addr:postcode ###############################
# postcode for Balearic Islands is a 5 figure number beggining with 07

# Searching for not expected postcodes
get_not_expected("addr:postcode", "^(?!07[0-9]{3})")

# there are two instances whit a typo. The first one seems to be a number switching.
# The second has a 1 bewteen 0 and 7

# Updating postcode fixing the typos found
for child in root.iter():
    if child.tag == "tag" and child.attrib["k"] == "addr:postcode":
        if child.attrib["v"] == "70712":
            child.set("v", "07012") 
        if child.attrib["v"] == "017160":
            child.set("v", "07160")

get_not_expected("addr:postcode", "^(?!07[0-9]{3})")

## Now all postcodes are OK.


################################## barrier ##################################### 
# http://wiki.openstreetmap.org/wiki/Key:barrier
get_names("barrier")



################################## created_by ##################################
# http://wiki.openstreetmap.org/wiki/Key:created_by

# shows different editors
get_names("created_by")

################################# leisure ######################################
# http://wiki.openstreetmap.org/wiki/Key:leisure

get_names("leisure")


################################ addr:country ##################################
# http://wiki.openstreetmap.org/wiki/Key:country

# It must be a country code: two uppercase characters: ES
get_names("addr:country") # OK


############################### access #########################################
# http://wiki.openstreetmap.org/wiki/Key:access
get_names("access") # ok

############################## addr:province ###################################
# Must be 'Illes Balears'
get_names("addr:province") #ok


# writing xml cleaned data
tree.write('data/cleaned')

# parsing into json
process_map("data/cleaned")

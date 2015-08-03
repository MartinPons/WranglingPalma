# -*- coding: utf-8 -*-
# hepler_functions.py
"""
Created on Wed Jul 22 16:53:33 2015

@author: Martin
"""

# dictionary -> list
# returns a list of two length tuples: the first element containing the name of the element
# value and the second its frequency, given a dictionary of tag value distributions    
def sort_dict_distribution(dic):
    dic = dic.items()
    dic = sorted(dic, key = lambda(item): item[1], reverse = True)
    return dic

# string -> list
# returns tag names distribution given a specific tag name
def get_names(type_key):
    names_distribution = dict()
    for child in root.iter():
        if child.tag == "tag" and child.get("k") == type_key:
            if child.get("v") not in names_distribution:
                names_distribution.update({child.get("v"): 1})
            else: 
                names_distribution[child.get("v")] += 1
    names_distribution = sort_dict_distribution(names_distribution)
    return names_distribution
    
# string, string -> list
# returns a distribution of all not expected given patterns 
# specified from an specified tag key
def get_not_expected(element_key, not_expected_pattern):
    not_expect_dist = dict()
    for child in root.iter():
        if child.tag == "tag" and child.get("k") == element_key:
            if re.search(not_expected_pattern, child.get("v")):
                not_expected = child.get("v")
                if not_expected not in not_expect_dist:
                    not_expect_dist.update({not_expected: 1})
                else:
                    not_expect_dist[not_expected] += 1
    not_expect_dist = sort_dict_distribution(not_expect_dist)
    return not_expect_dist

# string, string -> list
# Returns the first word of the tag name being analised, assumming the name 
# has differenttypes as in 'street' or 'name', thus, getting the type of the 
# street, name, etc.
def get_tag_types(pattern, tag):
    types_distribution = dict()
    for child in root.iter():
        if child.tag == "tag" and is_key(child, tag):
            if re.search(pattern, child.get("v")): 
                tag_type = re.search(pattern, child.get("v")).group()
                if tag_type not in types_distribution:
                    types_distribution.update({tag_type: 1})
                else:
                    types_distribution[tag_type] += 1
    types_distribution = sort_dict_distribution(types_distribution)
    return types_distribution

########## Lesson 6 functions and modifications #########
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    # YOUR CODE HERE
   for pat in mapping.keys():
       if re.search(pat, name):
           name = re.sub(pat, mapping[pat], name)
           break

   return name

            
def is_key(elem, key_type):
    return (elem.attrib['k'] == key_type)
    


########## addr:street functions ########

# like get_type_tags but for the street tag
def get_street_types(pattern):
    types_distribution = dict()
    for child in root.iter():
        if child.tag == "tag" and is_street_name(child):
            if re.search(pattern, child.get("v")): 
                street_type = re.search(pattern, child.get("v")).group()
                if street_type not in types_distribution:
                    types_distribution.update({street_type: 1})
                else:
                    types_distribution[street_type] += 1
    types_distribution = sort_dict_distribution(types_distribution)
    return types_distribution
    
######## addr:housenumber functions #########
    
# string -> string
# changes the order of a given string contaning first letters followed by numbers, 
# to numbers followed by letters
def invert_letter_number(hn_value):
    if re.search("^[a-z][0-9]{1,4}", hn_value):
        number = re.search("[0-9]{1,4}", hn_value).group()
        letter = re.search("[a-z]", hn_value).group()
        return number + letter
    else:
        return hn_value
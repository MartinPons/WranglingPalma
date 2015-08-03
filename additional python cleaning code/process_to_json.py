# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:12:16 2015

@author: Martin
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node = {'id':None, 'type':element.tag, 'visible': None}
        created = {'version': None, 'changeset': None, 'timestamp': None, 
                   'user': None, 'uid': None}
        address = {}
        pos = []

         # attributes and created
        for at in element.attrib.keys():
            if at in node.keys():
                node[at] = element.get(at)
            if at in created.keys():
                created[at] = element.get(at)
        
        # position
        if element.get('lat')!= None:
            pos.append(float(element.get('lat')))
        if element.get('lon')!= None:
            pos.append(float(element.get('lon')))

        # tag subelements
        for t in element.findall('tag'):
            tag_key = t.get('k')
            if problemchars.search(tag_key):
                continue
            
            # address
            elif re.search('^addr:', tag_key) and not re.search('^addr:.*:.*', tag_key):
                address.update({re.sub('^addr:', "", tag_key): t.get('v')})
                
            
            # rest of tags with ":"
            elif re.match(":", tag_key) and not re.match(".*:.*:", tag_key):
                node.update({re.sub("^.*:", "", tag_key), t.get('v')})
                
            # rest of tags    
            else:
                node.update({t.get('k'):t.get('v')})
        
        ## adding node references if way
        if node['type'] == 'way':
            node_refs = []
            for n in element.findall("nd"):
                node_refs.append(n.get('ref'))
            if len(node_refs) > 0:
                node.update({'node_refs': node_refs})
  
       # update dict       
        node.update({'created': created, 'pos': pos})
        if len(address) > 0:
            node.update({'address': address})
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    
  
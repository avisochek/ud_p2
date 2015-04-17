#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Tags.py

Super confusing what this was actually supposed to do.
I think the idea is just to have a framework 
for recording different types of tags.
"""

filename = 'lexington_kentucky.osm'
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        kval = element.attrib['k']
        if lower.search(kval):
            keys['lower']+=1
        elif lower_colon.search(kval):
            keys['lower_colon']+=1
        elif problemchars.search(kval):
            keys['problemchars']+=1
        else:
            keys['other']+=1

	if kval in keys.keys():
            keys[kval]+=1
        else:
            keys[kval] = 1
        pass
    return keys



def process_map(filename):

    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

    
	########
	########
    # the following three lines allow us
    # to access the root element from within
    # the iterator in order to clear the memory...
    # get an iterable
    context = ET.iterparse(filename, events=("start", "end"))
    # turn it into an iterator
    context = iter(context)
    # get the root element
    event, root = context.next()
	########
	########

    for _,element in context:
        keys = key_type(element, keys)
	root.clear() ## clear from memory so that computer doesn't crash...
    return keys


keys = process_map(filename);
for key,value in (sorted(keys.items())):
    print key,': ',value

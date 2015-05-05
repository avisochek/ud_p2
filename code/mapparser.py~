#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mapparser:
iterate through elements and 
record the frequency of each tag name.
"""
import xml.etree.ElementTree as ET
import pprint
filename = 'lexington_kentucky.osm'


def count_tags(filename):
    tags = {}
    i=0

    # get an iterable
    context = ET.iterparse(filename, events=("start", "end"))

    # turn it into an iterator
    context = iter(context)

    # get the root element
    event, root = context.next()

    for event,elem in context:
	i+=1
        tag = elem.tag
        if tag in tags.keys():
            tags[tag]+=1
        else:
            tags[tag] = 1
	root.clear()
    return tags

tags = count_tags(filename)
for tag,quant in tags.items():
    print tag,": ", quant

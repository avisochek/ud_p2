import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""
filename = 'lexington_kentucky.osm'

def process_map(filename):
    users = set()

    # the following three lines allow us
    # to access the root element from within
    # the iterator in order to clear the memory...
	########
	########
    # get an iterable
    context = ET.iterparse(filename, events=("start", "end"))
    # turn it into an iterator
    context = iter(context)
    # get the root element
    event, root = context.next()
	########
	########

    for _,element in context:
        if 'uid' in element.attrib.keys():
            user = element.attrib['uid']
            if user in users:
                continue
            else:
                users.add(user)
        pass
	root.clear()

    return users

users = process_map(filename)
for user in users:
	print user

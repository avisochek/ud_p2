"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected


#### NOTE, audit and update functions serve two distinc purposes 
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

filename = 'lexington_kentucky.osm'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "Ave": 'Avenue',
            'Rd.':'Road',
            "St": "Street",
            "St.": "Street"
            }


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

    for _,elem in context:

        if elem.tag == "node" or elem.tag == "nd" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        print street_type
        new_street_type = mapping[street_type]
        print new_street_type
        name = name.replace(street_type,new_street_type)
    return name


#streets = audit_streets(filename)
#for street_type,street_names in streets.items():
#	print '**',street_type
#	for street_name in street_names:
#		print '	->', street_name


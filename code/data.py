import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json



### set up pymongo
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.lexington_osm

"""
Data: iterate through the xml data,
clean it and put it into a mongodb database..
"""

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile('^addr:')
is_gnis = re.compile('^gnis:')
is_tiger = re.compile('^tiger:')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



### dictionary to replace improper 
### street names with proper ones...
Street_type_map = {
"Ln": "Lane",
"St." : "Street",
"Courth":  "Court",
"Rd"  : "Road",
"Dr." : "Drive",
"broadway":  "Broadway",
"Rd." :"Road",
"DR"   :"Drive",
"Dr" :" Drive",
"Ave." :"Avenue",
"St" :"Street",
"Ave"  :"Avenue",
"drive" :"Drive",
"Blvd"  :"Boulivard",
"Ter" :"Terrace",
"Ct" :"Court"
}

### dictionary to replace improper 
### city names with proper ones...
City_name_map = {
"Lexington, KY":"Lexington",
"Lexingotn":"Lexington",
"lexington":"Lexington",
"Lexingtion":"Lexington",
"lexingotn":"Lexington",
"lexington ky":"Lexington",
"Lexington ky":"Lexington",
"LEXINGTON":"Lexington",
"Versailles, KY":"Versailles",
"versailles":"Versailles",
"georgetown":"Georgetown",
"WILMORE":"Wilmore"
}


### replace improper 
### street names with proper ones...
def clean_street_name(street_name):
    m = street_type_re.search(street_name)
    cleaned_street_name = street_name
    if m:
        street_type = m.group()
        if street_type in Street_type_map:
            cleaned_street_name = re.split(street_type_re,street_name)[0]+Street_type_map[street_type]	
    return cleaned_street_name

### replace improper 
### city names with proper ones...
def clean_city_name(city_name):
    cleaned_city_name=city_name
    if city_name in City_name_map:
	cleaned_city_name=City_name_map[city_name]
    return cleaned_city_name


def shape_element(element):
    if element.tag == "node" or element.tag == "nd" or element.tag == "way" :
	### keep track of the element tag
	### in elem_type
        if element.tag == "way":
		elem_type="way"
	else:
		elem_type="node"
        start_node = {}
        created = {}
        pos = [0,0]
        for key,value in element.attrib.items():
            if key in CREATED:
                created[key] = value
            elif key == 'lon':
                pos[1] = float(value)
            elif key == 'lat':
                pos[0] = float(value)
            else:
                start_node[key] = value

        node = start_node
	
	#insert nested info into the 
        address = {}
	gnis ={}
	tiger = {}


        for tag in element.iter('tag'):
            kval = tag.attrib["k"]
            vval = tag.attrib['v']
            if not problemchars.search(kval) and sum([i==':' for i in kval])<2:

		### place all the addr tags in the address object,
		### clean the value if it is a street name or a city name.
                if addr.search(kval):
                    key = kval.split(':')[1]
		    if key=='street' :
                        address[key] = clean_street_name(vval)
                    elif key=='city':
                        address[key] = clean_city_name(vval)
                    else:
                        address[key] = vval
		### place all of the gnis tags in the gnis object
		###
		elif is_gnis.search(kval):
                    key = kval.split(':')[1]
                    gnis[key] = vval
		
		### place all of the tiger tags in the tiger object
		elif is_tiger.search(kval):
                    key = kval.split(':')[1]
                    tiger[key] = vval

		### all other key value pairs entered straight into the node.
                else:
                    node[kval] = vval

	## for each object, check if it is used,
	## and then add it to the node if it is...
        if created:
        	node['created'] = created
        if address:
        	node['address'] = address
        if pos:
            node['pos'] = pos
	if tiger:
	    node['tiger'] = tiger
	if gnis:
	    node['gnis'] = gnis
	node["type"]=elem_type
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    #with codecs.open(file_out, "w") as fo:
 # get an iterable
    context = ET.iterparse(file_in, events=("start", "end"))
    # turn it into an iterator
    context = iter(context)
    # get the root element
    event, root = context.next()
#######
########

    ### iterate through the elements, 
    ### cleaning the data and insert them into 
    ### the database...

    for _,element in context:
        el = shape_element(element)
        if el:
            data.append(el)
            ##if pretty: this doesn't matter since we're using mongodb 
              ##  db.insert(json.dumps(el, indent=2)+"\n")
            #else
            db.fourth_run.insert(el)
    print data[0]
    return data


file_in = '/home/allan/Documents/data_science/p2/submission/data/lexington_kentucky.osm'
process_map(file_in)

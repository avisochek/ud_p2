import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
Data: this is basically to put the data in the right format...
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile('^addr:')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    if element.tag == "node" or element.tag == "way" :

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

	insert nested info into the 
        address = {}
	gnis ={}
	tiger = {}


        for tag in element.iter('tag'):
            kval = tag.attrib["k"]
            vval = tag.attrib['v']
            if not problemchars.search(kval) and sum([i==':' for i in kval])<2:
                if addr.search(kval):
                    key = kval.split(':')[1]
                    address[key] = vval
		elif is_gnis.search(kval):
                    key = kval.split(':')[1]
                    gnis[key] = vval
		elif is_tiger.search(kval):
                    key = kval.split(':')[1]
                    tiger[key] = vval
                else:
                    node[kval] = vval

	## insert nexted values...
        if created:
        	node['created'] = created
        if address:
		address = clean_address(adress)
        	node['address'] = address
        if pos:
            node['pos'] = pos
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
	 # get an iterable
    	context = ET.iterparse(file_in, events=("start", "end"))
    	# turn it into an iterator
    	context = iter(context)
    	# get the root element
    	event, root = context.next()
	########
	########

    	for _,element in context:
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    print data[0]
    return data


file_in = 'lexington_kentucky.osm'
process_map(file_in)

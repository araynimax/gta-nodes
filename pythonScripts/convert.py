import xml.etree.ElementTree as ET
import json
from functools import cmp_to_key

print('Parsing xml...')

objects = ET.parse("../data/paths.xml").findall("./objects/object")

print('Generating Lists...')

# replace guids with simple indexes
guidCounter = 1
guids = {}

def getIndexforGUID(guid):
    global guidCounter
    index = guids.get(guid)
    if index == None:
        guids[guid] = guidCounter
        index = guidCounter
        guidCounter += 1
    return index


def writeData(file, *args):
    for data in args:
        file.write(data)
        file.write(" ")
    file.write("\n")


nodes = []
links = []

# push into list
for obj in objects:
    objectClass = obj.get("class")
    coords = obj.find("./transform/object/position")
    x = coords.get("x")
    y = coords.get("y")
    z = coords.get("z")
    dataDict = {"pos": {"x": x, "y": y, "z": z}}

    attributes = obj.findall("./attributes/attribute")
    attributesDict = {}
    for attribute in attributes:
        attributesDict[attribute.get("name")] = attribute.get("value")

    if objectClass == "vehiclenode":
        guid = str(getIndexforGUID(obj.get("guid")))
        dataDict["guid"] = guid
        dataDict["attributes"] = attributesDict
        nodes.append(dataDict)
    elif objectClass == "vehiclelink":
        refs = obj.findall("./references/ref")
        fromId = str(getIndexforGUID(refs[0].get("guid")))
        toId = str(getIndexforGUID(refs[1].get("guid")))
        dataDict["fromId"] = fromId
        dataDict["toId"] = toId
        dataDict["attributes"] = attributesDict
        links.append(dataDict)


print('=> Created a lists with {} Nodes and {} Links'.format(len(nodes), len(links)))

print('Filtering..')

# convert node array to dict
nodesDict = {}

for node in nodes:
  nodesDict[node['guid']] = node

# filtering

linksBefore = len(links)
nodesBefore = len(links)

def removeLinkFromList(link):
  isWaterLink = nodesDict[link["fromId"]]['attributes'].get('Water', 'false') == 'true' or nodesDict[link["toId"]]['attributes'].get('Water', 'false') == 'true'
  noGPS = nodesDict[link["fromId"]]['attributes'].get('NoGps', 'false') == 'true' or nodesDict[link["toId"]]['attributes'].get('NoGps', 'false') == 'true'
  eventNodes = nodesDict[link["fromId"]]['attributes'].get('Special', 'false') == '14' or nodesDict[link["toId"]]['attributes'].get('Special', 'false') == '14'
  pedCrossings = nodesDict[link["fromId"]]['attributes'].get('Special', 'false') == '10' or nodesDict[link["toId"]]['attributes'].get('Special', 'false') == '10'
  pedCrossings2 = nodesDict[link["fromId"]]['attributes'].get('Special', 'false') == '18' or nodesDict[link["toId"]]['attributes'].get('Special', 'false') == '18'
  return isWaterLink or noGPS or eventNodes or pedCrossings or pedCrossings2
  
links = [x for x in links if not removeLinkFromList(x)]

def removeNodeFromList(node):
  isWaterNode = node['attributes'].get('Water', 'false') == 'true'
  noGPS = node['attributes'].get('NoGps', 'false') == 'true'
  eventNodes = node['attributes'].get('Special', 'false') == '14'
  pedCrossings = node['attributes'].get('Special', 'false') == '10'
  pedCrossings2 = node['attributes'].get('Special', 'false') == '18'

  return isWaterNode or noGPS or eventNodes or pedCrossings or pedCrossings2

nodes = [x for x in nodes if not removeNodeFromList(x)]

print('=> Removed {} Nodes and {} Links'.format(nodesBefore - len(nodes), linksBefore - len(links)))

# extend link attributes
print('Manipulating attributes..')

for link in links:
  nodeFrom = nodesDict[link['fromId']]
  speed = nodeFrom['attributes'].get('Speed', '1')

  if speed == '0':
    speed = '30'
  elif speed == '1':
    speed = '50'
  elif speed == '2':
    speed = '70'
  elif speed == '3':
    speed = '100'

  # speed = '1'
  if link['attributes'].get('Narrowroad', 'false') == 'true':
    speed = "50"
  if link['attributes'].get('Off Road', 'false') == 'true':
    speed = "20"
    
  link['attributes']['Speed'] = speed
  node['attributes'].pop('Off Road', None)
  


for node in nodes:
  node['attributes'].pop('Speed', None)
  node['attributes'].pop('Off Road', None)


# convert list to json and write it to files
print('Saving to files..')

fileNodes = open("../data/gta_nodes.json", "w")
fileLinks = open("../data/gta_links.json", "w")

fileNodes.write(json.dumps(nodes))
fileLinks.write(json.dumps(links))

fileNodes.close()
fileLinks.close()

print('=> Saved a total of {} Nodes and {} Links'.format(len(nodes), len(links)))


# generate attribute list

# linkAttributes = {}

# for link in links:
#   for attributeName in link['attributes']:
#     value = link['attributes'][attributeName]
#     if attributeName not in linkAttributes:
#       linkAttributes[attributeName] = {}
#     if value not in linkAttributes[attributeName]:
#       linkAttributes[attributeName][value] = 0
#     linkAttributes[attributeName][value] = linkAttributes[attributeName][value] + 1

# nodeAttributes = {}

# for node in nodes:
#   for attributeName in node['attributes']:
#     value = node['attributes'][attributeName]
#     if attributeName not in nodeAttributes:
#       nodeAttributes[attributeName] = {}
#     if value not in nodeAttributes[attributeName]:
#       nodeAttributes[attributeName][value] = 0
#     nodeAttributes[attributeName][value] = nodeAttributes[attributeName][value] + 1

# fileNodes = open("../data/node_attributes.json", "w")
# fileLinks = open("../data/link_attributes.json", "w")
# fileNodes.write(json.dumps(nodeAttributes))
# fileLinks.write(json.dumps(linkAttributes))
# fileNodes.close()
# fileLinks.close()

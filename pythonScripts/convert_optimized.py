import xml.etree.ElementTree as ET
import json
import base62

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
        guids[guid] = base62.encode(guidCounter)
        guidCounter += 1
    return guids[guid]


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
    dataDict = {"pos": {"x": float(x), "y": float(y), "z": float(z)}}

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

linksArray = []

for link in links:
  nodeFrom = nodesDict[link['fromId']]
  speed = nodeFrom['attributes'].get('Speed', '1')

  if speed == '0':
    speed = 30
  elif speed == '1':
    speed = 50
  elif speed == '2':
    speed = 70
  elif speed == '3':
    speed = 100

  if link['attributes'].get('Narrowroad', 'false') == 'true':
    speed = 50
  if link['attributes'].get('Off Road', 'false') == 'true':
    speed = 20

  lanes_out = int(link['attributes'].get('Lanes Out', '1'))
  lanes_in = int(link['attributes'].get('Lanes In', '1'))
  one_way = 0 # 0 = false || 1 = lanesOut || 2 = lanesIn

  if lanes_out == 0:
    one_way = 1
  elif lanes_in == 0:
    one_way = 2

  # linksArray.append(link.get('pos')['x'])
  # linksArray.append(link.get('pos')['y'])
  # linksArray.append(link.get('pos')['z'])
  linksArray.append(link.get('fromId'))
  linksArray.append(link.get('toId'))
  linksArray.append(speed)
  linksArray.append(one_way)
  
nodesArray = []

for node in nodes:
  nodesArray.append(node.get('guid'))
  nodesArray.append(node.get('pos')['x'])
  nodesArray.append(node.get('pos')['y'])
  nodesArray.append(node.get('pos')['z'])
  nodesArray.append(node.get('attributes').get('Special', 'NOT SET'))


# convert list to json and write it to files
print('Saving to files..')

fileLinks = open("../data/gta_paths.json", "w")
fileLinks.write(json.dumps({"nodes": nodesArray, "links": linksArray}, separators=(',', ':')))
fileLinks.close()

print('=> Saved a total of {} Nodes and {} Links'.format(len(nodes), len(links)))

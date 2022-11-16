from PIL import Image, ImageDraw
import json
import sys
import math

with open('../data/gta_paths.json', 'r') as f:
    paths = json.load(f)

nodes = []

for i in range(0, len(paths['nodes']) - 1, 4):
  nodes.append({
    "id": paths['nodes'][i],
    "pos": {
      "x": paths['nodes'][i+1],
      "y": paths['nodes'][i+2],
      "z": paths['nodes'][i+3],
    }
  })


links = []

for i in range(0, len(paths['links']) - 1, 4):
  links.append({
    "fromId": paths['links'][i],
    "toId": paths['links'][i+1],
    "speed_limit": paths['links'][i+2],
    "one_way": paths['links'][i+3],
  })

coordSize = 660/1000
offset = {
  "top" : 5525,
  "left": 3756,
}

# draw functions
im = Image.new('RGBA', (8192, 8192))
draw = ImageDraw.Draw(im)

def line(x1, y1, x2, y2, color = 'black', width=1):
  x1 *= coordSize;
  x1 += offset["left"];
  y1 *= coordSize;
  y1 *= -1;
  y1 += offset["top"];

  x2 *= coordSize;
  x2 +=  offset["left"];
  y2 *= coordSize;
  y2 *= -1;
  y2 += offset["top"];
  
  draw.line([
    (x1, y1),
    (x2, y2)
  ], fill=color, width=width)

def circle(x1, y1, size, color = 'red'):
  x1 *= coordSize;
  x1 += offset["left"];
  y1 *= coordSize;
  y1 *= -1;
  y1 += offset["top"];
  
  draw.ellipse((x1 - (size/2), y1 - (size/2), x1 + size, y1 + size), fill = color)



# convert node array to dict
nodesDict = {}

for node in nodes:
  nodesDict[node['id']] = node

for link in links:
  color = 'black'
  width = 2

  nodeFrom = nodesDict.get(link['fromId'])
  nodeTo   = nodesDict.get(link['toId'])
  posFrom = nodeFrom.get('pos')
  posTo   = nodeTo.get('pos')

  line(posFrom['x'], posFrom['y'], posTo['x'], posTo['y'], color, width)


for node in nodes:
  nodePos = node['pos']
  color = 'red'
  size = 2

  circle(float(nodePos["x"]), float(nodePos["y"]), size, color) 


im.save("../output/gta_nodes.png", "PNG")
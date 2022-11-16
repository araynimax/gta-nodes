const createGraph = require('ngraph.graph');
const path = require('ngraph.path');
window.graph = createGraph();
const createTree = require('yaqt');


const nodes = require('../data/gta_nodes.json')
const links = require('../data/gta_links.json')

const points = [];
const pointNodeDict = {};


nodes.forEach(node => {
  const { guid, pos, attributes } = node;
  graph.addNode(guid, {
    pos,
    ...attributes
  });
  pointNodeDict[pos.x+pos.y] = node;
  points.push(Number(pos.x), Number(pos.y))
});


links.forEach(link => {
  const { guid, pos, attributes, fromId, toId } = link;
  graph.addLink(fromId, toId, {
    pos,
    ...attributes
  });
});

const tree = createTree();
tree.init(points);


window.findNodesAround = (x,y,r) => {
  r = r || 1;
  const foundPoints = tree.pointsAround(x,y,r);
  if(foundPoints.length) {
    return foundPoints
      .map(key => ({x: points[key], y: points[key+1]}))
      .map(coord => pointNodeDict[String(coord.x) + String(coord.y)]);
  } else {
    return findNodesAround(x,y,r+1);
  }
};


//module.exports = graph;
window.pathFinder = path.aStar(graph, {
  // We tell our pathfinder what should it use as a distance function:
  distance(fromNode, toNode, link) {
    // We don't really care about from/to nodes in this case,
    const lanesIn = parseInt(link.data['Lanes In'], 10);
    const lanesOut = parseInt(link.data['Lanes Out'], 10);
    const speed = parseInt(link.data['Speed'], 10);
    // wrong way

    let multiplicator = speed/100 * -1 + 2;

    //console.log(speed,multiplicator);

    if ( lanesOut === 0 && fromNode.id === link.toId || lanesIn === 0 && fromNode.id === link.fromId) return Number.MAX_SAFE_INTEGER;

    return Math.sqrt((toNode.data.pos.x - fromNode.data.pos.x) ** 2 + (toNode.data.pos.y - fromNode.data.pos.y) ** 2 + (toNode.data.pos.z - fromNode.data.pos.z) ** 2) * multiplicator;
  },
  heuristic(fromNode, toNode) {
    return Math.sqrt((toNode.data.pos.x - fromNode.data.pos.x) ** 2 + (toNode.data.pos.y - fromNode.data.pos.y) ** 2 + (toNode.data.pos.z - fromNode.data.pos.z) ** 2);
  }
});

//let foundPath = pathFinder.find("187", "18787");
// let foundPath = pathFinder.find("18787", "187");
// let foundPath = pathFinder.find("1887", "2187");
// let foundPath = pathFinder.find("1337", "420");
// let foundPath = pathFinder.find("1234", "5678");





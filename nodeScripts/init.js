const path = require('ngraph.path');
const calcDistance = (p1, p2) => Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);

module.exports = (pathFinderOptions = {}) => {
  const nodes = require('../data/gta_nodes.json');
  const links = require('../data/gta_links.json');

  date = Date.now();
  const graph = require('ngraph.graph')();
  const tree = require('yaqt')();

  const points = [];
  const nodeDict = {};

  for (const node of nodes) {
    const { guid, pos, attributes } = node;

    graph.addNode(guid, {
      pos,
      ...attributes
    });

    points.push(Number(pos.x), Number(pos.y));
    nodeDict[points.length - 2] = guid;
  }

  for (const link of links) {
    const { pos, attributes, fromId, toId } = link;

    graph.addLink(fromId, toId, {
      pos,
      ...attributes
    });
  }

  tree.init(points);

  const findNearestNode = (x, y, r = 1) => {
    let points = tree.pointsAround(x, y, r);
    points = points
      .map(index => graph.getNode(nodeDict[index]))
      .sort((a, b) => calcDistance(a.data.pos, { x, y }) - calcDistance(b.data.pos, { x, y }));

    if (points.length) {
        return points[0];
    }

    return findNearestNode(x, y, r+1);
  };

  const pathFinder = path.aStar(graph, pathFinderOptions)

  return {
    graph,
    findNearestNode,
    pathFinder,
    points,
    nodes,
    links,
  };
}
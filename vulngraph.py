import networkx as nx
from dataclasses import asdict

class VulnGraph:
    def __init__(self):
        self.g = nx.MultiDiGraph()

    def addNode(self, node):
        self.g.add_node(node.id, **asdict(node))

    def addEdge(self, src, dst, relation, **attrs):
        self.g.add_edge(src, dst, relation=relation, **attrs)

    def neighbors(self, nodeID):
        return list(self.g.neighbors(nodeID))
    
    def shortPath(self, src, dst):
        return nx.shortest_path(self.g, src, dst)
    
    def hasPath(self, src, dst):
        return nx.has_path(self.g, src, dst)
    
def buildPath(graph, cve_id):
    for node in graph.g.nodes:
        if graph.g.nodes[node]["type"] == "IMAGE":
            if graph.hasPath(cve_id, node):
                return graph.shortPath(cve_id, node)
    return None
#path = buildPath(gra, CVE)
#print(path)

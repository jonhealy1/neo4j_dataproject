from py2neo import Graph
from igraph import Graph as IGraph
graph = Graph(password="password")
print(igraph.__version__)
query = '''
MATCH (c1:Subreddit)-[r:LINK]->(c2:Subreddit)
RETURN c1.id, c2.id, r.weight AS weight
'''

ig = IGraph.TupleList(graph.run(query), weights=True)
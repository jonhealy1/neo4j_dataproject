from py2neo import Graph, Node, Relationship

graph = Graph(password="password")

# create constraint 
print(graph.run("CREATE CONSTRAINT ON (s:Subreddit) ASSERT s.id IS UNIQUE;"))

# load data and create links between source and target 
query = '''
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "file:////matrix1_neg.csv" as row
MERGE (s:Subreddit{id:row.source})
MERGE (t:Subreddit{id:row.target})
CREATE (s)-[:LINK{post_id:row.POST_ID,
   weight:toInteger(row.weight)}]->(t)
'''

# run query
data = graph.run(query)
print(data)

# print number of links by year
print("---Number of LINKS ---")
example = graph.run("MATCH ()-[r:LINK]->() RETURN count(*) as count")
print(example.to_data_frame())


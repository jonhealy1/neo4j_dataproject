from py2neo import Graph, Node, Relationship

graph = Graph(password="password")

# create constraint 
print(graph.run("CREATE CONSTRAINT ON (s:Subreddit) ASSERT s.id IS UNIQUE;"))

# load data and create links between source and target 
query = '''
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "file:////soc-redditHyperlinks-title.tsv" as row FIELDTERMINATOR "\t"
MERGE (s:Subreddit{id:row.SOURCE_SUBREDDIT})
MERGE (t:Subreddit{id:row.TARGET_SUBREDDIT})
CREATE (s)-[:LINK{post_id:row.POST_ID,
   link_sentiment:toInteger(row.LINK_SENTIMENT),
   date:localDateTime(replace(row['TIMESTAMP'],' ','T'))}]->(t)
'''

# run query
data = graph.run(query)
print(data)

# print number of links by year
print("---Number of LINKS by Year---")
example = graph.run("MATCH ()-[r:LINK]->() RETURN r.date.year as year,count(*) as count ORDER BY year")
print(example.to_data_frame())


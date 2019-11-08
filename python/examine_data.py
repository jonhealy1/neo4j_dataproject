from py2neo import Graph, Node, Relationship
import sys
graph = Graph(password="password")

if (len(sys.argv) < 2):
    print("Missing argument - lpa, regular, eigen, eigen2, eigen3, singlesub or pagerank")

elif (sys.argv[1]=="regular"):

    # total number of nodes
    print("--- Total # of Nodes ---")
    numNodes = graph.run("MATCH (s:Subreddit) RETURN count(s)")
    print(numNodes.to_data_frame())

    # average number of interactions
    print("--- Avg. Interactions ---")
    numNodes = graph.run("MATCH (c:Subreddit)-[:LINK]->() WITH c, count(*) AS num \
        RETURN min(num) AS min, max(num) AS max, avg(num) \
        AS avg_interactions, stdev(num) AS stdev")
    print(numNodes.to_data_frame())

    # # find pivotal nodes - pivotal if it lies on all shortest paths between two other nodes in the network
    # print("--- Pivotal Nodes ---")
    # numNodes = graph.run("MATCH (a:Subreddit), (b:Subreddit) \
    #     MATCH p=allShortestPaths((a)-[:LINK*]-(b)) WITH collect(p) AS paths, a, b \
    #     MATCH (c:Subreddit) WHERE all(x IN paths WHERE c IN nodes(x)) AND NOT c IN [a,b] \
    #     RETURN a.id, b.id, c.id AS PivotalNode SKIP 490 LIMIT 10")
    # print(numNodes.to_data_frame())

    # degree centrality
    print("--- Degree Centrality Top 30 ---")
    numNodes = graph.run("MATCH (c:Subreddit) \
        RETURN c.id AS node, size( (c)-[:LINK]-() ) AS degree ORDER BY degree DESC LIMIT 30")
    print(numNodes.to_data_frame())

    # weighted degree centrality
    print("--- Weighted Degree Centrality Top 30 ---")
    numNodes = graph.run("MATCH (c:Subreddit)-[r:LINK]-() \
        RETURN c.id AS node, sum(r.weight) \
        AS weightedDegree ORDER BY weightedDegree LIMIT 30")
    print(numNodes.to_data_frame())

    # betweeness centrality
    print("--- Betweeness Centrality Top 30 ---")
    numNodes = graph.run("CALL algo.betweenness.stream() \
        YIELD nodeId, centrality MATCH (user:Subreddit) \
        WHERE id(user) = nodeId \
        RETURN user.id AS user,centrality \
        ORDER BY centrality DESC LIMIT 30")
    print(numNodes.to_data_frame())


    # print number of links by year
    print("--- Number of LINKS by Year ---")
    numLinksYear = graph.run("MATCH ()-[r:LINK]->() RETURN r.date.year as year,count(*) as count ORDER BY year")
    print(numLinksYear.to_data_frame())

    # number of links by post
    print("--- Number of LINKS by Post ---")
    numLinksPost = '''
        MATCH (s:Subreddit)-[r:LINK]->() RETURN r.post_id as post,count(*) as count ORDER BY count DESC LIMIT 10
    '''
    ex = graph.run(numLinksPost)
    print(ex.to_data_frame())

elif (sys.argv[1]=="singlesub"):
    # single subreddit through the years
    print("--- Subreddit Through the Years ---")
    eigen = '''
        MATCH (s:Subreddit{id:'funny'})-[e:EIGEN]->(y:Year) 
        RETURN s.id as subreddit, y.value as year,
        sum(CASE WHEN e.sentiment = 1 THEN e.score END) as positive_sentiment,
        sum(CASE WHEN e.sentiment = -1 THEN e.score END) as negative_sentiment
        ORDER BY year
    '''
    e2 = graph.run(eigen)
    print(e2.to_data_frame())

    ''' Multigraph '''
elif (sys.argv[1]=="eigen"):
    # eigenvector centrality algorithm 
    print("--- Eigenvector Centrality ---")
    eigen = '''
        CALL algo.eigenvector.stream('Subreddit','LINK')
        YIELD nodeId,score
        RETURN algo.getNodeById(nodeId).id as subreddit,score
        ORDER BY score DESC LIMIT 10
    '''
    e2 = graph.run(eigen)
    print(e2.to_data_frame())

elif (sys.argv[1]=="eigen2"):
    # eigenvector centrality top 5 positive and negative 
    print("--- Top 5 Positive and Negative ---")
    eigen = '''
        UNWIND [-1, 1] as sentiment
        CALL algo.eigenvector.stream(
        'MATCH (s:Subreddit) return id(s) as id',
        'MATCH (s:Subreddit)-[r:LINK]->(t:Subreddit)
        // Use parameter
        WHERE r.link_sentiment = $sentiment
        // Deduplicate relationships
        WITH id(s) as source,id(t) as target,count(*) as count
        RETURN source,target',
        {graph:'cypher', params:{sentiment:sentiment}})
        YIELD nodeId,score
        WITH sentiment,algo.getNodeById(nodeId).id as id,score
        ORDER BY score DESC
        RETURN sentiment,collect(id)[..5] as top5
    '''
    e2 = graph.run(eigen)
    print(e2.to_data_frame())

elif (sys.argv[1]=="eigen3"):
    # eigenvector centrality top 5 positive and negative by year 
    print("--- Top 5 Positive and Negative By Year ---")
    store_results = '''
        // Get year and sentiment
        UNWIND [-1, 1] as sentiment
        UNWIND range(2014,2017) as year
        CALL algo.eigenvector.stream(
            'MATCH (s:Subreddit) return id(s) as id',
            'MATCH (s:Subreddit)-[r:LINK]->(t:Subreddit)
            // Use parameters 
            WHERE r.link_sentiment = $sentiment AND r.date.year = $year
            // Deduplicate relationships
            WITH id(s) as source,id(t) as target,count(*) as count
            RETURN source,target',
            {graph:'cypher', params:{sentiment:sentiment,year:year}})
        YIELD nodeId,score
        WITH sentiment,year,algo.getNodeById(nodeId) as node,score
        // Filter out very low eigenvector centrality scores
        // before storing results
        WHERE score > 1
        MERGE (y:Year{value:year})
        MERGE (node)-[e:EIGEN{sentiment:sentiment}]->(y)
        ON CREATE SET e.score = score
    '''
    graph.run(store_results)

    eigen = '''
        MATCH (sub:Subreddit)-[e:EIGEN]->(year)
        WITH year,e.sentiment as sentiment,e.score as score,sub
        ORDER BY score DESC
        // One way of limiting by row is by using collect()[..x]
        RETURN year.value as year,
            sentiment,
            collect(sub['id'])[..5] as top_5
        ORDER BY year,sentiment
    '''
    e2 = graph.run(eigen)
    print(e2.to_data_frame())

    ''' Cypher Projection '''
elif (sys.argv[1]=="pagerank"):  
    # weighted pageRank
    print("--- Weighted PageRank ---")
    pageR = '''
        CALL algo.pageRank.stream(
        // Node statement
        'MATCH (s:Subreddit) RETURN id(s) as id',
        // Relationship statement
        'MATCH (s:Subreddit)-[:LINK]->(t:Subreddit)
        RETURN id(s) as source, id(t) as target, count(*) as weight',
        {graph:'cypher',weightProperty:'weight'})
        YIELD nodeId,score
        RETURN algo.getNodeById(nodeId).id as subreddit, score
        ORDER BY score DESC LIMIT 10
    '''
    e3 = graph.run(pageR)
    print(e3.to_data_frame())
elif (sys.argv[1]=="lpa"):
    # Label propagation algorithm for community detection
    print("--- Label Propagation ---")
    # return top 5 communities
    lpa = '''
    CALL algo.labelPropagation.stream(
        "Subreddit", "LINK",
        {direction: "OUTGOING", iterations: 10}) 
    YIELD nodeId, label
    RETURN label, count(*) as size, collect(algo.asNode(nodeId).id) 
    as subreddits 
    ORDER BY size DESC LIMIT 5
    '''
    e4 = graph.run(lpa)
    print(e4.to_data_frame())


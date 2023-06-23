# freight-transport-data
A simple project based on [freight transport data](https://www.kaggle.com/datasets/giobbu/belgium-obu) that are analyzed with new technologies : 
- MongoDB for store the data in related documents, 
- Neo4j for produce graphs and plots for analyze data <br>
To make installation easy, a docker compose file is offered.
To run docker services, locate in the project folder and run ```docker-compose up``` for  run and view logs or ```docker-compose up -d``` for run without logs on shell.  Once the execution is finished , type ```docker-compose down```


CALL apoc.mongo.find('mongodb://mongo:27017/mydb.polygons') YIELD value
WITH value.coordinate AS coordinates
UNWIND range(0, size(coordinates) - 2) AS idx
WITH coordinates[idx] AS current, coordinates[idx + 1] AS next
MERGE (c:Coordinate {lat: current.lat, lon: current.lon})
MERGE (n:Coordinate {lat: next.lat, lon: next.lon})
MERGE (c)-[:NEXT]->(n)

MATCH (c:Coordinate)-[:NEXT]->(n:Coordinate)
RETURN c, n

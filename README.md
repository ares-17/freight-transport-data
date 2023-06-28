# freight-transport-data
A simple project based on [freight transport data](https://www.kaggle.com/datasets/giobbu/belgium-obu) that are analyzed with new technologies : 
- MongoDB for store the data in related documents, 
- Neo4j for produce graphs and plots for analyze data <br>
To make installation easy, a docker compose file is offered.
To run docker services, locate in the project folder and run ```docker-compose up``` for  run and view logs or ```docker-compose up -d``` for run without logs on shell.  Once the execution is finished , type ```docker-compose down```

CALL apoc.mongo.find('mongodb://mongo:27017/mydb.polygons') YIELD value
WITH value.streets AS streets
UNWIND range(0, size(streets) - 1) AS street_id
WITH streets[street_id] AS current
UNWIND range(0, size(current.coords) - 2) AS coord_id
WITH current.coords[coord_id] AS current_c, current.coords[coord_id + 1] AS next_c, current.traffic AS traffic
MERGE (c1:Coordinate {latitude: current_c[1], longitude: current_c[0], color: '#ffffff00'})
MERGE (c2:Coordinate {latitude: next_c[1], longitude: next_c[0], color: '#ffffff00'})
MERGE (c1)-[n:NEXT]->(c2)
ON CREATE SET n.traffic = traffic
ON MATCH SET n.traffic = traffic

# freight-transport-data
A simple project based on [freight transport data](https://www.kaggle.com/datasets/giobbu/belgium-obu) that are analyzed with new technologies : 
- MongoDB for store the data in related documents, 
- Neo4j for produce graphs and plots for analyze data <br>
To make installation easy, a docker compose file is offered.
To run docker services, locate in the project folder and run ```docker-compose up``` for  run and view logs or ```docker-compose up -d``` for run without logs on shell.  Once the execution is finished , type ```docker-compose down```
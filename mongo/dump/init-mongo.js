use('mydb');

const data = require('/home/aress/Documenti/NoSQL/neo4j/freight-transport-data/mongo/dump/Anderlecht_streets.json');

function mapCoordinates(coordinate){
  return {
    latitude: coordinate[1],
    longitude: coordinate[0],
  }
}

function mapStreetToCoordinates(street){
  return street.geometry.coordinates[0].map(coord => mapCoordinates(coord))
}

document = {name : 'Anderlect'}
streets = data.features
document.streets = streets.map(street => mapStreetToCoordinates(street))

// Create a new document in the collection.
db.getCollection('polygons').insertOne(document);

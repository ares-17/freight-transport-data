import data from './dataset/Anderlecht_streets.json' assert { type: "json" };

function mapCoordinates(coordinate) {
  return {
    latitude: coordinate[1],
    longitude: coordinate[0],
  }
}

function mapStreetToCoordinates(street) {
  return street.geometry.coordinates[0].map(coord => mapCoordinates(coord))
}

const document = { name: 'Anderlect' }
const streets = data.features
document.streets = streets.map(street => mapStreetToCoordinates(street))


async function execute(client){
  await client.db('mydb').collection('polygons').insertOne(document);
}

export { execute }
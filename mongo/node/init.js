import data from './dataset/Anderlecht_streets.json' assert { type: "json" };

function mapCoordinates(coordinate) {
  return [
    coordinate[1],
    coordinate[0]
  ]
}

function mapStreetToCoordinates(street) {
  return {
    coords: street.geometry.coordinates[0].map(coord => mapCoordinates(coord)),
    traffic: 0,
    velocity: 0
  }
}

const document = { name: 'Anderlect' }
const streets = data.features
document.streets = streets.map(street => mapStreetToCoordinates(street))


async function execute(client){
  await client.db('mydb').collection('polygons').insertOne(document);
}

export { execute }
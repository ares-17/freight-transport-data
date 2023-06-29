import anderlecht from './dataset/Anderlecht_streets.json' assert { type: "json" };
import belgium from './dataset/Belgium_streets.json' assert { type: "json" };
import bruxelles from './dataset/Bruxelles_streets.json' assert { type: "json" };
//import data from './dataset/bruxelles.json' assert { type: "json" };

const max = 10
const min = 1
const street_coordinates = 6
const cities = [
  { name: 'anderlecht', data: anderlecht },
  { name: 'belgium', data: belgium },
  { name: 'bruxelles', data: bruxelles }
]

function getFixedArrayPolygon(array, size) {
  if (array.length === 0 || array.length <= size) {
    return array;
  }

  const result = [array[0]]
  size -= 2

  const step = Math.floor(array.length / size);

  for (let i = 0; i < size; i++) {
    const index = i * step % array.length;
    result.push(array[index]);
  }

  result.push(array[0])
  return result
}

function mapStreetToCoordinates(street) {
  const coords = getFixedArrayPolygon(street.geometry.coordinates[0], street_coordinates);
  return {
    coords: coords,
    traffic: Math.random() * (max - min) + min,
    velocity: 0
  }
}

const documents = cities.map(city => {
  return {
    name: city.name,
    streets: city.data.features.map(street => mapStreetToCoordinates(street))
  }
})

async function execute(client) {
  await client.db('mydb').collection('polygons').insertMany(documents);
}

export { execute }
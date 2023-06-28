import data from './dataset/Anderlecht_streets.json' assert { type: "json" };

/*
function getCenter(coordinates) {
  let south = coordinates[0]
  let north = coordinates[0]
  let ovest = coordinates[0]
  let est = coordinates[0]

  for (const coord of coordinates) {
    if (south[0] > coord[0]) {
      south = coord
    } else if (north[0] < coord[0]) {
      north = coord
    } else if (ovest[1] < coord[1]) {
      ovest = coord
    } else if (est[1] > coord[1]) {
      est = coord
    }
  }
  let latitude = (south[0] + north[0]) / 2
  let longitude = (ovest[1] + est[1]) / 2
  let center = [latitude, longitude]
  console.log(center)
  return center
} */

function getFixedArrayPolygon(array, size){
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

function mapCoordinates(coordinate) {
  return [
    coordinate[1],
    coordinate[0]
  ]
}

const max = 10
const min = 1

// coords: getCenter(street.geometry.coordinates[0]),
function mapStreetToCoordinates(street) {
  const coords = getFixedArrayPolygon(street.geometry.coordinates[0], 8);
  return {
    //coords: street.geometry.coordinates[0].map(coord => mapCoordinates(coord)),
    coords : coords,
    traffic: Math.random() * (max - min) + min,
    velocity: 0
  }
}

const document = { name: 'Anderlect' }
const streets = data.features
document.streets = streets.map(street => mapStreetToCoordinates(street))


async function execute(client) {
  await client.db('mydb').collection('polygons').insertOne(document);
}

export { execute }
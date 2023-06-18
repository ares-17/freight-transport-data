// Ottenere l'elenco dei database
var databases = db.adminCommand({ listDatabases: 1 }).databases;

use("cities")

db.cities.insertOne({name : "Belgium", streets : 200})

// Stampa l'elenco dei database
print("Database disponibili:");
databases.forEach(function(database) {
  printjson(database.name);
});

db.cities.find().pretty()
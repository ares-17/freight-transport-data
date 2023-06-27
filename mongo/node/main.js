import pkg from 'mongodb';
const { MongoClient } = pkg;
import { execute } from './init.js'

const url = 'mongodb://mongo:27017/';

async function checkIsEmpty() {
    const client = new MongoClient(url);
    try {
        await client.connect();
        const result = await client.db('mydb').listCollections().toArray();
        return !Array.isArray(result) || !result.length
    } catch (err) {
        console.error('Error:', err);
    } finally {
        await client.close();
    }
}


async function runOnMongo(callback) {
    const client = new MongoClient(url);
    try {
        await client.connect();
        await callback(client)
    } catch (err) {
        console.error('Error:', err);
    } finally {
        await client.close();
    }
}

async function main() {
    const isEmpty = await checkIsEmpty()
    if (isEmpty) {
        console.log('database is empty!')
        runOnMongo(client => execute(client))
    } else {
        console.log('database is not empty!, exiting...')
    }
}


main()
console.log('hello')
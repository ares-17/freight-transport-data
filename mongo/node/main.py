from pymongo import MongoClient
from init import execute
import asyncio

url = 'mongodb://mongo:27017/'

async def check_is_empty():
    client = MongoClient(url)
    try:
        result = client['mydb'].list_collection_names()
        print(result)
        return not result
    except Exception as err:
        print('Error:', err)


async def run_on_mongo(callback):
    client = MongoClient(url)
    try:
        await callback(client)
    except Exception as err:
        print('Error:', err)


async def main():
    is_empty = await check_is_empty()
    if is_empty:
        print('database is empty!')
        await run_on_mongo(lambda client: execute(client))
    else:
        print('database is not empty!, exiting...')


if __name__ == "__main__":  
    asyncio.run(main())
    print('end...')
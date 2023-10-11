import pymongo
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME

def ensure_database_and_collection(client, db_name, collection_name):
    # Si la base de données n'existe pas, elle sera automatiquement créée lors de la création de la collection
    db = client[db_name]

    # Si la collection n'existe pas, elle sera créée
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

def store_data_base(json_data):
    # Retrieve MongoDB connection details from environment variables
    print(f"MONGODB_URI: {MONGODB_URI}")
    print(f"DATABASE_NAME: {DATABASE_NAME}")
    print(f"COLLECTION_NAME: {COLLECTION_NAME}")


    # Establish a connection to the MongoDB
    client = pymongo.MongoClient(MONGODB_URI)

    # Ensure the database and collection exist
    ensure_database_and_collection(client, DATABASE_NAME, COLLECTION_NAME)

    # Select the collection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Insert the JSON data
    result = collection.insert_one(json_data)

    # Close the connection
    client.close()

    return result.inserted_id



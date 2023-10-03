from flask import Flask, render_template, request, jsonify
import http.client
import urllib.parse
import json
import pymongo
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def send_post_request(message, idSender, idReceiver):
    conn = http.client.HTTPSConnection("app-7b3a3c98-565a-4b75-9e80-683f4e59b229.cleverapps.io", port=443)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = urllib.parse.urlencode(
        {"msg": message, "idSender": idSender, "idReceiver": idReceiver}
    )
    conn.request("POST", "/server", body=payload, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print("Received response:", data.decode("utf-8"))
    conn.close()

def ensure_database_and_collection(client, db_name, collection_name):
    # Si la base de données n'existe pas, elle sera automatiquement créée lors de la création de la collection
    db = client[db_name]

    # Si la collection n'existe pas, elle sera créée
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)


def store_data_base(json_data):
    # Retrieve MongoDB connection details from environment variables
    MONGODB_URI = os.environ.get("MONGODB_URI")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

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
    collection.insert_one(json_data)

    # Close the connection
    client.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        idSender = request.form.get("expediteur")
        idReceiver = request.form.get("destinataire")
        json_data = {"idSender": idSender, "idReceiver": idReceiver, "message": message}
        print(json_data)

        # Send the POST request to the NestJS app
        send_post_request(message, idSender, idReceiver)

        store_data_base(json_data)

        # return jsonify(json_data)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(port=5000)

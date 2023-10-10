from flask import Flask, render_template, request, jsonify
import http.client
import urllib.parse
import json
import pymongo
import os

app = Flask(__name__)

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

        # return jsonify(json_data)

    return render_template("form.html")

@app.route("/messages", methods=["POST"])
def store_message():
    json_data = request.json
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    return jsonify({"message": "Data stored successfully"}), 201

if __name__ == "__main__":
    app.run(port=5000)

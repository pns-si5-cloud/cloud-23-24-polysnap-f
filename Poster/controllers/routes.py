from flask import Blueprint, render_template, request, jsonify
from services.database_service import store_data_base
from services.post_service import send_post_request

routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        idSender = request.form.get("expediteur")
        idReceiver = request.form.get("destinataire")
        json_data = {"idSender": idSender, "idReceiver": idReceiver, "message": message}
        print(json_data)

        # Send the POST request to the NestJS app
        send_post_request(message, idSender, idReceiver)

        id_collection = store_data_base(json_data)

        # return jsonify(json_data)

    return render_template("form.html")

@routes.route("/messages", methods=["POST"])
def store_message():
    json_data = request.json
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400

    store_data_base(json_data)
    return jsonify({"message": "Data stored successfully"}), 201
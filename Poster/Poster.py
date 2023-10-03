from flask import Flask, render_template, request, jsonify
import http.client
import urllib.parse
import json

app = Flask(__name__)


def send_post_request(message, idSender, idReceiver):
    conn = http.client.HTTPConnection("localhost", 3000)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = urllib.parse.urlencode(
        {"msg": message, "idSender": idSender, "idReceiver": idReceiver}
    )
    conn.request("POST", "/server", body=payload, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print("Received response:", data.decode("utf-8"))
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        idSender = "123"
        idReceiver = "456"
        json_data = {"idSender": idSender, "idReceiver": idReceiver, "message": message}
        print(json_data)

        # Send the POST request to the NestJS app
        send_post_request(message, idSender, idReceiver)

        return jsonify(json_data)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(port=5000)

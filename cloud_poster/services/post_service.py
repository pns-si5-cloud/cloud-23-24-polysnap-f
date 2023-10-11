import http.client
import urllib.parse

def send_post_request(message, idSender, idReceiver):
    conn = http.client.HTTPSConnection("app-7b3a3c98-565a-4b75-9e80-683f4e59b229.cleverapps.io", port=443)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = urllib.parse.urlencode({
        "msg": message, 
        "idSender": idSender, 
        "idReceiver": idReceiver
    })
    conn.request("POST", "/server", body=payload, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print("Received response:", data.decode("utf-8"))
    conn.close()

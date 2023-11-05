import aiohttp
import urllib.parse

async def send_post_request(message, idSender, idReceiver):
    url = "https://app-7b3a3c98-565a-4b75-9e80-683f4e59b229.cleverapps.io/server"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    payload = urllib.parse.urlencode({
        "msg": message, 
        "idSender": idSender, 
        "idReceiver": idReceiver
    })
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            print("Received response:", await response.text())

import aiohttp

from config import CLOUD_GENERATOR_URL

#async def send_post_request(conversation_id,message):
async def send_post_request(message):
    url = CLOUD_GENERATOR_URL + "/server/message"
    headers = {
        "Content-Type": "application/json"
    }

    message['_id'] = str(message['_id'])
    message['conversation_id'] = str(message['conversation_id'])
    #payload = {
        #"conversation_id": conversation_id,
        #**message
    #}


    async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=message) as response:
                print("Status:", response.status)
                print("Content:", await response.text())
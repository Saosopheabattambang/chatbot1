import os, sys
from flask import Flask, request

from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN="EAAkBdRfasssBAJXMS6kIG0Wfmif7lZAXQJfDFwhOTsidOXZBm0jVCZAm2PMxkMXLipmll3BmqUZCcVI75NyTjixdIIXIcSLjxEsLQvs8FOsaSOz6tJTST0JoPAJ7uNxUchZCaklwz7pDAwjlyYbY4L1cCRlF9sH92dVOZCiZBcbQwZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods =['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismation",403
        return request.args["hub.challenge"],200
    return "Hello sophea",200

@app.route('/',methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                recipient_id= messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text='no text'

                    response=messaging_text
                    bot.send_text_message(sender_id,response)

    return "ok",200


def log(message):
    print(message)
    sys.stdout.flush()
if  __name__=="__main__":
    app.run(debug= True, port = 80)
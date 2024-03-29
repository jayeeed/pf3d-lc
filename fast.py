import requests
import os, signal
from flask import Flask, request
from openai import OpenAI
from dotenv import load_dotenv
# import logging, ngrok

load_dotenv()

# logging.basicConfig(level=logging.INFO)
# listener = ngrok.forward("localhost:5000", authtoken_from_env=True)

app = Flask(__name__)

# tokens
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
access_token = os.environ.get("FACEBOOK_ACCESS_TOKEN")
verify_token = os.environ.get("VERIFY_TOKEN")

API = "https://graph.facebook.com/v19.0/me/messages?access_token=" + access_token

@app.route('/webhook', methods=['GET'])
def verify():
    # Verify the webhook subscription with Facebook Messenger
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == verify_token:
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/webhook", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    try:
        if data['entry'][0]['messaging'][0]['sender']['id']:
            message = data['entry'][0]['messaging'][0]['message']
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']
            chat_gpt_input=message['text']
            print("User=>", chat_gpt_input)

            chat_completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": chat_gpt_input}],
                            max_tokens=100)          
            chatbot_res = chat_completion.choices[0].message.content

            print("Response=>", chatbot_res)
            response = {
                'recipient': {'id': sender_id},
                'message': {'text': chatbot_res}
            }
            requests.post(API, json=response)
    except Exception as e:
        print(e)
        pass
    return '200 OK HTTPS.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

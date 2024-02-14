import requests
import os, signal
from flask import Flask, request
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# tokens
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
access_token = os.environ.get("FACEBOOK_ACCESS_TOKEN")
verify_token = os.environ.get("VERIFY_TOKEN")

API = "https://graph.facebook.com/v19.0/me/messages?access_token=" + access_token

# Read business_info from the text file
with open("Bangobandu.txt", "r") as file:
    business_info = file.read()

def chatbot(user_query, client, business_info):
    llm = OpenAI(temperature=0.7, openai_api_key=client)

    # Define fixed examples
    examples = [
        {"input": "What's your company name?",
        "output": business_info
        },
    ]

    # Create a few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "Reply within 20 words and be very precise:\n {input}"),
            ("ai","{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    # Create the main prompt template
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are interacting with a business information chatbot."),
            few_shot_prompt,
            ("human", user_query),
        ]
    )

    # Create the chain with the prompt template
    faq_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="response")

    # Invoke the chain with user input
    response = faq_chain.invoke({'user_query': user_query})

    return response

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

            chatbot_res = chatbot(chat_gpt_input, os.environ.get("OPENAI_API_KEY"), business_info)

            chatbot_res = chatbot_res['response']
            
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

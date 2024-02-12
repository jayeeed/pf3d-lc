import json
from flask import Flask, request, jsonify
import requests
import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def chatbot(user_query, openai_api_key, business_info):
    llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)

    # Define fixed examples
    examples = [
        {"input": "Tell me about your business.",
        "output": business_info
        },
    ]

    # Create a few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
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

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook verification challenge
        if request.args.get('hub.verify_token') == 'mytoken':
            return request.args.get('hub.challenge')
        return 'Invalid verification token'

    elif request.method == 'POST':
        # Handle incoming messages
        data = request.json
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):  # If there is a message from user
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']

                    # Process the user's message using your chatbot function
                    response_text = chatbot(message_text)

                    # Send the response back to the user
                    send_message(sender_id, response_text)

        return 'OK'


def send_message(recipient_id, message_text):
    params = {
        "access_token":'EAA1LsR3ZAS6wBOZBZBcnCIy3rjTBFRRhuFJxotle043UqBbw4EuQnYTwMNlndrxpmaUSNZApemS1LUzgXBsVmZCrRGQPRZBKoL88lY01N8EJcEJGZC8ediS20ppRDxT8KyQZAiSVLLN7EP1xo4ZCyKBBNPlCeGP6LyVCF6GbcBppuzKa3m4nZAqZBVl7v6q6oWjglmvDjwA7PN917IHjBKhRHCMcElZC0ZCfsXhZCBFp6ru3oZD'
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    response = requests.post("https://graph.facebook.com/v19.0/me/messages", params=params, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    app.run(debug=True)

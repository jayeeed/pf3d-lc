from flask import Flask, request, jsonify
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import requests

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

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Facebook verification challenge
        verify_token = request.args.get("hub.verify_token")
        if verify_token == os.getenv("VERIFY_TOKEN"):
            return request.args.get("hub.challenge")
        else:
            return "Invalid verification token"
    elif request.method == "POST":
        data = request.json

        # Check if message contains text
        if "entry" in data and "messaging" in data["entry"][0]:
            message_text = data["entry"][0]["messaging"][0].get("message", {}).get("text")
            if message_text:
                # Call Facebook API to get latest message and conversation IDs
                api_url = "https://graph.facebook.com/v19.0/me/conversations"
                params = {
                    "fields": "created_time,messages",
                    "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN")
                }
                response = requests.get(api_url, params=params)
                data = response.json()

                # Extract latest message ID and conversation ID
                latest_conversation = data["data"][0]
                latest_message = latest_conversation["messages"]["data"][0]
                message_id = latest_message["id"]
                conversation_id = latest_conversation["id"]

                # Call Facebook API to get participant IDs
                conversation_url = f"https://graph.facebook.com/v19.0/{conversation_id}"
                params = {
                    "fields": "id,name,participants",
                    "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN")
                }
                response = requests.get(conversation_url, params=params)
                conversation_data = response.json()

                # Extract ps_id from participants
                ps_id = conversation_data["participants"]["data"][0]["id"]

                # Call Facebook API to get message text
                message_url = f"https://graph.facebook.com/v19.0/{message_id}"
                params = {
                    "fields": "message",
                    "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN")
                }
                response = requests.get(message_url, params=params)
                message_data = response.json()
                message_text = message_data.get("message")

                user_query = message_text
                api_key = os.getenv("OPENAI_API_KEY")

                # Read business_info from the text file
                with open("business_info.txt", "r") as file:
                    business_info = file.read()

                if user_query:
                    bot_response = chatbot(user_query, api_key, business_info)

                    if "response" in bot_response:
                        # Post chatbot response to Facebook API
                        post_url = "https://graph.facebook.com/v19.0/me/messages"
                        headers = {
                            "Content-Type": "application/json"
                        }
                        data = {
                            "recipient": {"id": ps_id},
                            "message": {"text": bot_response["response"]},
                            "messaging_type": "RESPONSE"
                        }
                        response = requests.post(post_url, json=data, headers=headers)
                        if response.status_code == 200:
                            return jsonify({"response": bot_response["response"], "message_id": message_id, "conversation_id": conversation_id, "ps_id": ps_id, "message_text": message_text})
                        else:
                            return jsonify({"error": "Failed to send response to Facebook."})
                    else:
                        return jsonify({"error": "Invalid response format."})
                else:
                    return jsonify({"error": "No user query provided."})

        # If message does not contain text, return success response
        return "OK"

if __name__ == "__main__":
    app.run(debug=True)

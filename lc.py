import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()

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
            ("{output}"),
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

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")

    # Read business_info from the text file
    with open("business_info.txt", "r") as file:
        business_info = file.read()

    # Get user input for the question
    user_query = st.text_input("Ask a question:")

    if user_query:
        bot_response = chatbot(user_query, api_key, business_info)

        if "response" in bot_response:
            st.write("Chatbot Response:")
            st.write(bot_response["response"])
        else:
            st.text("Invalid response format.")

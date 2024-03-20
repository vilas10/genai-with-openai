# GenAI demo with OpenAI integration
import streamlit as st
import tempfile
import openai
import pandas as pd
import requests
import datetime
import pprint
import tiktoken
from pypdf import PdfReader
import os
from matplotlib import pyplot, image

client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_email(review, chat_transcript, postfix):
    with st.spinner("Generating email response..."):
        # output_email = generate_email(review, chat_transcript, postfix)
        
        
        chat_history = chat_transcript.copy()
        chat_history.append({"role": "user", "content": review + postfix})

        reply = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=chat_history
        )

        return reply.choices[0].message.content
    


def app():
    st.header("GenAI Demo")
    st.subheader("Built using OpenAI APIs")
    st.write("Reply to customer feedback!")

    chat_transcript = [{"role": "system", "content": "You are a polite customer support representative"}]
    postfix = "\n\nWrite an email to customers to address the issues put forward in the above review, thank them if they write good comments, and encourage them to make further purchases. Do not give promotion codes or discounts to the customers. Do not recommend other products. Keep the emails short."

    with st.form("my_form"):
        review = st.text_area('Customer Review', 'Please provide customer review')

        is_submitted = st.form_submit_button(label="Submit")

    if is_submitted:
        output_email = generate_email(review, chat_transcript, postfix)
        st.write(output_email)
        

if __name__ == "__main__":
    app()
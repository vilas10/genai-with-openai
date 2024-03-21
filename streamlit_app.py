# GenAI demo with OpenAI integration
import streamlit as st
import openai
import os

GPT_MODEL = "gpt-3.5-turbo-1106"
openai_client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def get_model_response(review, chat_transcript, postfix):
        chat_transcript.append({"role": "user", "content": review + postfix})

        reply = openai_client.chat.completions.create(
            model=GPT_MODEL,
            messages=chat_transcript
        )

        return reply.choices[0].message.content


def generate_email_response_to_customer_review():
    st.subheader("Reply to customer review!")

    chat_transcript = [{"role": "system", "content": "You are a polite customer support representative"}]
    postfix = "\n\nWrite an email to customers to address the issues put forward in the above review, thank them if they write good comments, and encourage them to make further purchases. Do not give promotion codes or discounts to the customers. Do not recommend other products. Keep the emails short."

    with st.form("my_form"):
        review = st.text_area('Customer Review', 'Please provide customer review')

        is_submitted = st.form_submit_button(label="Submit")

    if is_submitted:
        with st.spinner("Generating email response..."):
            try:
                output_email = get_model_response(review, chat_transcript, postfix)
                st.write(output_email)
            except:
                st.warning("Thanks for your interest in GenAI Demo. The demo period has ended.")

def app():
    st.header("GenAI Demo (Using OpenAI APIs)")
    # Generate email response to customer review.
    generate_email_response_to_customer_review()


if __name__ == "__main__":
    app()

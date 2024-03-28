# GenAI demo with OpenAI integration
import streamlit as st
import openai

GPT_MODEL = "gpt-3.5-turbo-0125"
DALLE_MODEL = "dall-e-3"

# Get an OpenAI API Key before continuing
if "openai_api_key" in st.secrets:
    openai_api_key = st.secrets.openai_api_key
else:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    st.stop()

openai_client = openai.OpenAI(api_key=openai_api_key)

def get_model_response(
        content, 
        chat_transcript, 
        postfix
        ):
    chat_transcript.append({"role": "user", "content": content + postfix})

    reply = openai_client.chat.completions.create(
        model=GPT_MODEL,
        messages=chat_transcript
    )

    return reply.choices[0].message.content


def generate_response_to_customer_review(
        postfix, 
        id="review"
        ):
    print('generating email response')
    chat_transcript = [{"role": "system", "content": "You are a polite customer support representative"}]

    with st.form(id + "_form"):
        review = st.text_area('Please provide customer review below', '')

        is_submitted = st.form_submit_button(label="Submit")

    output_email = ""
    if is_submitted:
        with st.spinner("Generating email response..."):
            try:
                output_email = get_model_response(review, chat_transcript, postfix)
                st.write(output_email)
            except:
                st.warning("Thanks for your interest in GenAI Demo. The demo period has ended.")
    
    return output_email


def generate_image_based_on_prompt(
        image_text="",
        postfix="",
        id="image",
        size="1024x1024",
        quality="standard",
        n = 1
    ):
    print("generating image", id, image_text)
    prompt = ""
    if not image_text:
        if "visibility" not in st.session_state:
            st.session_state.visibility = "visible"
            st.session_state.disabled = False
            st.session_state.horizontal = False

        col1, col2 = st.columns(2)

        with col1:
            quality = st.radio(
                "Quality",
                ["standard", "hd"],
                key=id+"_quality",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                horizontal=st.session_state.horizontal,
            )

        with col2:
            size = st.radio(
                "Size",
                ["1024x1024", "1024x1792", "1792x1024"],
                key=id+"_size",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                horizontal=st.session_state.horizontal,
            )

        with st.form(id + "_form"):
            prompt = st.text_area('Please provide prompt to generate image', "")
            is_submitted = st.form_submit_button(label="Submit")

    if image_text or is_submitted:
         with st.spinner("Generating image..."):
            try:
                response = openai_client.images.generate(
                    model=DALLE_MODEL, 
                    prompt=prompt if prompt else image_text + "\n\n" + postfix, 
                    size=size,
                    quality=quality,
                    n=n
                )
                
                # The prompt is revised for generating the image
                revised_prompt = response.data[0].revised_prompt
                st.write(revised_prompt)

                image_url = response.data[0].url
                st.image(image_url)
            except Exception as e:
                print(e)
                st.warning("Thanks for your interest in GenAI Demo. The demo period has ended.")

def respond_to_customer_review_with_note_on_image():
    print("generating thank you note")
    postfix = "\n\nWrite an note to address the issues put forward in the above review, thank them if they write good comments, and encourage them to make further purchases. Do not give promotion codes or discounts to the customers. Do not recommend other products. Keep the note short. This should fit on greeting card. Limit to 30 words"
    note_text = generate_response_to_customer_review(postfix, "review_note")
    if note_text:
        generate_image_based_on_prompt(note_text, postfix="Add the above text on the generated image", id="image_note")

def app():
    st.header("GenAI Demo (Using OpenAI APIs)")

    review_tab, image_tab, note_tab = st.tabs(["Review", "Image", "Note"])

    # Generate email response to customer review.
    with review_tab:
        st.subheader("Reply to customer review!")
        postfix = "\n\nWrite an email to customers to address the issues put forward in the above review, thank them if they write good comments, and encourage them to make further purchases. Do not give promotion codes or discounts to the customers. Do not recommend other products. Keep the emails short. If you get a bad comment, try to reach out to use for any questions. If you receive review in other languages, respond in that language."
        st.write(postfix)
        generate_response_to_customer_review(postfix)

    with image_tab:
        st.subheader("Generate image!")
        # Generate image using dalle model
        generate_image_based_on_prompt()
    
    with note_tab:
        st.subheader("Write a response note to customer!")
        # Lets chain the above.
        respond_to_customer_review_with_note_on_image()

if __name__ == "__main__":
    app()

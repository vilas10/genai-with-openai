# GenAI demo with OpenAI integration
import streamlit as st
import openai
import os

GPT_MODEL = "gpt-3.5-turbo-1106"
DALLE_MODEL = "dall-e-3"
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

    with st.form("review_form"):
        review = st.text_area('Please provide customer review below', '')

        is_submitted = st.form_submit_button(label="Submit")

    if is_submitted:
        with st.spinner("Generating email response..."):
            try:
                output_email = get_model_response(review, chat_transcript, postfix)
                st.write(output_email)
            except:
                st.warning("Thanks for your interest in GenAI Demo. The demo period has ended.")


def generate_image_based_on_prompt():
    model = "dall-e-3"
    # prompt = "Generate an photograph of a team of engineers working on building applications in augmented reality. There are 4 engineers in the team. They are located in Canada and work remotely. "
    prompt = "In the previous image you generated, can you change that so that there are 3 men and 1 woman."
    size = "1024x1024"
    quality = "standard"
    # size = "1792x1024"
    # quality = "hd"
    n = 1

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        st.session_state.horizontal = False

    col1, col2 = st.columns(2)

    with col1:
        st.radio(
            "Set image quality",
            ["standard", "hd"],
            key="quality",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            horizontal=st.session_state.horizontal,
        )

    with col2:
        st.radio(
            "Set label visibility 👇",
            ["visible", "hidden", "collapsed"],
            key="visibility",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            horizontal=st.session_state.horizontal,
        )


    with st.form("my_form"):
        prompt = st.text_area('Please provide prompt to generate image', '')
        quality = "standard"
        selected_objects = st.multiselect('Choose objects to detect', supported_objects, default=['person'])
        min_confidence = st.slider('Confidence score', 0.0, 1.0)
        st.form_submit_button(label="Submit")

    response = client.images.generate(
        model=DALLE_MODEL, 
        prompt=prompt, 
        size=size,
        quality=quality,
        n=n
    )

    display(Markdown(response.data[0].revised_prompt))

    image_url = response.data[0].url
    path = 'dall-e-3/images'
    os.makedirs(path, exist_ok=True)
    name = path + '/' + str(datetime.datetime.now())

    image_data = requests.get(image_url).content

    with open(name+'.jpg', 'wb') as handler:
            handler.write(image_data)

    pyplot.figure(figsize=(11,9))
    img = image.imread(name+'.jpg')

    imgplot = pyplot.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    pyplot.show()



def app():
    st.header("GenAI Demo (Using OpenAI APIs)")
    # Generate email response to customer review.
    generate_email_response_to_customer_review()


if __name__ == "__main__":
    app()

from langchain.llms import GooglePalm 
import streamlit as st
import time


def load_model_GooglePalm():
    try:
        api_key = "AIzaSyDc9dLSWX0jerFioIn3OoYPaXpxi0qsNKY"
        llm_model = GooglePalm(google_api_key=api_key, temperature=0.9)
        return llm_model
    except NotImplementedError as e:
        raise e
    

def generate_answear(llm_model, question): 
    poem = llm_model(question)
    return poem

def stream_data(answear):
    for word in answear.split(" "):
        yield word + " "
        time.sleep(0.02)

st.title("NutriMate Chat")

client = load_model_GooglePalm()

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hai welcome to NutriMate Chat, what can i do for you ? 😊"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream =  generate_answear(client,  prompt)
        response = st.write_stream(stream_data(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})
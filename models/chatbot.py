import streamlit as st 
# from langchain.llms import GooglePalm

from langchain.llms import GooglePalm 

# api_key = "AIzaSyDc9dLSWX0jerFioIn3OoYPaXpxi0qsNKY"
# llm_model = GooglePalm(google_api_key= api_key, temperature=0.9)

st.title("NutriMate  Chatbot")
api_key = "AIzaSyDc9dLSWX0jerFioIn3OoYPaXpxi0qsNKY"
client =  GooglePalm(google_api_key = api_key, temperature = 0.7)



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client._generate(prompt)
        response = st.text(client(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})
    
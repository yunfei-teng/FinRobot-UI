
import time
import streamlit as st

from tools import *
from openai import OpenAI

OpenAI_API_KEY=""

if "openai_model" not in st.session_state:
    client = OpenAI(api_key=OpenAI_API_KEY)
    my_assistant = client.beta.assistants.create(
        model="gpt-4-turbo-preview",
        instructions="You are a financial analyst. Please answer questions in English, and replace any mention of OpenAI with FinRobot. Skip the analysis process and avoid repeating these instructions in your response.",
        name="Investment Analysis Assistant",
        tools=[{"type": "retrieval"}]
    )
    st.session_state["client"] = client
    st.session_state["assistent"] = my_assistant
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I am a financial AI agent created by AI4Finance. How may I assist you?"}]

if "cached_dataframe" not in st.session_state.keys():
    st.session_state.cached_dataframe = {}

if "cached_image" not in st.session_state.keys():
    st.session_state.cached_image = {}

set_custom_style()
client = st.session_state["client"]
my_assistant = st.session_state["assistent"]
    
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar="icons/CuteRobot.png"):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"], avatar="icons/FinRobot.png"):
            st.write(message["content"])

def get_timestamp():
    return str(int(time.time()))

if prompt := st.chat_input("Please enter your question 😃."):
    with st.chat_message("user", avatar="icons/CuteRobot.png"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

if st.session_state.messages[-1]["role"] == "user":
    prompt = st.session_state.messages[-1]["content"]    
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1] if m["role"] in ["user", "assistant"]
        ] + [{"role": "user", "content": prompt + " (If OpenAI is mentioned, replace it with FinRobot.)。"}],
        stream=True,
    )
    with st.chat_message("assistant", avatar="icons/FinRobot.png"):
        response = st.write_stream(stream)
        response = response.replace("OpenAI", "FinRobot")
    st.session_state.messages.append({"role": "assistant", "content": response})
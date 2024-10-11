import streamlit as st
from core import SuperAgent 

# Page configuration
st.set_page_config(page_title="DataMirror", page_icon="🔍")  

# SuperAgent initialization
super_agent = SuperAgent()

# Sidebar
with st.sidebar:
    reset_button_key = "reset_button"
    reset_button = st.button("Reset Session", key=reset_button_key)
    if reset_button:
        st.session_state.conversation = None
        st.session_state.chat_history = None

    st.image('assets/img/logo.jpg', width=200)
    st.caption("🔍 **Welcome to DataMirror, your digital mirror!**\n\n DataMirror helps you discover, in just a few clicks, the information available about you online. Using our AI-powered solution, we gather only publicly accessible data while strictly adhering to privacy and confidentiality laws. Take control of your digital footprint and see what others can find out about you!")

# Initializes session state to keep message history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I’m DataMirror, your personal digital assistant. I’m here to help you uncover publicly accessible information about you on the internet. Together, we’ll explore your digital footprint while respecting privacy laws. \n\nHow can I assist you today? To get started, simply enter your name or ask me a question!"}]

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input management
if prompt := st.chat_input("Enter your query here:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try :
        # Display a spinner while the SuperAgent processes the request
        with st.spinner('Analysis of ongoing search results...'):
            response = super_agent.handle_query(prompt)

        # Retrieve and display response
        msg = response.get('final_result', "Sorry, I can't answer that right now. Please come back later.")
        st.session_state.messages.append({"role": "assistant", "content": msg})
    except Exception as error:
        print(f"An error has occurred. Error : {error}")
        st.session_state.messages.append({"role" : "assistant", "content" : "Sorry, I can't answer that right now. Please come back later."})

    with st.spinner('Displaying results...'):
        st.chat_message("assistant").write(msg)
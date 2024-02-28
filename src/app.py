# pip install streamlit langchain lanchain-openai beautifulsoup4 python-dotenv chromadb

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

# app config
st.set_page_config(page_title="Chat with websites", page_icon="🤖")
st.title("Chat with websites")

template = """
You are a helpful assistant. Answer the following questions considering the history of the conversation:

Chat history: {chat_history}

User question: {user_question}
"""

prompt = ChatPromptTemplate.from_template(template)

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

    
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        llm = ChatOpenAI()
        
        chain = prompt | llm | StrOutputParser()
        stream = chain.stream({
            "chat_history": st.session_state.chat_history,
            "user_question": user_query,
        })
        response = st.write_stream(stream)

    st.session_state.chat_history.append(AIMessage(content=response))

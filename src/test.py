# pip install streamlit langchain langchain-openai
# URL: https://youtu.be/bupx08ZgSFg?si=XgzJ9e1f313c2U84&t=2276

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader


def get_response(user_input):
    return "I don't know"

def get_vectorstore_from_url(url):
    """
    Retrieves a vector store from the given URL.

    Args:
        url (str): The URL of the vector store.

    Returns:
        documents: The retrieved vector store.

    """
    return WebBaseLoader(url).load()


# app config
st.set_page_config(page_title="Chat with websites", page_icon="🤖")
st.title("Chat with websites") 

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

# sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

if website_url is None or website_url == "":
    st.info("Please enter a website URL")

else:
    documents = get_vectorstore_from_url(website_url)
    with st.sidebar:
        st.write(documents)

    # user input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(
            HumanMessage(
                content=user_query
            )
        )
        st.session_state.chat_history.append(
            AIMessage(
                content=response
            )
        )
        with st.chat_message("Human"):
            st.write(user_query)

        with st.chat_message("AI"):
            st.write(response)

# for debug only
# with st.sidebar:
#     st.write(st.session_state.chat_history)

# conversation
# for message in st.session_state.chat_history:
#     if isinstance(message, AIMessage):
#         with st.chat_message("AI"):
#             st.write(message.content)
#     elif isinstance(message, HumanMessage):
#         with st.chat_message("Human"):
#             st.write(message.content)
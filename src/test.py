# pip install streamlit langchain langchain-openai
# URL: https://youtu.be/bupx08ZgSFg?si=XgzJ9e1f313c2U84&t=2276

import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from dotenv import load_dotenv


load_dotenv()



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

    # get the text indocument form
    loader = WebBaseLoader(url)
    document = loader.load()

    # split the document into chunk's
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)
    return document_chunks


def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()

    retriver = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages(
        MessagesPlaceholder(variable_name="chat_history"),
        ("User", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    )

    retriver_chain = create_history_aware_retriever(
        llm,
        retriver,
        prompt
    )

    return retriver_chain


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
    vector_store = get_vectorstore_from_url(website_url)

    retriver_chain = get_context_retriever_chain(vector_store)

    with st.sidebar:
        st.write(document_chunks)

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

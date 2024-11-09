from llama_index.llms.together import TogetherLLM
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from IPython.display import Markdown, display
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
import os 
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from llama_index.readers.web import SimpleWebPageReader
from helpers.clean_data import clean_text
from langchain_community.document_loaders import WebBaseLoader
from llama_index.embeddings.together import TogetherEmbedding





def get_documents(url_link):
    # documents=SimpleWebPageReader(html_to_text=True).load_data([url_link])
    loader=WebBaseLoader([url_link])
    data=loader.load().pop().page_content
    data=clean_text(data)
    return data

def get_vector_Store(documents):
    embed_model = TogetherEmbedding(
        model_name=os.getenv('TOGETHERAI_EMBEDDING_MODEL_NAME'),
        api_key=os.getenv('TOGETHER_API_KEY')
    )
    db=chromadb.PersistentClient(path='./data/chroma_db/')
    chromadb_collection=db.get_or_create_collection('url')
    vectorstore=ChromaVectorStore(chroma_collection=chromadb_collection)
    storage_context=StorageContext.from_defaults(vector_store=vectorstore)
    index=VectorStoreIndex.from_documents(documents,storage_context=storage_context,embed_model=embed_model)
    return index


if __name__ == '__main__':
    
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    load_dotenv()

    st.set_page_config(page_title="🦙:Right-Guide", page_icon="🤖")
    st.markdown("<center><h1 style='color: white;'>🦙LLama-Law</h1></center>", unsafe_allow_html=True)
    USER_AVATAR = "👤"
    BOT_AVATAR = "🤖"


    user_question = st.text_input("Ask me anything about the URL:")

    # if user_question:
    #     handle_userinput(user_question)

    with st.sidebar:
        st.subheader('URL')
        url_link = st.text_input("The URL link")
        if url_link:

            if st.button('Process'):
                with st.spinner('Processing'):
                    documents = get_documents(url_link)
                    documents = clean_text(documents)
                    print(documents)
                    vectorstore=get_vector_Store(documents)


    
           
 
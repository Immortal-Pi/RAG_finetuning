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
from llama_index.readers.web import SimpleWebPageReader
from langchain.text_splitter import CharacterTextSplitter
from llama_index.readers.web import SpiderWebReader
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.prompts import ChatPromptTemplate
from llama_index.core.memory import ChatMemoryBuffer
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from llama_index.core.memory import  ChatMemoryBuffer
from llama_index.core.memory import ChatMemoryBuffer
from helpers.prompt import text_qa_template,refine_template







def get_documents(url_link):
    documents=SimpleWebPageReader(html_to_text=True).load_data([url_link])
    print(documents)
    return documents

def get_vector_Store_index(documents):
    embed_model = TogetherEmbedding(
        model_name=os.getenv('TOGETHERAI_EMBEDDING_MODEL_NAME'),
        api_key=os.getenv('TOGETHER_API_KEY')
    )


    db=chromadb.PersistentClient(path='./data/chroma_db/')
    # if "url" in [c.name for c in db.list_collections()]:


    # db.reset()
    db.delete_collection('url')
    chromadb_collection=db.create_collection('url')
    vectorstore=ChromaVectorStore(chroma_collection=chromadb_collection)
    storage_context=StorageContext.from_defaults(vector_store=vectorstore)
    index=VectorStoreIndex.from_documents(documents,storage_context=storage_context,embed_model=embed_model)

    return index

def get_chat_engine():
    embed_model = TogetherEmbedding(
        model_name=os.getenv('TOGETHERAI_EMBEDDING_MODEL_NAME'),
        api_key=os.getenv('TOGETHER_API_KEY')
    )
    db = chromadb.PersistentClient(path='./data/chroma_db/')
    chroma_collection = db.get_collection('url')
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )
    memory = ChatMemoryBuffer.from_defaults(token_limit=1000)
    chat_engine = index.as_chat_engine(
        chat_mode='context',
        memory=memory,
        system_prompt=(text_qa_template),
    )
    return chat_engine


# def handle_userinput(user_question,index):
#
#
#     response=chat_engine.chat(user_question)
#     st.write(response.response)


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



    # index=get_vector_Store_index()




    st.subheader('URL')
    url_link = st.text_input("The URL link")
    button=st.button('Process')
    if button:
        with st.spinner('Processing'):
            documents = get_documents(url_link)
            index=get_vector_Store_index(documents)

    user_question = st.text_input("Ask me anything about the URL:")
    chat_engine = get_chat_engine()
    if user_question:
        response=chat_engine.chat(user_question)
        st.write(response.response)

    
           
 
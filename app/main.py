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
from llama_index.core import SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from helpers.prompt import text_qa_template,refine_template
import subprocess
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
# from openai import OpenAI,Op





def get_documents(url_link):
    # documents=SimpleWebPageReader(html_to_text=True).load_data([url_link])
    subprocess.run(["python", "craw4ai.py", url_link])
    # try:
    #     with open("crawled_data.txt", "r", encoding="utf-8") as file:
    #         documents = file.read()
    #         # print('test', documents)
    # except FileNotFoundError:
    #     documents = None
    #     print(FileNotFoundError)
    # # print(documents)
    documents=SimpleDirectoryReader('data').load_data()
    print(documents)
    return documents

def get_vector_Store_index(documents):
    # embed_model = TogetherEmbedding(
    #     model_name=os.getenv('TOGETHERAI_EMBEDDING_MODEL_NAME'),
    #     api_key=os.getenv('TOGETHER_API_KEY')
    # )
    # embed_model=
    # embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    embed_model=AzureOpenAIEmbedding(
        model='text-embedding-ada-002',
        deployment_name=os.getenv('AZURE_OPENAI_EMBEDDING_MODEL_NAME'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
        api_version=os.getenv('AZURE_OpenAI_API_VERSION')
    )

    db=chromadb.PersistentClient(path='./app/data/chroma_db/')
    if "url" in [c.name for c in db.list_collections()]:
        db.delete_collection('url')

    # db.reset()

    chromadb_collection=db.create_collection('url')
    vectorstore=ChromaVectorStore(chroma_collection=chromadb_collection)
    storage_context=StorageContext.from_defaults(vector_store=vectorstore)
    index=VectorStoreIndex.from_documents(documents,storage_context=storage_context,embed_model=embed_model)

    return index

def get_chat_engine(language):
    # embed_model = TogetherEmbedding(
    #     model_name=os.getenv('TOGETHERAI_EMBEDDING_MODEL_NAME'),
    #     api_key=os.getenv('TOGETHER_API_KEY')
    # )
    embed_model=AzureOpenAIEmbedding(
        model='text-embedding-ada-002',
        deployment_name=os.getenv('AZURE_OPENAI_EMBEDDING_MODEL_NAME'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
        api_version=os.getenv('AZURE_OpenAI_API_VERSION')
    )
    db = chromadb.PersistentClient(path='./app/data/chroma_db/')
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
        system_prompt=(text_qa_template.format(
            language=language,
            context="The client is an immigrant or a tourist from other state and doesnt know any laws in USA"
        )),
    )
    return chat_engine


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

    st.subheader('URL')
    url_link = st.text_input("The URL link")
    button=st.button('Process')
    if button:
        with st.spinner('Processing'):
            documents = get_documents(url_link)
            index=get_vector_Store_index(documents)
            print(index)
            # chat_engine = get_chat_engine()

    language = st.selectbox(
        "select language",
        ('English','Spanish','Chinese','Tagalog(Filipino)','Vietnamese','Arabic','French','Koream','Russian','Portuguese','German','Polish','Italian','Urdu','Telugu','Japanese','Kannada', 'Hindi', 'Spanish', 'Urdu'),
        index=0
    )

    user_question = st.text_input("Ask me anything about the URL:")
    chat_engine=get_chat_engine(language)
    # print(language)
    if user_question:
        # chat_engine = get_chat_engine()
        response=chat_engine.chat(user_question)
        st.write(response.response)

    
           
 
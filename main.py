import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.vectorstores import BigQueryVectorSearch
from google.cloud import bigquery
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv


def main():
    st.title("File Reader")


    question = st.text_input("Enter your question")
    if st.button("Ask"):
        if not question:
            st.error("Please enter a question")
        else:
            answer = 'process_question(chain, embedding, store, question)'
            st.subheader("Answer:")
            st.write(answer)




if __name__ == "__main__":
    main()
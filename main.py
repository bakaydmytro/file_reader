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

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
DATASET = os.getenv('DATASET')
TABLE = os.getenv('TABLE')
REGION = os.getenv('REGION')

def setup_embedding_and_client():
    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest", project=PROJECT_ID
    )
    client = bigquery.Client(project=PROJECT_ID, location=REGION)
    client.create_dataset(dataset=DATASET, exists_ok=True)
    return embedding, client


def setup_store(embedding):
    return BigQueryVectorSearch(
        project_id=PROJECT_ID,
        dataset_name=DATASET,
        table_name=TABLE,
        location=REGION,
        embedding=embedding,
        distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
    )


def process_uploaded_file(uploaded_file):
    if uploaded_file:
        temp_file_path = f"./upload/{uploaded_file.name}"
        with open(temp_file_path, "wb") as file:
            file.write(uploaded_file.getvalue())
        return temp_file_path
    return None


def split_documents(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(data)


def main():
    st.title("File Reader")

    embedding, client = setup_embedding_and_client()
    store = setup_store(embedding)
    chat = ChatVertexAI()
    chain = load_qa_chain(chat, chain_type="stuff")

    uploaded_file = st.file_uploader("Upload file", type=["pdf"])
    file_path = process_uploaded_file(uploaded_file)

    if file_path:
        texts = split_documents(file_path)
        store.add_documents(texts)

    question = st.text_input("Enter your question")
    if st.button("Ask"):
        if not question:
            st.error("Please enter a question")
        else:
            answer = process_question(chain, embedding, store, question)
            st.subheader("Answer:")
            st.write(answer)


def process_question(chain, embedding, store, question):
    query_vector = embedding.embed_query(question)
    docs = store.similarity_search_by_vector(query_vector, k=1)
    result = chain.run(input_documents=docs, question=question)
    return result


if __name__ == "__main__":
    main()
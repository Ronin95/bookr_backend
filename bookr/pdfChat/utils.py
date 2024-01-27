import os
import json
import logging
from django.conf import settings
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.document_transformers import LongContextReorder
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

def fetch_pdf(filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'splitUpPDFs', filename)
    if os.path.exists(file_path):
        return file_path
    else:
        # Handle the case where the file doesn't exist
        raise FileNotFoundError(f"The file {filename} does not exist in the specified path.")

def get_splitUpPDF_text(selectedPDF):
    text = ""
    for pdf in selectedPDF:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def ai_answer(text_chunks, user_input):
    # Get embeddings
    embeddings = OpenAIEmbeddings()

    # texts from the rest api django backend
    texts = text_chunks

    # Create a retriever
    retriever = Chroma.from_texts(texts, embedding=embeddings).as_retriever(search_kwargs={"k":4})

    # Get last user text input
    query = user_input

    # Get relevant documents ordered by relevance score
    docs = retriever.get_relevant_documents(query)

    # reorder docs - relevant docs at the beginning
    reordering = LongContextReorder()
    reordered_docs = reordering.transform_documents(docs)

    # Override prompts
    document_prompt = PromptTemplate(
        input_variables=["page_content"], template="{page_content}"
    )
    document_variable_name = "context"
    llm = OpenAI(model="gpt-3.5-turbo-instruct") # Update the model as time goes - models become deprecated
    stuff_prompt_override = """Given this text extracts:
    -----
    {context}
    -----
    Please answer the following question and if you do not know the answer say "I do not know":
    {query}"""
    prompt = PromptTemplate(
        template=stuff_prompt_override, input_variables=["context", "query"]
    )

    # Instantiate the chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_prompt=document_prompt,
        document_variable_name=document_variable_name,
    )
    output = chain.run(input_documents=reordered_docs, query=query)
    return output
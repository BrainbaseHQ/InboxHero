import os
import pathlib
import pickle
import subprocess
import tempfile

import requests
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
# -*- coding: utf-8 -*-
from langchain.llms import OpenAI, OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor

from lib.read_emails import save_emails_to_db

def approve(type, request):
    return "Error approving."


def run(message, history):
    db = SQLDatabase.from_uri('sqlite:///emails.db')
    toolkit = SQLDatabaseToolkit(db=db)

    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0),
        toolkit=toolkit,
        verbose=True
    )
    
    res = agent_executor.run(message)

    return res


def setup(config):
    os.environ['email_address'] = config["email_address"]
    os.environ['email_password'] = config["email_password"]
    os.environ['instructions'] = config["instructions"]
    os.environ['fields'] = config["fields"]
    os.environ['OPENAI_API_KEY'] = config["OPENAI_API_KEY"]

def cron():
    save_emails_to_db()
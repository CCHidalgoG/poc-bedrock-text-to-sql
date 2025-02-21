import boto3
import psycopg2
import json
import re
import os

from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import BedrockChat
from langchain.prompts import PromptTemplate
from tabulate import tabulate
from dotenv import load_dotenv
from settings import DOMAIN_DESCRIPTIONS

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')


def get_llm():
    llm = BedrockChat(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        client=bedrock_client,  # Use the same client instance
        model_kwargs={
            "temperature": 0,
            "max_tokens": 1000
        }
    )
    return llm

# Configurar cliente AWS Bedrock
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# Function to configure the LLM with AWS Bedrock using the custom class

def invoke_bedrock_model(prompt, model_id='anthropic.claude-3-5-sonnet-20240620-v1:0'):
    response = bedrock_client.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )
    return json.loads(response['body'].read().decode('utf-8'))
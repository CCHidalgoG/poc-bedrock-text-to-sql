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
MODEL_ID = os.environ['MODEL_ID1']
REGION = os.environ['AWS_REGION2']


bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

def get_llm():
    llm = BedrockChat(
        model_id=MODEL_ID,
        client=bedrock_runtime,  # Use the same client instance
        model_kwargs={
            "temperature": 0,
            "max_tokens": 1000
        }
    )
    return llm


# Function to configure the LLM with AWS Bedrock using the custom class

def invoke_bedrock_model(prompt, model_id=MODEL_ID):
    response = bedrock_runtime.invoke_model(
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


def query_postgresql(query):
    try:
        connection = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password")
        )
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        connection.close()
        return records, column_names
    except (Exception, psycopg2.Error) as error:
        return f"Error al conectar a PostgreSQL: {error}"


def get_sql_from_question_bedrock(question, all_domain_descriptions, memory):
    prompt = (
        "Eres un asistente especializado en transformar preguntas en consultas SQL.\n"
        f"Tu tarea es transformar la siguiente pregunta en una consulta SQL: {question}\n\n"
        "IMPORTANTE:\n"
        "- Todos los campos en la base de datos están almacenados como VARCHAR/STRING\n"
        "- Para operaciones matemáticas, usa CAST(campo AS TIPO), ejemplo:\n"
        "  * Para números enteros: CAST(valor AS INTEGER)\n"
        "  * Para decimales: CAST(valor AS DECIMAL(10,2))\n"
        "  * Para fechas: CAST(fecha AS DATE)\n"
        "- Siempre usa CAST al comparar o calcular valores numéricos\n\n"
        "Todos los nombres de las columnas deben de ir entre comillas dobles :\n"
        "Usa los siguientes dominios de datos para ayudar en la creación de la consulta SQL:\n"
        "Por favor, devuelve solo la consulta SQL dentro de un bloque ```sql```. No incluyas ninguna otra explicación o comentario."
    )

    # Adicionar descrições de colunas para todos os domínios
    for domain, details in all_domain_descriptions.items():
        schema_table = f"Schema: {details['schema']}, Tabela: {details['table']}"
        columns_description = "\n".join([f"{col}: {desc}" for col, desc in details["columns"].items()])
        prompt += f"\nDomínio {domain}:\n{schema_table}\n{columns_description}\n"

    # Invocar o modelo Bedrock para gerar a consulta SQL
    sql_response = invoke_bedrock_model(prompt)

    # sql_response = response.choices[0].message.content.strip()  # PONTO DE ATENCAO - VERIFICAR OUTPUT DO MODELO
    content = sql_response['content'][0]['text']  # Assuming it's always in the first item of content list

    # Usar regex para extrair a consulta SQL dentro do bloco sql
    match = re.search(r"```sql\n(.*?)\n```", content, re.DOTALL)
    if match:
        query = match.group(1).strip()
    else:
        query = content

    memory.save_context({"input": question}, {"output": query})
    return query


def interpret_results_with_bedrock(question, results, headers, memory):
    # Formatar a tabela para facilitar a leitura pelo modelo Bedrock
    table = tabulate(results, headers=headers, tablefmt="grid")

    prompt = (
        "Eres un asistente inteligente. A continuación se muestra una pregunta hecha por un usuario, seguida de una tabla de datos que fue devuelta por una consulta SQL."
        "Tu tarea es analizar estos datos y responder a la pregunta del usuario de manera clara y directa, teniendo en cuenta los encabezados de la tabla.\n\n"
        f"Pregunta: {question}\n\n{table}\n\n"
        "Interpreta estos datos y responde a la pregunta anterior en función de los resultados proporcionados."
    )

    try:
        # Invocar o modelo Bedrock para interpretar os resultados
        interpretation = invoke_bedrock_model(prompt)
        content = interpretation['content'][0]['text']  # Assuming it's always in the first item of content list
        memory.save_context({"input": question}, {"output": content})
        return content
    except Exception as e:
        return f"Error al interpretar los resultados: {e}"
    

def create_memory():
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="history"
    )
    return memory


# Função para obter a resposta do chatbot com contexto de memória
def get_chat_response(input_text, memory):
    llm = get_llm()  # Utilize o LLM personalizado Bedrock
    conversation_with_memory = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
    )

    # Gera a resposta do chatbot com o contexto atual
    chat_response = conversation_with_memory.invoke(input=input_text)  # Passa a mensagem do usuário e o resumo para o modelo
    return chat_response['response']
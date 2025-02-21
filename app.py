import boto3
import json
import re
import os
import psycopg2
from dotenv import load_dotenv
from settings import DOMAIN_DESCRIPTIONS

# Cargar variables desde .env
load_dotenv()

# Conexión a la base de datos PostgreSQL
#host = os.getenv("host")
#database = os.getenv("database")
#user = os.getenv("user")
#password = os.getenv("password")

#try:
#    connection = psycopg2.connect(host=host, database=database, user=user, password=password)
#    cursor = connection.cursor()
#    # ... (resto del código)
#except (Exception, psycopg2.Error) as error:
#    print(f"Error while connecting to PostgreSQL {error}"

# Set up AWS credentials
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


bedrock_client = boto3.client('bedrock', region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY, 
                              aws_secret_access_key=AWS_SECRET_KEY)


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
        return f"Error while connecting to PostgreSQL {error}"


def get_llm(input_text):
    payload = {
        "anthropic_version": "bedrock-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": input_text
            }
        ]
    }
    
    payload_bytes = json.dumps(payload).encode('utf-8')

    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        contentType='application/json',
        accept='application/json',
        body=payload_bytes
    )

    return json.loads(response['body'].read().decode('utf-8'))

question = "What is the meaning of life?"

prompt = (
    "Usted es un asistente especializado en transformar preguntas en consultas SQL.\n"
    f"Su tarea es transformar la siguiente pregunta en una consulta SQL: {question}\n\n"
    "IMPORTANTE:\n"
    "- Todos los campos en la base de datos están almacenados como VARCHAR/STRING\n"
    "- Para operaciones matemáticas, utilice CAST(campo AS TIPO), ejemplo:\n"
    "  * Para números enteros: CAST(valor AS INTEGER)\n"
    "  * Para decimales: CAST(valor AS DECIMAL(10,2))\n"
    "  * Para fechas: CAST(fecha AS DATE)\n"
    "- Siempre utilice CAST al comparar o calcular valores numéricos\n\n"
    "Use los siguientes dominios de datos para ayudar en la creación de la consulta SQL:\n"
    "Por favor, devuelva solo la consulta SQL dentro de un bloque ```sql```. No incluya ninguna otra explicación o comentario\n"
)

for domain, details in DOMAIN_DESCRIPTIONS.items():
    schema_table = f"Schema: {details['schema']}, Table: {details['table']}"
    columns_description = "\n".join([f"{col}: {desc}" for col, desc in details["columns"].items()])
    prompt += f"\nDomain {domain}:\n{schema_table}\n{columns_description}\n"

response = get_llm(prompt)

sql_response = response

# sql_response = response.choices[0].message.content.strip()  # PONTO DE ATENCAO
content = sql_response['content'][0]['text']  # Assuming it's always in the first item of content

# Usar regex para extrair a consulta SQL dentro do bloco sql
match = re.search(r"```sql\n(.*?)\n```", content, re.DOTALL)
if match:
    query = match.group(1).strip()
else:
    query = content

query_postgresql(query)

#query = format_sql_response(sql_response)  # Passe a memória se necessário
#print(query)

print(response)
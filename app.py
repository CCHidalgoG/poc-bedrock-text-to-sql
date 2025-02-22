# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api.html
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html#getting-started-model-access
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-ex-python.html
# https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html

import json
import re
import os
import psycopg2
import boto3
from dotenv import load_dotenv
from settings import DOMAIN_DESCRIPTIONS

# Cargar variables desde .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
MODEL_ID = os.environ['MODEL_ID1']
REGION = os.environ['AWS_REGION2']

bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


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
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": input_text
            }
        ]
    }
    
    payload_bytes = json.dumps(payload).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
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




#####################################################################################################################3
sts_client = boto3.client('sts')

# Qué usuario soy?
try:
    # Obtiene la identidad del usuario actual
    response = sts_client.get_caller_identity()
    
    # Imprime los detalles del usuario
    print("Detalles del usuario:")
    print(f"ARN: {response['Arn']}")
    print(f"ID de cuenta: {response['Account']}")
    print(f"ID de usuario: {response['UserId']}")
except Exception as e:
    print(f"Error al obtener la identidad del usuario: {e}")

# Configurar cliente AWS Bedrock
bedrock_client = boto3.client(
    'bedrock',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


try:
    # Llama al método para listar los modelos disponibles
    response = bedrock_client.list_foundation_models()
    
    # Imprime la respuesta
    print("Modelos disponibles en Bedrock:")
    for model in response.get('modelSummaries', []):
        print(model['modelId'])
except Exception as e:
    print(f"Error al acceder a Bedrock: {e}")

#############################PROMPT#############################################3
prompt = "¿Cuál es la capital de Francia?"

try:
    # Invoca el modelo
    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,  # Modelo a usar
        contentType="application/json",                      # Tipo de contenido
        accept="application/json",                           # Formato de respuesta
        body=json.dumps({
            "prompt": prompt,                                # Pregunta o entrada
            "max_tokens_to_sample": 100                     # Máximo número de tokens en la respuesta
        })
    )
    
    # Procesa la respuesta
    result = json.loads(response['body'].read())
    print("Respuesta del modelo:")
    print(result['completion'])  # Imprime la respuesta generada por el modelo

except Exception as e:
    print(f"Error al invocar el modelo: {e}")

################################################################################################################
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-api-ex-python.html
from botocore.exceptions import ClientError

# Create an Amazon Bedrock Runtime client.
brt = boto3.client("bedrock-runtime")

# Set the model ID, e.g., Amazon Titan Text G1 - Express.
model_id = os.environ['MODEL_ID1']

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Format the request payload using the model's native structure.
native_request = {
    "inputText": prompt,
    "textGenerationConfig": {
        "maxTokenCount": 512,
        "temperature": 0.5,
        "topP": 0.9
    },
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    response = brt.invoke_model(modelId=model_id, body=request)
except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# POC Bedrock Text-to-SQL

Este proyecto implementa una aplicación web usando [Streamlit](https://streamlit.io/) que integra AWS Bedrock y Langchain para transformar preguntas en lenguaje natural en consultas SQL, ejecutar las consultas en una base de datos PostgreSQL, e interpretar los resultados.

## Funcionalidades

1. **Transformación de Preguntas en SQL**: La aplicación usa la integración con AWS Bedrock (Claude) para generar consultas SQL a partir de preguntas en lenguaje natural.
2. **Ejecución de Consultas SQL**: Las consultas generadas se ejecutan en una base de datos PostgreSQL, y los resultados se muestran directamente en la interfaz.
3. **Interpretación de los Resultados**: La aplicación también usa AWS Bedrock para interpretar los resultados de las consultas SQL y proporcionar una explicación detallada de los datos.
4. **Memoria de Conversación**: El chatbot mantiene el historial de interacciones utilizando `ConversationSummaryBufferMemory` de Langchain, permitiendo que el contexto de las interacciones anteriores sea considerado en las conversaciones subsecuentes.

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrese de tener las siguientes dependencias instaladas:

1. **Python 3.7 o superior**: [Descargar Python](https://www.python.org/downloads/)
2. **PostgreSQL**: Asegúrese de tener acceso a una base de datos PostgreSQL.
3. **AWS CLI**: Configure sus credenciales de AWS, ya que el proyecto utiliza AWS Bedrock para el procesamiento de lenguaje natural. Para configurar el CLI, siga [esta guía](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
4. **Dependencias del Proyecto**: Asegúrese de tener un archivo `.env` con las variables de entorno necesarias, como las credenciales de la base de datos y las configuraciones de AWS.

## Instalación

### 1. Clonar el Repositorio

Clone el repositorio en su entorno local:
```bash
git clone https://github.com/SU-USUARIO/poc-bedrock-text-to-sql.git
```

```cmd
cd poc-bedrock-text-to-sql
```

```cmd
python -m venv .venv
```

```cmd
source .venv/bin/activate
```

```cmd
.venv\Scripts\activate
```

```cmd
pip install -r requirements.txt
```

# Configuraciones de PostgreSQL
host=SU_HOST_DE_POSTGRESQL
database=NOMBRE_DE_SU_BASE_DE_DATOS
user=SU_USUARIO_DE_LA_BASE
password=SU_CONTRASEÑA_DE_LA_BASE

# Credenciales de AWS
AWS_ACCESS_KEY_ID=SU_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=SU_SECRET_KEY
AWS_DEFAULT_REGION=SU_REGION_AWS

# Otras configuraciones, si es necesario

```cmd
streamlit run chatfrontend.py
```

### Cambios Adicionales:
- **Sección de Entorno Virtual (venv)**: Explicación de cómo crear y activar un entorno virtual para aislar las dependencias.
- **Sección `.env`**: Incluye más detalles sobre el archivo `.env` y cómo configurarlo.
- **Instrucciones Detalladas para la Instalación**: Ahora detalla todos los pasos desde clonar el repositorio hasta ejecutar la aplicación con el entorno virtual.

## Requisitos Previos

Asegúrese de tener Python y las siguientes bibliotecas instaladas:

- pandas
- SQLAlchemy
- python-dotenv
- psycopg2-binary (para conexión con PostgreSQL)

Para instalar las dependencias, ejecute:

```bash
pip install pandas SQLAlchemy python-dotenv psycopg2-binary
```

**Detalles Específicos de la Aplicación**
La aplicación se compone de dos componentes principales:

Frontend: Implementado en chatfrontend.py usando Streamlit. Proporciona la interfaz de usuario para interactuar con el chatbot.
Backend: Implementado en chatbackend.py. Contiene la lógica para transformar preguntas en consultas SQL, ejecutar consultas en PostgreSQL e interpretar los resultados usando AWS Bedrock.

**Detalles de Langchain**
Langchain es una biblioteca que facilita la integración de modelos de lenguaje con flujos de trabajo de datos. En este proyecto, Langchain se usa para:

Memoria de Conversación: Utiliza `ConversationSummaryBufferMemory` para mantener el historial de interacciones.
Cadenas de Conversación: Utiliza `ConversationChain` para gestionar el flujo de conversación entre el usuario y el chatbot.
Modelos de Lenguaje: Integración con AWS Bedrock para generar consultas SQL e interpretar resultados.
Para más información sobre Langchain, visite la documentación oficial.

### Activación del Modelo de Marketing en AWS Bedrock
**Crear una función IAM con permisos para Bedrock:**

Acceda al consola de IAM en AWS.
Cree una nueva función con permisos para acceder al servicio Bedrock.
Adjunte las políticas necesarias, como AmazonBedrockFullAccess.

**Activar el modelo de marketing:**

En la consola de AWS Bedrock, navegue hasta la sección de modelos.
Seleccione el modelo de marketing (por ejemplo, anthropic.claude-3-5-sonnet-20240620-v1:0).
Siga las instrucciones para activar el modelo en la documentación de AWS:
https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html

![image](https://github.com/user-attachments/assets/234c351e-3412-4958-9e80-c56b1651b2f7)

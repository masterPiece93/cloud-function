import psycopg2
from google.cloud.sql.connector import Connector
import pg8000.dbapi
from typing import Final, Dict, Tuple, Set


__all__ = [
    'get_all_supported_projects',
    'get_all_supported_db_types',
    'get_supported_db_types',
    'get_all_supported_env_names',
    'get_supported_env_names',
    'attempt_connection'
]

DATABASE:Final[Dict[str, str]]  = dict(
    datti={
        "postgres":{
            # "dev": {                  # <-- REF 1
            #     'dbname': '...',
            #     'user': '...',
            #     'password': '...',
            #     'host': '...',
            #     'port': '...'
            # },
            # "qa": {
            #     'dbname': '...',
            #     'user': '...',
            #     'password': '...',
            #     'host': '...',
            #     'port': '...'
            # },
        },
        "cloud-sql-postgres":{
            "dev": {
                'dbname': '...',
                'user': '...',
                'password': '...',
                'host': '...',
                'port': '...'
            },
        },
    },
    local={
        "postgres":{
            "dev": {
                'dbname': 'mydatabase',
                'user': 'myuser',
                'password': 'mypassword',
                'host': 'localhost',
                'port': '5433'
            },
        },
    }
    
)


def get_all_supported_projects() -> Tuple[str]:
    return tuple(DATABASE.keys())

def get_all_supported_db_types() -> Tuple[str]:
    result: Set = set()
    for value in DATABASE.values():
        for key in value:
            result.add(key)
    return tuple(result)

def get_supported_db_types(project: str) -> Tuple[str]:
    return tuple(DATABASE[project].keys())

def get_all_supported_env_names() -> Tuple[str]:
    result: Set = set()
    for key1, value1 in DATABASE.items():
        for value2 in DATABASE[key1].values():
            for key2 in value2:
                result.add(key2)
    return tuple(result)

def get_supported_env_names(project: str, db_type: str) -> Tuple[str]:
    return tuple(DATABASE[project][db_type].keys())


def attempt_connection(project: str, env_name: str = 'dev', database_type: str = 'postgres'):
    conn = None  # Initialize conn to None
    messages = []

    # credentials verification
    try:
        connection_params = DATABASE[project][database_type][env_name]
        messages.append(f"connection params found.")
    except:
        messages.append(f"creds not available for project: {project} for provided env : {env_name} for database : {database_type}")
        return messages
    
    # connection with classic postgres db
    if database_type == "postgres":
        try:
            conn = psycopg2.connect(**connection_params)
            messages.append("Connection to PostgreSQL database successful!")
            # You can now create a cursor and execute queries
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            messages.append(cursor.fetchone())
        except psycopg2.Error as e:
            messages.append(f"Error connecting to PostgreSQL database: {e}")
        finally:
            if conn:
                conn.close()
                messages.append("PostgreSQL connection closed.")
    
    # connection with cloudSql postgres 
    if database_type == "cloud-sql-postgres":
        # Define instance connection name (e.g., "project-id:region:instance-name")
        instance_connection_name = connection_params["host"]

        # Define database credentials
        database_user = connection_params["user"]
        database_password = connection_params["password"]
        database_name = connection_params["dbname"]

        # Create a connection
        connector = Connector()
        with connector.connect(
            instance_connection_name,
            "pg8000",
            user=database_user,
            password=database_password,
            db=database_name,
        ) as conn:
            messages.append("Connection to CloudSql(:PostgreSQL) database successful!")
            # Create a cursor object
            cursor = conn.cursor()

            # Execute a query (example: fetch version)
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            messages.append(f"PostgreSQL version: {result[0]}")

            # Close the cursor and connection (handled by 'with' statement)
        
    return messages


# Code Comment References :
# -------------------------

# REF 1 :
# # - this code was written to test on a live database .
# # - so , this comment is left here to show how to add your
# #     enterprise/application databases .


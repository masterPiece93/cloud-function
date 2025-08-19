import os
import logging
import functions_framework
from flask import request, jsonify, redirect, render_template, url_for
from typing import Final
from test_gcs_conn import bucket_metadata
import test_db_conn as db
from environs import Env


# ENV VARIABLES
env = Env()
env.read_env() # Reads .env file in the current directory

DEBUG: Final[bool] = env.bool("DEBUG")
ENV: Final[str] = env.str("ENV")
SA_FILE_PATH: Final[str] = env.str('SA_FILE_PATH')

__supported_envs__ = ('dev', 'qa', 'stage', 'prod', )
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_FILE_PATH
os.environ["STORAGE_EMULATOR_HOST"] = "http://localhost:8000"
try:
    from google.cloud import storage
    storage_client = storage.Client()
    bucket_name="my-test-bucket"
    bucket = storage_client.create_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' created.")
except Exception as e:
    print(f"Bucket '{bucket_name}' already exists or error: {e}")
# - x -


# LOGGING
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.INFO
# - x -


# UTILITIES
def redirect_to_https():
    if request.is_secure:
        return # Already on HTTPS, do nothing
    
    # Check for X-Forwarded-Proto header if behind a proxy/load balancer
    # This header indicates the original protocol of the request
    if request.headers.get('X-Forwarded-Proto') == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301) # Use 301 for permanent redirect
    
    # Fallback for direct HTTP requests without X-Forwarded-Proto
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
# - x -


# Main
@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function that processes a request."""

    if ENV in __supported_envs__[2:]:
        value = redirect_to_https()
        if value:
            return value

    if request.path == "/" and request.method == "GET":
        base_path = request.path.rstrip('/')
        return render_template('home.html',
            bucket_meta_path= base_path + '/bucket-meta',
            db_postgres_path= base_path + '/db-conn',
        )
    
    if request.path == "/bucket-meta" and request.method == "GET":
        bucket_name = request.args.get('name', '@bucket_dev_td_11@')
        if not bucket_name.startswith('@') and not bucket_name.endswith('@'):
            bucket_name = "@bucket_dev_td_11@"
        bucket_name = bucket_name.strip('@')
        logger.info(f"fetching details for bucket : {bucket_name}")
        messages = bucket_metadata(bucket_name)
        return render_template('bucket_metadata.html', messages=messages)
    
    if request.path == "/db-conn" and request.method == "GET":
        # Query Param Parsing
        
        valid_project_names: tuple = db.get_all_supported_projects()
        
        default_env_name: str = 'dev'
        default_db_type: str = 'postgres'
        
        required_qparams: tuple = ('project', )
        
        project = request.args.get('project', '')
        if project.lower() not in valid_project_names:
            if "project" in required_qparams:
                return f"A valid `project` is required."
            else:
                ...
        
        db_type = request.args.get('db_type', 'postgres')
        if db_type not in db.get_supported_db_types(project):
            if "db_type" in required_qparams:
                return f"A valid `db_type` is required."
            else:
                db_type = default_db_type
        
        env_name = request.args.get('env_name', 'dev')
        if env_name.lower() not in db.get_supported_env_names(project, db_type):
            if "env_name" in required_qparams:
                return f"A valid `env_name` is required."
            else:
                env_name = default_env_name
        
        
        logger.info(f"attempting connecting to env : {project}:{db_type}:{env_name}")

        # attempting connection
        messages = db.attempt_connection(project, env_name=env_name, database_type=db_type)
        return render_template('db_conn.html', messages=messages)
    
    return "Not Implemented", 405
    
# POC : Cloud Function 

- testing cloud function connection to :
    - google bucket ( using emulator for local testing )
    - postgre sql ( using docker image of postgres for local testing )
    - cloud sql ( can be tested on cloud function only )

So we currently have two endpoints available 
1. /bucket-meta : for testing bucket connection
2. /db-conn : for testing db related connection
    - for testing a new database , you need to add the credentials in the `test_db_conn.py` file .


### Env Setting
Following varibles must be set for environment
```sh
ENV='dev'
DEBUG=true
SA_FILE_PATH='datti_sa.json'
```

> `ENV` : used to control which environment your are deploying this code

> `DEBUG` : used to control debug mode of code

> `SA_FILE_PATH` : used to set the service account file path. It is used in bucket test


### Running Cloud Function

- Create venv
- Install requirements in it.
- ```sh
    # running cloud function
    functions-framework --target hello_http --signature-type http --debug --port 8080
    ```

### Starting Services 
For testing on local , we need 'google cloud storage' and 'postgres database' in our local.
hence we use :
    - gcs emulator ( via docker image )
    - postgres db ( via docker image )
we have added their configs in the `docker-compose.yml` file .
Run the following command in a seperate terminal :
```sh
# start services ( gcs emulator, postgres, ...)
docker compose up
```

<!-- PERSONAL NOTES -->
<!-- # sample service accounts will be found in your personal GDrive -->
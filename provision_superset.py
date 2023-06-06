import json
import os
import sys
import psycopg2
import string
import random
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from nginx import create_nginx_config
from dotenv import load_dotenv
import yaml

def generate_random_password(length=10):
    # Define the characters to be used in the password
    characters = string.ascii_letters + string.digits

    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

def create_folder(unit_name: str):
    # Create the unit folder
    try:
        os.mkdir(unit_name)
        print(f"Folder '{unit_name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{unit_name}' already exists.")
    except Exception as e:
        print(f"Error occurred while creating folder: {str(e)}")

def create_secret_json(unit_name: str):
    # create a database connection to keycloak
    keycloak_conn = create_db_conn("keycloak")

    cursor = keycloak_conn.cursor()

    # get client secret from database
    cursor.execute(f'''
    select client.client_id,client.secret from client, realm 
        where client.client_id = 'superset' 
            and client.realm_id = realm.id 
            and realm.name = '{unit_name}';''')

    client_id, client_secret = cursor.fetchone()

    data = {
        "web": {
            "issuer": f"https://sso.ducluong.monster/realms/{unit_name}",
            "auth_uri": f"https://sso.ducluong.monster/realms/{unit_name}/protocol/openid-connect/auth",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [
                f"https://{unit_name}.superset.ducluong.monster/*"
            ],
            "userinfo_uri": f"https://sso.ducluong.monster/realms/{unit_name}/protocol/openid-connect/userinfo",
            "token_uri": f"https://sso.ducluong.monster/realms/{unit_name}/protocol/openid-connect/token",
            "token_introspection_uri": f"https://sso.ducluong.monster/realms/{unit_name}/protocol/openid-connect/token/introspect"
        }
    }

    # Specify the file path for the JSON file
    file_path = f"{unit_name}/client_secret.json"

    # Write the data to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)

    # close connection
    keycloak_conn.close()

    print("JSON file client_secret.json created successfully.")

def create_datbase_resource(unit_name: str, conn):
    # Create a cursor object
    with conn.cursor() as cursor:
        db_name = f"superset_{unit_name}"

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        database_exists = bool(cursor.fetchone())

        if not database_exists:
            # SQL query to create a database
            create_db_query = f"CREATE DATABASE {db_name}"

            # Execute the SQL query
            cursor.execute(create_db_query)

            # Create the username and password for the superset
            superset_username = f"superset_user_{unit_name}"
            superset_password = generate_random_password(32)

            # Check if the user exists
            cursor.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{superset_username}'")
            user_exists = bool(cursor.fetchone())

            if not user_exists:
                # SQL queries to create the user and grant privileges
                create_user_query = f"CREATE USER {superset_username} WITH PASSWORD '{superset_password}';"
                grant_privileges_query = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {superset_username};"

                # Execute the SQL query
                cursor.execute(create_user_query)
                cursor.execute(grant_privileges_query)
                
                # Create a connection to new superset database
                superset_conn = create_db_conn(db_name=db_name) 

                # Grant all priviledges on schema public
                grant_schema_access = f"GRANT ALL PRIVILEGES ON SCHEMA public TO {superset_username};"

                with superset_conn.cursor() as inner_cursor:
                    inner_cursor.execute(grant_schema_access)

                # close connection
                superset_conn.close()
                print(f"Database '{db_name}' created successfully.")

                return db_name, superset_username, superset_password

            else:
                raise Exception(f"User {superset_username} has existed!")
        
        else:
            raise Exception(f"Database {db_name} has existed!") 



def create_dockerfile(unit_name: str, dbname: str, username: str, password: str):
    dockerfile = f'''FROM ducluongvn/superset_extended
USER root
WORKDIR /app

ENV DATABASE_DIALECT=postgres
ENV DATABASE_USER={username}
ENV DATABASE_PASSWORD={password}
ENV DATABASE_HOST=159.223.66.111
ENV DATABASE_PORT=5432
ENV DATABASE_DB={dbname}

USER superset

COPY client_secret.json ./pythonpath/

RUN superset db upgrade
RUN superset init

EXPOSE 8088
    '''

    # Specify the file path for the Dockerfile
    file_path = f"{unit_name}/Dockerfile"

    # Write the Dockerfile content to a file
    with open(file_path, "w") as dockerfile_file:
        dockerfile_file.write(dockerfile)

    print("Dockerfile created successfully.")

# Function to add a new service to the Docker Compose file
def add_service_to_docker_compose(unit_name):
    # Load the existing Docker Compose file
    with open('docker-compose.yml', 'r') as file:
        docker_compose = yaml.safe_load(file)

    # Create a new service
    new_service = {
        f'superset_{unit_name}': {
            'image': f'ghcr.io/luongnguyentrong/lvtn_superset/{unit_name}:master'
        }
    }

    # Add the new service to the Docker Compose file
    docker_compose['services'].update(new_service)

    # Save the modified Docker Compose file
    with open('docker-compose.yml', 'w') as file:
        yaml.dump(docker_compose, file)

def create_db_conn(db_name: string):
    # Connect to PostgreSQL
    conn = psycopg2.connect(dsn=os.getenv("POSTGRES_DSN") + "/" + db_name) 

    conn.autocommit = True
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

    return conn

def main():
    # Load local env variables
    load_dotenv()

    # Check if the folder name is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide a unit name as a command-line argument.")
        sys.exit(1)

    try:
        # Get the folder name from the command-line argument
        unit_name = sys.argv[1]

        # create a connection to metadata database
        db_conn = create_db_conn("metadata")

        # Create the unit folder
        create_folder(unit_name=unit_name)

        # create json secret file in unit folder
        create_secret_json(unit_name=unit_name)

        # create database resource
        dbname, superset_username, superset_password = create_datbase_resource(unit_name=unit_name, conn=db_conn)

        # create docker file
        create_dockerfile(unit_name=unit_name, dbname=dbname, username=superset_username, password=superset_password)

        # add new superset service to docker compose
        add_service_to_docker_compose(unit_name=unit_name)

        # create nginx server block
        create_nginx_config(unit_name=unit_name)

        # close db conn
        db_conn.close()

        print("Success!")

    except Exception as e:
        print("Provision failed: ", e)

main()
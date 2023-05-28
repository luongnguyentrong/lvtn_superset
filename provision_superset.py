import json
import os
import sys
import psycopg2
import string
import random
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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
    data = {
        "web": {
            "issuer": f"https://sso.ducluong.monster/realms/{unit_name}",
            "auth_uri": f"https://sso.ducluong.monster/realms/{unit_name}/protocol/openid-connect/auth",
            "client_id": "superset",
            "client_secret": "QyRIJn5UWSpurK9e4hU6Sv6uamRK5PpY",
            "redirect_uris": [
                f"https://{unit_name}.superset.ducluong.monster"
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

    print("JSON file client_secret created successfully.")

def create_datbase_resource(unit_name: str):
    host = "159.223.66.111"
    port = "5432"
    database = "postgres"
    user = "api_server"
    password = "634zgwxwsjvt5179ximsmkhmg2uxnq5q"

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    ) 

    conn.autocommit = True
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

    # Create a cursor object
    cursor = conn.cursor()

    # SQL query to create a database
    db_name = f"superset_{unit_name}"
    create_db_query = f"CREATE DATABASE {db_name}"

    # Execute the SQL query
    cursor.execute(create_db_query)

    # Create the username and password for the superset
    superset_username = f"superset_user_{unit_name}"
    superset_password = generate_random_password(32)

    # SQL queries to create the user and grant privileges
    create_user_query = f"CREATE USER {superset_username} WITH PASSWORD '{superset_password}';"
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {superset_username};"

    # Execute the SQL query
    cursor.execute(create_user_query)
    cursor.execute(grant_privileges_query)
    
    with psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=user,
        password=password
    ) as inner_conn:
        grant_schema_access = f"GRANT ALL PRIVILEGES ON SCHEMA public TO {superset_username};"

        with inner_conn.cursor() as inner_cursor:
            inner_cursor.execute(grant_schema_access)

    cursor.close()
    conn.close()

    print(f"Database '{db_name}' created successfully.")

    return db_name, superset_username, superset_password

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



def main():
    # Check if the folder name is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide a unit name as a command-line argument.")
        sys.exit(1)

    # Get the folder name from the command-line argument
    unit_name = sys.argv[1]

    # Create the unit folder
    create_folder(unit_name=unit_name)

    # create json secret file
    create_secret_json(unit_name=unit_name)

    # create database resource
    dbname, superset_username, superset_password = create_datbase_resource(unit_name=unit_name)

    # create docker file
    create_dockerfile(unit_name=unit_name, dbname=dbname, username=superset_username, password=superset_password)

    print("Success!")

main()
# Provision superset and manage deploy config

### Provision a new superset server for a unit

- Step #1:
    ```
    # activate venv and install required packages
    source ./venv/bin/activate
    ```

- Step #2:

    This step creates:
    - A folder named <unit_name> in this repository that contains a client_secret.json file (Keycloak endpoints and client secrets) and dockerfile for new superset server. 
    - A database named superset_\<unit_name\>, and a user role superset_user_<unit_name> for new superset server
    - An Nginx server block file nginx_<unit_name>.conf in /nginx/conf.d to proxy request to <unit_name>.superset.ducluong.monster to this server 

    ```
    # run provision.py script with unit_name, e.g: python provision.py <unit_name>
    python provision_superset.py <unit_name>
    ```

- Step #3:

    Run the post-deploy script which simply updates the superset_status to 'success'
    ```
    python post_deploy.py
    ```
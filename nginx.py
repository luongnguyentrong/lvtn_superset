import os

# Function to create a new Nginx configuration file
def create_nginx_config(unit_name):
    nginx_config = f'''
server {{
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name {unit_name}.superset.ducluong.monster;
    ssl_certificate /etc/letsencrypt/live/superset.ducluong.monster/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/superset.ducluong.monster/privkey.pem;

    location / {{
        proxy_pass http://superset_{unit_name}:8088/;
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Origin $http_origin; # Add this line
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
'''

    # Save the Nginx configuration file in nginx/conf.d directory
    filename = f'nginx_{unit_name}.conf'
    filepath = os.path.join('nginx', 'conf.d', filename)
    with open(filepath, 'w') as file:
        file.write(nginx_config)

    print(f'Nginx configuration file "{filename}" has been created in nginx/conf.d directory.')
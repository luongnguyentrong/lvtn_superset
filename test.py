import yaml

# Function to add a new service to the Docker Compose file
def add_service_to_docker_compose(unit_name):
    # Load the existing Docker Compose file
    with open('docker-compose.yml', 'r') as file:
        docker_compose = yaml.safe_load(file)

    # Create a new service
    new_service = {
        f'superset_{unit_name}': {
            'image': f'ghcr.io/luongnguyentrong/lvtn_superset/{unit_name}'
        }
    }

    # Add the new service to the Docker Compose file
    docker_compose['services'].update(new_service)

    # Save the modified Docker Compose file
    with open('docker-compose.yml', 'w') as file:
        yaml.dump(docker_compose, file)

# User input for the unit name
unit_name = input('Enter the unit name: ')

# Add the new service to the Docker Compose file
add_service_to_docker_compose(unit_name)

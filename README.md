# keycloak-py-config

Docker image to configure a keycloak instance using a python 3 script.
The container will run the python script and then exit.
It waits for the keycloak instance to be up and running before running the script.

## Usage

docker run -e KEYCLOAK_URL=http://keycloak:8080/auth -e KEYCLOAK_ADMIN_USER=admin -e KEYCLOAK_ADMIN_PASSWORD=admin -e OTHER_VARS=TEST -v /path/to/script.py:/app/config.py -it --rm keycloak-py-config
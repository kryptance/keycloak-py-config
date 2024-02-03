FROM python:3.9

MAINTAINER ab@kryptance.de

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Define environment variable
ENV KEYCLOAK_URL http://keycloak:8080/auth
ENV KEYCLOAK_ADMIN admin
ENV KEYCLOAK_ADMIN_PASSWORD admin

# Run mounted python script
CMD wait-for-it --service $KEYCLOAK_URL -- python /app/config.py
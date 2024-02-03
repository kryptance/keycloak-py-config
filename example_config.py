from os import environ

from keycloak import KeycloakAdmin

print("Configuring Keycloak...")
# print the environment variables
print(f"KEYCLOAK_URL: {environ.get('KEYCLOAK_URL')}")
print(f"KEYCLOAK_ADMIN: {environ.get('KEYCLOAK_ADMIN')}")
print(f"KEYCLOAK_ADMIN_PASSWORD: {environ.get('KEYCLOAK_ADMIN_PASSWORD')}")

# Initialize KeycloakAdmin client
keycloak_admin = KeycloakAdmin(server_url=environ.get("KEYCLOAK_URL"),
                               username=environ.get("KEYCLOAK_ADMIN"),
                               password=environ.get("KEYCLOAK_ADMIN_PASSWORD"),
                               realm_name="master",
                               verify=False)


# Function to create or get realm
def create_or_get_realm(realm_name):
    realms = keycloak_admin.get_realms()
    if not any(realm.get('realm') == realm_name for realm in realms):
        keycloak_admin.create_realm(payload={"realm": realm_name, "enabled": True})
        print(f"Created realm: {realm_name}")
    else:
        print(f"Realm {realm_name} already exists.")


# Function to create or get client scope with protocol mappers
def create_or_get_client_scope(realm_name, client_scope_name, protocol_mappers):
    keycloak_admin.realm_name = realm_name
    client_scopes = keycloak_admin.get_client_scopes()
    if not any(scope.get('name') == client_scope_name for scope in client_scopes):
        client_scope_id = keycloak_admin.create_client_scope(
            payload={"name": client_scope_name, "protocol": "openid-connect"})
        for mapper in protocol_mappers:
            keycloak_admin.add_mapper_to_client_scope(client_scope_id=client_scope_id, payload=mapper)
        print(f"Created client scope: {client_scope_name}")
    else:
        print(f"Client scope {client_scope_name} already exists.")


# Function to create or get client
def create_or_get_client(realm_name, client_name, client_scope_name):
    keycloak_admin.realm_name = realm_name
    clients = keycloak_admin.get_clients()
    if not any(client.get('clientId') == client_name for client in clients):
        keycloak_admin.create_client(
            payload={"clientId": client_name, "protocol": "openid-connect", "defaultClientScopes": [client_scope_name],
                     "directAccessGrantsEnabled": True, "publicClient": True, "redirectUris": ["http://localhost/*"]})
        print(f"Created client: {client_name}")
    else:
        print(f"Client {client_name} already exists.")


# Function to create or get user
def create_or_get_user(realm_name, user_names):
    keycloak_admin.realm_name = realm_name
    for user_name in user_names:
        users = keycloak_admin.get_users(query={"username": user_name})
        if not users:
            keycloak_admin.create_user(
                {"username": user_name, "enabled": True, "emailVerified": True, "firstName": user_name,
                 "lastName": "User", "credentials": [{"type": "password", "value": "password", "temporary": False}]})
            print(f"Created user: {user_name}")
        else:
            print(f"User {user_name} already exists.")


if __name__ == '__main__':
    realm_name = "my_new_realm1"
    client_scope_name = "my_oidc_client_scope"
    client_name = "my_oidc_client"
    user_names = ["admin", "a", "b"]
    protocol_mappers = [
        # Define your protocol mappers here
    ]

    # Execute functions
    create_or_get_realm(realm_name)
    create_or_get_client_scope(realm_name, client_scope_name, protocol_mappers)
    create_or_get_client(realm_name, client_name, client_scope_name)
    create_or_get_user(realm_name, user_names)

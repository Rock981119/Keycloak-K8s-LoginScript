import requests
import urllib3
import json
from getpass import getpass

session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

keycloak_url = input('Keycloak Auth Url: ')
keycloak_realms = input('Keycloak Realms Name: ')
keycloak_client_id = input('Keycloak Client ID: ')
keycloak_client_secret = getpass('Keycloak Client Secret: ')
keycloak_username = input('Username: ')
keycloak_password = getpass('Password: ')

url = keycloak_url + '/auth/realms/' + keycloak_realms + '/protocol/openid-connect/token'

payload = {
    'grant_type': 'password',
    'response_type': 'id_token',
    'scope': 'openid',
    'client_id': keycloak_client_id,
    'client_secret': keycloak_client_secret,
    'username': keycloak_username,
    'password': keycloak_password
}

response = session.request("POST", url, headers=headers, data=payload)

auth_result = json.loads(response.text)

refresh_token = auth_result["refresh_token"]

id_token = auth_result["id_token"]

kubeconfig = '''You can directly copy and paste the commands below\n\n\n
kubectl config set-credentials {keycloak_username} \\
    --auth-provider=oidc \\
    --auth-provider-arg=idp-issuer-url={keycloak_url}auth/realms/{keycloak_realms} \\
    --auth-provider-arg=client-id={keycloak_client_id} \\
    --auth-provider-arg=client-secret={keycloak_client_secret} \\
    --auth-provider-arg=refresh-token={refresh_token} \\
    --auth-provider-arg=id-token={id_token}

'''.format_map(vars())
print("-" * 80)
print(kubeconfig)

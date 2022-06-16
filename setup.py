from setuptools import setup

setup(
    name="quetz-keycloak_auth",
    install_requires="quetz",
    entry_points={
         "quetz.authenticator": [
            "keycloak_auth = quetz_keycloak_auth:KeycloakAuthenticator"
        ]
    },
    packages=[
        "quetz_keycloak_auth",
        ],
)

from setuptools import setup

setup(
    name="quetz-keycloak_auth",
    install_requires="quetz",
    entry_points={
        "quetz": ["quetz-keycloak_auth = quetz_keycloak_auth.main"],
        "quetz.models": ["quetz-keycloak_auth = quetz_keycloak_auth.db_models"],
        "quetz.migrations": ["quetz-keycloak_auth = quetz_keycloak_auth.migrations"],
        "quetz.jobs": ["quetz-keycloak_auth = quetz_keycloak_auth.jobs"]
        },
    packages=[
        "quetz_keycloak_auth",
        "quetz_keycloak_auth.migrations",
        "quetz_keycloak_auth.migrations.versions",
        ],
)

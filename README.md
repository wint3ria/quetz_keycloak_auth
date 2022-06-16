# quetz_keycloak_auth plugin

This is a plugin to use with the [quetz](https://github.com/mamba-org/quetz) package server.


## Installing

To install use:

```
pip install .
```

## Example config.toml section for Quetz server

[keycloak]
url = "http://mydomain.com"
realm = "master"
client_id = "quetz"
client_secret = "myKeycloakClientSecret"
scope = "email profile"

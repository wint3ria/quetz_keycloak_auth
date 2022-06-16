# quetz_keycloak_auth plugin

This is a plugin to use with the [quetz](https://github.com/mamba-org/quetz) package server.
It implements a Keycloak authenticator using the OpenID protocol.
Supported keycloak version: 18.0.1

## Installing

To install use:

```
pip install .
```

## Example config.toml section for Quetz server

Assuming that you are using the "master" realm and you implemented a "quetz" confidential OpenID client:

[keycloak]
url = "http://mydomain.com"
realm = "master"
client_id = "quetz"
client_secret = "myKeycloakClientSecret"
scope = "email profile"

## Limitations

 - Make sure your users have a user name, login, and email defined in your realm. The authenticator will fail otherwise. This is a Quetz requirement to have these fields correctly filled.
 - The Avatar is not working. Keycloak does not provide avatars by default.
 - This module usage is limited to OpenID clients, but it could be extended

I am open to PRs and issues

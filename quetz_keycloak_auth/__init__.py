from quetz.authentication.oauth2 import OAuthAuthenticator
from quetz.config import Config, ConfigEntry, ConfigSection
import logging


class KeycloakAuthenticator(OAuthAuthenticator):

    provider = 'keycloak'
    collect_emails = False
    scope = 'openid'

    def configure(self, config: Config):

        config.register(
            [
                ConfigSection(
                    "keycloak",
                    [
                        ConfigEntry("realm", str),
                        ConfigEntry("url", str),
                        ConfigEntry("client_id", str),
                        ConfigEntry("client_secret", str),
                        ConfigEntry("scope", str)
                    ],
                )
            ]
        )

        if config.configured_section("keycloak"):

            self.realm = config.keycloak_realm
            self.realm_url = f'{config.keycloak_url}/auth/realms/{self.realm}'
            self.access_token_url = f'{self.realm_url}/protocol/openid-connect/token'
            self.authorize_url = f'{self.realm_url}/protocol/openid-connect/auth'
            self.revoke_url = f'{self.realm_url}/protocol/openid-connect/revoke'
            self.userinfo_url = f'{self.realm_url}/protocol/openid-connect/userinfo'
            self.client_id = config.keycloak_client_id
            self.client_secret = config.keycloak_client_secret
            self.is_enabled = True
            if config.configured_section("users"):
                self.collect_emails = config.users_collect_emails
            self.scope = config.keycloak_scope

        else:
            self.is_enabled = False

        # call the configure of base class to set default_channel and default role
        super().configure(config)

    async def userinfo(self, request, token):

        resp = await self.client.get(self.userinfo_url, token=token)
        profile = resp.json()

        # TODO: better avatar implementation
        profile = {
            "id": profile["sub"],
            "name": profile["name"],
            "login": profile["preferred_username"],
            "email": profile["email"],
            "avatar_url": "",
        }

        return profile



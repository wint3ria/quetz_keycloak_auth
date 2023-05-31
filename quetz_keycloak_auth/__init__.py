from quetz.authentication.oauth2 import OAuthAuthenticator
from quetz.config import Config, ConfigEntry, ConfigSection
import json
import logging
logger = logging.getLogger("quetz.frontend.authenticators.keycloak")

import httpx


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
            self.realm_url = f'{config.keycloak_url}/realms/{self.realm}'
            self.access_token_url = f'{self.realm_url}/protocol/openid-connect/token'
            self.authorize_url = f'{self.realm_url}/protocol/openid-connect/auth'
            self.revoke_url = f'{self.realm_url}/protocol/openid-connect/logout'
            self.userinfo_url = f'{self.realm_url}/protocol/openid-connect/userinfo'
            self.validate_token_url = f'{self.realm_url}/protocol/openid-connect/auth'
            self.client_id = config.keycloak_client_id
            self.client_secret = config.keycloak_client_secret
            self.is_enabled = True
            if config.configured_section("users"):
                self.collect_emails = config.users_collect_emails
            self.scope = config.keycloak_scope

        else:
            self.is_enabled = False

        logger.debug(f"KeycloakAuthenticator configuration:\n{json.dumps({
            k: v
            for k, v in self.__dict__.items()
            if k in {"realm", "realm_url", "access_token_url", "authorize_url", "revoke_url", "userinfo_url", "validate_token_url", "client_id", "client_secret", "is_enabled", "collect_emails", "scope"}
        }, indent=4)}")

        # call the configure of base class to set default_channel and default role
        super().configure(config)

    async def userinfo(self, request, token):

        logger.debug(f"Requesting userinfo from {self.userinfo_url} with token {token} from request:\n{request}")

        resp = await self.client.get(self.userinfo_url, token=token)

        try:
            resp.raise_for_status()
        except httpx.RequestError as exc:
            raise RuntimeError(f"An error occurred while requesting {exc.request.url!r}.") from exc
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}:\n{exc.response.text}") from exc

        try:
            profile = resp.json()
        except json.decoder.JSONDecodeError as exc:
            raise RuntimeError(f"Error decoding JSON from {resp.url!r}. Received:\n{resp.text}") from exc

        # TODO: Avatar implementation
        profile = {
            "id": profile["sub"],
            "name": profile["name"],
            "login": profile["preferred_username"],
            "email": profile["email"],
            "avatar_url": "",
        }

        return profile

    async def authenticate(self, request, data=None, dao=None, config=None):
        token = await self.client.authorize_access_token(request)
        profile = await self.userinfo(request, token)

        username = profile["login"]

        # Filtering the refresh token so we can save the token in a cookie
        # session
        token.pop('refresh_token', None)

        auth_state = {"token": json.dumps(token), "provider": self.provider}

        return {"username": username, "profile": profile, "auth_state": auth_state}


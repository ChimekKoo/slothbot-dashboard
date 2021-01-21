from app.cred import get_cred
from requests import post as requests_post
from requests import get as requests_get

cred = get_cred()


class Oauth(object):
    client_id = cred["oauth"]["client-id"]
    client_secret = cred["oauth"]["client-secret"]
    scope = "identify%20guilds"
    redirect_url = "http://localhost:5000/auth"

    discord_auth_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&scope={scope}"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"

    @staticmethod
    def get_token(code):
        payload = {
            "client_id": Oauth.client_id,
            "client_secret": Oauth.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Oauth.redirect_url,
            "scope": Oauth.scope
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        access_token = requests_post(url=Oauth.discord_token_url, data=payload, headers=headers).json().get("access_token")
        return access_token

    @staticmethod
    def get_user_json(access_token):
        headers = {
            "Authorization": "Bearer " + access_token
        }
        user = requests_get(url=Oauth.discord_api_url + "/users/@me", headers=headers).json()
        return user

    @staticmethod
    def get_user_guilds(access_token):
        headers = {
            "Authorization": "Bearer " + access_token
        }
        guilds = requests_get(url=Oauth.discord_api_url + "/users/@me/guilds", headers=headers).json()
        return guilds

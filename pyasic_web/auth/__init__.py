from dataclasses import dataclass, field, asdict
from starlette.middleware import Middleware, sessions

from pyasic_web.auth.users import USERS
from passlib.hash import pbkdf2_sha256

from imia import LoginManager,  UserProvider, authentication
import json
import os
from copy import copy

key = "SECRET"

@dataclass
class User:
    """This is our user model. It may be an ORM model, or any python class, the library does not care of it,
    it only expects that the class has methods defined by the UserLike protocol."""

    username: str
    name: str = "Anon"
    password: str = 'password'
    scopes: list[str] = field(default_factory=list)
    ip_range: str = "*"

    def get_display_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.username

    def get_hashed_password(self) -> str:
        return self.password

    def get_scopes(self) -> list:
        return self.scopes


users = {}
for user in USERS:
    users[user] = User(username=user, name=USERS[user].get("name") or "Anon", password=pbkdf2_sha256.hash(USERS[user]["pwd"]), ip_range=USERS[user].get("ip_range") or "*", scopes=USERS[user].get("scopes") or [])

class JsonProvider(UserProvider):
    def __init__(self, file):
        self.user_map = {}
        self.file = file
        self.load_users()

    async def find_by_id(self, connection, identifier: str):
        return self.user_map.get(identifier)

    async def find_by_username(self, connection, username_or_email: str):
        return self.user_map.get(username_or_email)

    async def find_by_token(self, connection, token: str):
        return self.user_map.get(token)

    def load_users(self):
        with open(self.file, "r") as f:
            users_data = json.loads(f.read())

        for u in users_data:
            self.user_map[u] = User(
                username=users_data[u]["username"],
                name=users_data[u]["name"],
                password=users_data[u]["password"],
                scopes=users_data[u]["scopes"],
                ip_range=users_data[u]["ip_range"],
            )

    def add_user(self, username: str, name: str, password: str, scopes: list, ip_range: str):
        self.user_map[username] = User(username=username, name=name, password=pbkdf2_sha256.hash(password), scopes=scopes, ip_range=ip_range)
        self.dump_users()

    def delete_user(self, uid):
        self.user_map.pop(uid)
        self.dump_users()

    def update_user(self, username: str, name: str, scopes: list, ip_range: str, password: str = None):
        if not username in self.user_map:
            return
        old_user = self.user_map[username]
        if not password:
            password = old_user.get_hashed_password()
        else:
            password = pbkdf2_sha256.hash(password)
        new_user = User(username=username, name=name, password=password, scopes=scopes, ip_range=ip_range)
        self.user_map[username] = new_user  # noqa
        self.dump_users()

    def dump_users(self):
        user_data = copy(self.user_map)
        for u in user_data:
            user_data[u] = asdict(user_data[u])
        with open(self.file, "w") as f:
            f.write(json.dumps(user_data))


user_provider = JsonProvider(os.path.join(os.path.dirname(__file__), "users.json"))
user_provider.dump_users()

login_manager = LoginManager(user_provider=user_provider, password_verifier=pbkdf2_sha256, secret_key=key)

middleware = [
    Middleware(sessions.SessionMiddleware, secret_key=key),
    Middleware(
        authentication.AuthenticationMiddleware,
        authenticators=[authentication.SessionAuthenticator(user_provider)],
        on_failure="redirect",
        redirect_to="/login",
        include_patterns=["\/lpage"],
    )
]

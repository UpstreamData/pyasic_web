from dataclasses import dataclass, field
from starlette.middleware import Middleware, sessions

from pyasic_web.auth.users import USERS
from passlib.hash import pbkdf2_sha256

from imia import LoginManager,  InMemoryProvider, authentication

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
        return str(pbkdf2_sha256.hash(self.password))

    def get_scopes(self) -> list:
        return self.scopes


users = {}
for user in USERS:
    users[user] = User(username=user, name=USERS[user]["name"] if USERS[user].get("name") else "Anon", password=USERS[user]["pwd"], ip_range=USERS[user]["ip_range"] if USERS[user].get("ip_range") else "*")

user_provider = InMemoryProvider(users)

login_manager = LoginManager(user_provider=user_provider, password_verifier=pbkdf2_sha256, secret_key=key)

middleware = Middleware(sessions.SessionMiddleware, secret_key=key)

from starlette.applications import Starlette
from starlette.middleware import Middleware, sessions

from pyasic_web import routes, auth

app = Starlette(
    middleware=[auth.middleware],
    routes=routes.routes,
)

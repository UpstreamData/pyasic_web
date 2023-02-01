from starlette.applications import Starlette

from pyasic_web import routes, auth

app = Starlette(
    middleware=[auth.middleware],
    routes=routes.routes,
)

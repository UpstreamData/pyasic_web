from starlette.applications import Starlette

from pyasic_web import routes, auth, errors

app = Starlette(
    middleware=[*auth.middleware],
    routes=routes.routes,
    exception_handlers=errors.exception_handlers,
    debug=True
)

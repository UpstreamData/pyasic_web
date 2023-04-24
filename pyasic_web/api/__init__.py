from fastapi import FastAPI

from . import v1
from . import realtime

tags_metadata = [
    {
        "name": "v1",
        "description": "API V1",
    }
]

app = FastAPI(
    title="pyasic Web API",
    version="1.0.0",
    contact={
        "name": "Upstream Data",
        "url": "https://github.com/UpstreamData/pyasic_web",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    docs_url="/",
)

# router = APIRouter(prefix="/api")
app.include_router(v1.router)
app.include_router(realtime.router)

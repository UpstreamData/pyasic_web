import asyncio
from pyasic_web import api
from pyasic_web.api.realtime import MinerDataManager
from pyasic_web.web import app

# add API
app.mount("/api", api.app)

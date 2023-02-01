from starlette.templating import Jinja2Templates

from pyasic_web import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

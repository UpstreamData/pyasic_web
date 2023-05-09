import os
from pathlib import Path

from fastapi.templating import Jinja2Templates

from pyasic_web import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def card_exists(path):
    file_loc = Path(__file__).parent
    if os.path.exists(os.path.join(file_loc, path)):
        return True


import uvicorn
from pyasic_web import app

APP = app


def main():
    uvicorn.run("main:APP", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()

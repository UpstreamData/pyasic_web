from pyasic_web.app import app
import uvicorn


def main():
    uvicorn.run("pyasic_web:app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()

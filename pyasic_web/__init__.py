from pyasic_web.app import app
import uvicorn


def main():
    uvicorn.run("app:app", host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()

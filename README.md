# pyasic_web

pyasic_web is a web server for controlling miners and viewing miner data via pyasic, and is fully customizable.

## Running
- Install requirements (ideally in a virtual environment) with `pip install -r requirements.txt`
- Run with `python main.py` from this directory.
- You should now have access on port 8080, login with username `admin` and password `pass`.

## Login
![Login_Page](https://github.com/UpstreamData/pyasic_web/assets/75442874/a9d27160-2447-4556-89f6-39fa78ca5bd1)

## Home Page - No Miners
![Home_Page_1](https://github.com/UpstreamData/pyasic_web/assets/75442874/0f2257d1-c55e-4411-bed9-3a22a3a6d172)

## Scan Page
![Scan_Page](https://github.com/UpstreamData/pyasic_web/assets/75442874/482a8275-8406-4488-8600-1fa421294dcb)

## Home Page - With Miners
![Home_Page_2](https://github.com/UpstreamData/pyasic_web/assets/75442874/9bb3b856-474d-40df-90b1-130c5032daf6)

## Miner Page
![Miner_Page](https://github.com/UpstreamData/pyasic_web/assets/75442874/8e851728-7def-429e-b97f-aee5600d0620)

## User Management
![User_Management](https://github.com/UpstreamData/pyasic_web/assets/75442874/f260cc21-49c9-4a2f-b5e8-4cfdaf60d667)

## Card Management
![Card Management](https://github.com/UpstreamData/pyasic_web/assets/75442874/3332c483-409e-46f8-8a5f-019f6439ff5e)

## API
![API](https://github.com/UpstreamData/pyasic_web/assets/75442874/5683b3ad-8e11-45a3-9c57-ee43cb5d97aa)

Here is an example of how to use the API for this server.

```python3
import httpx
import asyncio

PYASIC_API_LOC = "localhost:8080"

async def test():
    login_data = httpx.post(f"http://{PYASIC_API_LOC}/api/login/", data={"username": "admin", "password": "pass"}).json()

    header = {
        "Authorization": f"{login_data['token_type']} {login_data['access_token']}"
    }
    miner_selector = {
        "miner_selector": "all"
    }
    miner_data = httpx.post(f"http://{PYASIC_API_LOC}/api/v1/miners/", headers=header, data=miner_selector).json()
    print(miner_data)

asyncio.run(test())
```

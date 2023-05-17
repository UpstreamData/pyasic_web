pyasic_web is a web server for controlling miners and viewing miner data via pyasic, and is fully customizable.

By default, pyasic_web runs on port 8080, and is accessible from external devices.  The default login for the administrative user is `admin/pass`.

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

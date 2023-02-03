USERS = {
    "admin": {"name": "Admin", "pwd": "pass", "scopes": ["admin"], "ip_range": "*"},
    "user": {
        "name": "Normie",
        "pwd": "pass",
        "scopes": [],
        "ip_range": "192.168.1.30-192.168.1.55",
    },
}

data = {
    "admin": {
        "username": "admin",
        "name": "Admin",
        "password": "$pbkdf2-sha256$29000$l3KOca4VwjgHQIgRonTuHQ$KnbVsj0WzfobPHCgOBGxbk.zzsKZ6tFNs6EyYkH54Hg",
        "scopes": ["admin"],
        "ip_range": "*",
    },
    "user": {
        "username": "user",
        "name": "Normie",
        "password": "$pbkdf2-sha256$29000$AaB0DkForZXSWsu5l1KqFQ$mdeqw1D934VZorBW9aIQGXXqC/3FNinCE9O2Wda0b7Y",
        "scopes": [],
        "ip_range": "192.168.1.30-192.168.1.55",
    },
}

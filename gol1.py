import urllib.parse
import webbrowser


def main() -> None:
    base = "https://glife3.org/show/"
    params = {
        "glife": "Game of Life",
        "FW": 1200,
        "FH": 700,
        "LF": 80,
        "maxfps": 300,
    }

    url = base + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    print(url)
    webbrowser.open(url)


if __name__ == "__main__":
    main()


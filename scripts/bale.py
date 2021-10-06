import re
from base64 import b64encode
from pathlib import Path

import requests
from beartype import beartype
from bs4 import BeautifulSoup

from models import EconData, ImageLink, Unit


__cache_root = Path(__file__).parent / "../balesite"
__cache_root.mkdir(exist_ok=True)
__economics_url = "https://www.mistabale.com/economics"
__welcome_selector = "#comp-jyz8knnk"


@beartype
def get_econ_main_data(cached: bool=True) -> EconData:
    html = __get_site(__economics_url)
    return EconData(welcome=__get_main_welcome(html), units=__get_main_units(html))


@beartype
def __get_main_welcome(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for welcome_el in soup.select(__welcome_selector):
        return __correct_text(welcome_el.text)


@beartype
def __get_main_units(html: str) -> list[Unit]:
    htmls = __get_unit_htmls(html)
    for html in htmls:
        print(BeautifulSoup(html, "html.parser").text)
        print("\n\n")
    return []


@beartype
def __get_unit_htmls(html: str) -> list[str]:
    # FIXME extract to function
    htmls = []
    start = html.find("<h2")
    end = html.find("</h2", start + 1)
    while -1 not in {start, end}:
        htmls.append(html[start:end])
        start = html.find("<h2", end + 1)
        end = html.find("</h2", start + 1)

    # FIXME extract to function
    results = []
    buf = []
    for bloc in htmls:
        # FIXME this nesting is ugly jesus
        # FIXME do a better check for unit when you stop being lazy
        if "Unit" in bloc:
            if buf:
                results.append("\n".join(buf))
            buf = [bloc]
            continue
        if "Unit" in "".join(buf[:1]):
            buf.append(bloc)

    return [*results, "\n".join(buf)]


@beartype
def __correct_text(text: str) -> str:
    return text.replace("\xa0", "").replace("\u200b", "").strip()


@beartype
def __get_site(url: str, cached: bool=True) -> str:
    cache_file = __cache_root / b64encode(url.encode()).decode()
    if cached and cache_file.exists():
        return cache_file.read_text()
    r = requests.get(url)
    r.raise_for_status()
    if cached:
        cache_file.write_text(r.text)
    return r.text

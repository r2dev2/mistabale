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
def get_econ_main_data(cached: bool = True) -> EconData:
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
    return __separate_into_units(html, __get_mainpage_bloc_idxs(html))


@beartype
def __get_mainpage_bloc_idxs(html: str) -> list[tuple[int, int]]:
    res = []
    start = html.find("<h2")
    end = html.find("</h2", start + 1)
    while -1 not in {start, end}:
        res.append((start, end))
        start = html.find("<h2", end + 1)
        end = html.find("</h2", start + 1)
    return res


@beartype
def __separate_into_units(html: str, bloc_idxs: list[tuple[int, int]]) -> list[str]:
    res = []
    unit_start, unit_end = [-1] * 2
    for start, end in bloc_idxs:
        if "Unit" in html[start:end]:
            if -1 not in [unit_start, unit_end]:
                res.append(html[unit_start:unit_end])
            unit_start, unit_end = start, end
            continue
        if -1 not in [unit_start, unit_end]:
            unit_end = end
    return [*res, html[unit_start:unit_end]]


@beartype
def __correct_text(text: str) -> str:
    return text.replace("\xa0", "").replace("\u200b", "").strip()


@beartype
def __get_site(url: str, cached: bool = True) -> str:
    cache_file = __cache_root / b64encode(url.encode()).decode()
    if cached and cache_file.exists():
        return cache_file.read_text()
    r = requests.get(url)
    r.raise_for_status()
    if cached:
        cache_file.write_text(r.text)
    return r.text

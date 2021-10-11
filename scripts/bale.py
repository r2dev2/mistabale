import re
import warnings
from base64 import b64encode
from collections.abc import Iterable
from pathlib import Path
from typing import Iterable

import requests
from beartype import beartype
from bs4 import BeautifulSoup
from models import EconData, ImageLink, TextLink, Unit

warnings.filterwarnings("ignore")

__cache_root = Path(__file__).parent / "../balesite"
__cache_root.mkdir(exist_ok=True)
__economics_url = "https://www.mistabale.com/economics"
__welcome_selector = "#comp-jyz8knnk"
__img_link_selector = "a[data-testid=linkElement]"
__text_link_selector = "p a"
__unit_divider = re.compile(r"Unit \d")
__width_finder = re.compile(r"w_(\d+)")
__height_finder = re.compile(r"h_(\d+)")


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
    return [*map(__get_unit_from_html, __get_unit_htmls(html))]


@beartype
def __get_unit_from_html(html: str) -> Unit:
    soup = BeautifulSoup(html, "html.parser")
    return Unit(
        title=__correct_text(soup.find("h2").text),
        description=__correct_text(soup.find("p").text),
        resources=[*__get_img_links(soup)],
        documents=[*__get_text_links(soup)],
    )


@beartype
def __get_unit_htmls(html: str) -> list[str]:
    return [*__separate_into_units(html, __get_mainpage_bloc_idxs(html))]


@beartype
def __get_mainpage_bloc_idxs(html: str) -> Iterable[tuple[int, int]]:
    start = html.find("<h2")
    end = html.find("</h2", start + 1)
    while -1 not in {start, end}:
        yield (start, end)
        start = html.find("<h2", end + 1)
        end = html.find("</h2", start + 1)


@beartype
def __separate_into_units(
    html: str, bloc_idxs: Iterable[tuple[int, int]]
) -> Iterable[str]:
    unit_start = -1
    for start, end in bloc_idxs:
        if re.search(__unit_divider, html[start:end]):
            if unit_start != -1:
                yield html[unit_start:start]
            unit_start = start
    yield html[unit_start:end]


@beartype
def __get_img_links(soup: BeautifulSoup) -> Iterable[ImageLink]:
    for a in soup.select(__img_link_selector):
        yield ImageLink(url=a["href"], img_src=__increase_img_res(a.find("img")["src"]))


@beartype
def __get_text_links(soup: BeautifulSoup) -> Iterable[list[TextLink]]:
    return (
        [TextLink(url=a["href"], text=a.text) for a in p.select("a")]
        for p in soup.select("p")
        if p.select("a")
    )


@beartype
def __increase_img_res(src: str) -> str:
    *beg, query, name = src.split("/")
    _w, _h, *middle, _blur = query.split(",")
    width = int(re.search(__width_finder, query).group(1))
    height = int(re.search(__height_finder, query).group(1))
    new_w_q = "w_290"
    new_h_q = f"h_{int(290 * height / width)}"
    new_query = ",".join([new_w_q, new_h_q, *middle])
    return "/".join([*beg, new_query, name])


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

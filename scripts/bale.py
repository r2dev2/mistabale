from base64 import b64encode
from pathlib import Path

import requests
from beartype import beartype
from bs4 import BeautifulSoup

from models import EconData


__cache_root = Path(__file__).parent / "../balesite"
__cache_root.mkdir(exist_ok=True)
__economics_url = "https://www.mistabale.com/economics"
__welcome_selector = "#comp-jyz8knnk"


@beartype
def get_econ_main_data(cached: bool=True) -> EconData:
    html = __get_site(__economics_url)
    welcome = __get_main_welcome(html)
    return EconData(welcome=welcome, units=[])


@beartype
def __get_main_welcome(html: str) -> str:
    soup = BeautifulSoup(html)
    for welcome_el in soup.select(__welcome_selector):
        return __correct_text(welcome_el.text)


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

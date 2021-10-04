import base64
from pathlib import Path

import requests
from beartype import beartype

from models import EconData


__cache_root = Path(__file__).parent / "../balesite"
__cache_root.mkdir(exist_ok=True)
__economics_url = "https://www.mistabale.com/economics"



@beartype
def __get_site(url: str, cached: bool=True) -> str:
    cache_file = __cache_root / base64.b64encode(url)
    if cached and cache_file.exists():
        return cache_file.read_text()
    r = requests.get(url)
    r.raise_for_status()
    if cached:
        cache_file.write_text(r.text)
    return r.text

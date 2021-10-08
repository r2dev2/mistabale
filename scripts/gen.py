import shutil
from argparse import ArgumentParser
from pathlib import Path

from bale import get_econ_main_data
from render import render_econ_data, render_unit_page

dist = Path(__file__).parent / "../__dist__"
dist.mkdir(exist_ok=True)


def main() -> None:
    parser = ArgumentParser(
        "genbale", description="Generate usable website from mistabale's website"
    )
    parser.add_argument(
        "-c", "--cached", help="Use cached website", action="store_true"
    )
    args = parser.parse_args()

    data = get_econ_main_data(args.cached)

    with open(dist / "index.html", "w+") as fout:
        print(render_econ_data(data), file=fout)

    for i, unit in enumerate(data.units, 1):
        with open(dist / f"Unit-{i}.html", "w+") as fout:
            print(render_unit_page(unit), file=fout)

    shutil.copy(dist / "../index.css", dist / "index.css")


if __name__ == "__main__":
    main()

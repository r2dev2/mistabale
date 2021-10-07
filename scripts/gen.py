from argparse import ArgumentParser

from bale import get_econ_main_data


def main() -> None:
    parser = ArgumentParser(
        "genbale", description="Generate usable website from mistabale's website"
    )
    parser.add_argument(
        "-c", "--cached", help="Use cached website", action="store_true"
    )
    args = parser.parse_args()

    data = get_econ_main_data(args.cached)


if __name__ == "__main__":
    main()

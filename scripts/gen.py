from argparse import ArgumentParser

import bale


def main() -> None:
    parser = ArgumentParser("genbale", description="Generate usable website from mistabale's website")
    parser.add_argument("-c", "--cached", help="Use cached website", action="store_true")
    args = parser.parse_args()


if __name__ == "__main__":
    main()

# Mistabale

[A more user-friendly website](https://r2dev2.github.io/mistabale/) for https://www.mistabale.com/economics.

## Usage

| Action                | Command                                      |
|-----------------------|----------------------------------------------|
| Install dependencies  | `python3 -m pip install -r requirements.txt` |
| Generate website      | `python3 scripts/gen.py -c`                  |
| Format code           | `isort . && black .`                         |

## Development

I run the following commands in two shells to make development easier

1. `watch -n 1 python3 scripts/gen.py -c` (generates the website every second as a makeshift livereload)
2. `python3 -m http.server -d __dist__` (hosts the generated website at http://0.0.0.0:8000)

## Features

- [x] Parse and generate site for [main page](https://www.mistabale.com/economics)
- [ ] Superior bale cursor
- [ ] Parse and generate site for [quarterly reports](https://www.mistabale.com/quarterly-reports)
- [ ] Parse and generate site for [case studies](https://www.mistabale.com/case-studies)
- [ ] Parse and generate site for [case studies on the radio](https://www.mistabale.com/case-studies)
- [ ] Dark mode

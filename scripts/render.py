from typing import List

from beartype import beartype
from models import EconData, ImageLink, TextLink, Unit

__quartery_reports = "https://www.mistabale.com/quarterly-reports"
__case_studies = "https://www.mistabale.com/case-studies"


@beartype
def render_econ_data(data: EconData) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta charset="UTF-8">
    <title>Economics - Mistabale</title>
    <link rel="stylesheet" href="./index.css" />
    <link rel="prefetch" href="{__quartery_reports}" />
    <link rel="prefetch" href="{__case_studies}" />
    {"".join(f'<link rel="prefetch" href="./Unit-{i}.html" />' for i in range(1, len(data.units) + 1))}
</head>
<body>
    <h1>Economics - Mistabale</h1>
    <section>
        <h2>General</h2>
        <ul>
            <li><a href="{__quartery_reports}">Quarterly reports</a></li>
            <li><a href="{__case_studies}">Case studies</a></li>
        </ul>
    </section>
    <section>
        <h2>Units</h2>
        <ul>
        {"".join(f'<li><a href="./Unit-{i}.html">{unit.title}</a></li>' for i, unit in enumerate(data.units, 1))}
        </ul>
    </section>
</body>
</html>
"""


@beartype
def render_unit_page(unit: Unit) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta charset="UTF-8">
    <title>{unit.title} - Mistabale</title>
    <link rel="stylesheet" href="./index.css" />
</head>
<body>
    <h1>{unit.title}</h1>
    <p>{unit.description}</p>
    <section>
        <h2>Documents</h2>
        <ul id="documents">
            {"".join(map(render_text_links, unit.documents))}
        </ul>
    </section>
    <section>
        <h2>Resources</h2>
        <div id="resources">
            {"".join(map(render_img_link, unit.resources))}
        </div>
    </section>
</body>
</html>
"""


@beartype
def render_img_link(link: ImageLink) -> str:
    return f"""
<div class="resource">
    <a title="Open {link.url}" href="{link.url}"><img src="{link.img_src}" /></a>
</div>
"""


@beartype
def render_text_links(links: List[TextLink]) -> str:
    rendered_links = ",&nbsp;&nbsp;&nbsp;&nbsp;".join(
        f'<a href="{link.url}">{link.text}</a>' for link in links
    )
    return f"""
<li class="document">{rendered_links}</a></li>
"""

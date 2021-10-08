from models import EconData, ImageLink, TextLink, Unit


def render_econ_data(data: EconData) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Economics - Mistabale</title>
</head>
<body>
    <h1>Economics</h1>
    <h2>Units:</h2>
    <ul>
    {"".join(f'<li><a href="./Unit-{i}.html">{unit.title}</a></li>' for i, unit in enumerate(data.units, 1))}
    </ul>
</body>
</html>
"""


def render_unit_page(unit: Unit) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{unit.title} - Mistabale</title>
</head>
<body>
    <h1>{unit.title}</h1>
    <p>{unit.description}</p>
    <section>
        <h2>Resources</h2>
        <div class="resources">
            {"".join(map(render_img_link, unit.resources))}
        </div>
    </section>
    <section>
        <h2>Documents</h2>
        <ul class="documents">
            {"".join(map(render_text_link, unit.documents))}
        </div>
    </section>
</body>
</html>
"""


def render_img_link(link: ImageLink) -> str:
    return f"""
<div class="resource">
    <a href="{link.url}"><img src="{link.img_src}" /></a>
</div>
"""


def render_text_link(link: TextLink) -> str:
    return f"""
<li class="document"><a href="{link.url}">{link.text}</a></li>
"""

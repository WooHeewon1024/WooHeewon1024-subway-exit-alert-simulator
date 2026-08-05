"""Create a static GitHub Pages bundle from the Flask front-end files."""
from pathlib import Path
from shutil import copytree, rmtree

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site"

if OUTPUT.exists():
    rmtree(OUTPUT)
OUTPUT.mkdir()

html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
# Flask's template URLs become plain relative URLs in GitHub Pages.
html = html.replace("{{ url_for('static', filename='css/style.css') }}", "static/css/style.css")
html = html.replace("{{ url_for('static', filename='css/refinement.css') }}", "static/css/refinement.css")
html = html.replace("{{ url_for('static', filename='js/app.js') }}", "static/js/app.js")
html = html.replace('data-server-api="true"', 'data-server-api="false"')
(OUTPUT / "index.html").write_text(html, encoding="utf-8")
copytree(ROOT / "static", OUTPUT / "static")

from flask import Flask, render_template_string
import requests
import pandas as pd
import json

from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, HoverTool
from bokeh.embed import components
from bokeh.transform import linear_cmap
from bokeh.palettes import Inferno256

app = Flask(__name__)

@app.route("/")
def index():
    # 1. Datos COVID
    covid_data = requests.get("https://disease.sh/v3/covid-19/countries").json()
    df = pd.DataFrame(covid_data)

    # 2. GeoJSON Mundial
    geo_data = requests.get("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json").json()

    for feature in geo_data["features"]:
        iso3 = feature["id"]
        row = df[df["countryInfo"].apply(lambda x: x["iso3"] == iso3)]
        feature["properties"]["cases"] = int(row["cases"].values[0]) if not row.empty else 0

    geo_source = GeoJSONDataSource(geojson=json.dumps(geo_data))

    # 3. Crear mapa con estilo
    p = figure(
        title="🌍 COVID-19: Casos por País (Live API)",
        height=700,
        width=1100,
        x_axis_location=None,
        y_axis_location=None,
        toolbar_location="above",
        tools="pan,wheel_zoom,reset,hover",
        background_fill_color="#fff",
    )
    p.grid.grid_line_color = None

    mapper = linear_cmap("cases", Inferno256, 0, df["cases"].max())

    p.patches(
        "xs", "ys",
        source=geo_source,
        fill_color=mapper,
        line_color="white",
        line_width=0.25,
        fill_alpha=0.85,
    )

    # Hover
    p.add_tools(HoverTool(tooltips=[
        ("País", "@name"),
        ("Casos", "@cases"),
    ]))

    # 4. Exportar a HTML y mostrar en Flask
    script, div = components(p)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>COVID Map 3D Octavio</title>
        <style>
            body {{
                background-color: #121212;
                color: #eee;
                font-family: 'Segoe UI', sans-serif;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                font-size: 2.2rem;
                color: #f1c40f;
                margin-bottom: 20px;
            }}
            .bokeh-chart {{
                display: flex;
                justify-content: center;
            }}
        </style>
        <script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.4.1.min.js"></script>
        <link rel="stylesheet" href="https://cdn.bokeh.org/bokeh/release/bokeh-3.4.1.min.css" />
    </head>
    <body>
        <h1>🌐 Mapa Interactivo de Casos COVID-19</h1>
        <div class="bokeh-chart">{div}</div>
        {script}
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)

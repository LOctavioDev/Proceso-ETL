import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import dcc, html
import plotly.express as px

# ? Conexión a la base de datos
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5434/wikipedia")

# ? Cargar datos
query = "SELECT id, url, title, content FROM public.articles"
df = pd.read_sql(query, engine)

# ? Limpiar datos
df.dropna(subset=["title", "content"], inplace=True)
df["title"] = df["title"].str.strip()
df["content"] = df["content"].str.strip()
df = df[df["content"].str.len() > 500]
df["content_length"] = df["content"].apply(len)

# * HISTOGRAMA DE LA LONGITUD DEL CONTENIDO
fig_hist = px.histogram(
    df,
    x="content_length",
    nbins=50,
    title="Distribución de longitud del contenido",
    labels={"content_length": "Longitud del contenido (caracteres)"},
    template="plotly_white",
)

# * TOP 10 ARTICULOS CON EL CONTENIDO MAS LARGO
top10 = df.sort_values("content_length", ascending=False).head(10)
fig_bar = px.bar(
    top10,
    x="content_length",
    y="title",
    orientation="h",
    title="Top 10 artículos con contenido más largo",
    labels={"content_length": "Longitud del contenido (caracteres)", "title": "Título"},
    template="plotly_white",
    height=450,
)
fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})

# ! Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "900px",
        "margin": "30px auto",
        "padding": "20px",
        "backgroundColor": "#f9f9f9",
        "borderRadius": "8px",
        "boxShadow": "0 0 15px rgba(0,0,0,0.1)",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "marginBottom": "40px"},
            children=[
                html.H1("Análisis de Artículos Wikipedia", style={"color": "#2c3e50"}),
                html.P(
                    "Visualización interactiva de la longitud del contenido de artículos.",
                    style={"color": "#555", "fontSize": "18px"},
                ),
            ],
        ),
        dcc.Graph(figure=fig_hist, style={"height": "400px"}),
        dcc.Graph(figure=fig_bar, style={"height": "500px", "marginTop": "40px"}),
        html.Footer(
            style={
                "textAlign": "center",
                "marginTop": "50px",
                "color": "#999",
                "fontSize": "14px",
            },
            children="Proyecto de Visualización · Octavio 2025",
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)

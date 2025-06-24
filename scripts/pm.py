import dash
from dash import dcc, html, Input, Output
import pandas as pd
import pymongo
import plotly.express as px

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["clima"]
col = db["historico"]

# Cargar datos desde MongoDB
data = list(col.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Limpiar datos y eliminar ciudades vacías
df.dropna(subset=["ciudad"], inplace=True)
ciudades = df["ciudad"].dropna().unique()

# Inicializar Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Clima Histórico por Ciudad", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="ciudad-dropdown",
        options=[{"label": c, "value": c} for c in ciudades],
        value=ciudades[0],  
        style={"width": "300px", "margin": "0 auto"}
    ),

    dcc.Graph(id="grafica-clima", style={"marginTop": "30px"})
])


@app.callback(
    Output("grafica-clima", "figure"),
    Input("ciudad-dropdown", "value")
)
def actualizar_grafica(ciudad):
    df_ciudad = df[df["ciudad"] == ciudad]
    fig = px.line(
        df_ciudad,
        x="fecha",
        y=["temp_max", "temp_min"],
        title=f"Temperaturas Diarias - {ciudad}",
        labels={"value": "Temperatura (°C)", "variable": "Tipo"},
        template="plotly_dark"
    )
    fig.update_layout(xaxis_title="Fecha", yaxis_title="°C")
    return fig

if __name__ == "__main__":
    app.run(debug=True)

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime
import os

app = dash.Dash(__name__)
server = app.server

# Nom du fichier Excel
fichier_excel = "presences.xlsx"

# Initialiser le fichier Excel s'il n'existe pas
if not os.path.exists(fichier_excel):
    df_init = pd.DataFrame(columns=['Prénom', 'Nom', 'Horodatage'])
    df_init.to_excel(fichier_excel, index=False)

app.layout = html.Div([
    html.H2("Pointage de présence à l'événement"),
    dcc.Input(id='prenom', type='text', placeholder='Prénom', style={'margin': '10px'}),
    dcc.Input(id='nom', type='text', placeholder='Nom', style={'margin': '10px'}),
    html.Button('Signer la présence', id='submit', n_clicks=0),
    html.Div(id='confirmation')
])

@app.callback(
    Output('confirmation', 'children'),
    Input('submit', 'n_clicks'),
    State('prenom', 'value'),
    State('nom', 'value')
)
def enregistrer_presence(n_clicks, prenom, nom):
    if n_clicks > 0 and prenom and nom:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nouvelle_ligne = pd.DataFrame([[prenom, nom, timestamp]], columns=['Prénom', 'Nom', 'Horodatage'])
        
        # Charger l'existant, ajouter la nouvelle ligne, et enregistrer
        df_existante = pd.read_excel(fichier_excel)
        df_maj = pd.concat([df_existante, nouvelle_ligne], ignore_index=True)
        df_maj.to_excel(fichier_excel, index=False)
        
        return f"Merci {prenom} {nom}, votre présence est enregistrée !"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)

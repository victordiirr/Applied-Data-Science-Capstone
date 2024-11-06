# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                # Dropdown for Launch Site selection
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                # Slider de intervalo para selecionar o intervalo de payload (carga útil)
                                dcc.RangeSlider(
                                    id='payload-slider',           # Define o ID do componente para uso no callback
                                    min=0,                          # Valor mínimo do slider
                                    max=10000,                      # Valor máximo do slider
                                    step=1000,                      # Intervalo do slider (aumenta de 1000 em 1000)
                                    value=[min_payload, max_payload],  # Valor padrão do intervalo (carga útil mínima e máxima)
                                    marks={i: f'{i} Kg' for i in range(0, 10001, 2500)},  # Marcas no slider de 2500 em 2500 kg
                                    tooltip={"placement": "bottom", "always_visible": True}  # Mostra o valor do slider
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Definição da função de callback
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    # Verifica se a seleção é "ALL"
    if selected_site == 'ALL':
        # Cria um gráfico de pizza usando todos os dados para mostrar o total de lançamentos bem-sucedidos por site
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Successful Launches by Site')
    else:
        # Filtra o DataFrame para incluir apenas os dados do site selecionado
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Cria um gráfico de pizza para mostrar a contagem de sucesso (class=1) e falha (class=0) para o site selecionado
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success and Failure Launches for {selected_site}')
    # Retorna o gráfico de pizza atualizado
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Callback para atualizar o gráfico de dispersão com base no site selecionado e no intervalo de payload
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filtra o DataFrame com base no intervalo de payload
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    # Verifica se o usuário selecionou todos os sites ou um site específico
    if selected_site == 'ALL':
        # Cria um gráfico de dispersão para todos os sites com base no payload e na classe
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',  # Cor dos pontos baseada na versão do booster
                         title='Correlation between Payload and Success for all Sites')
    else:
        # Filtra o DataFrame para o site específico
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Cria um gráfico de dispersão para o site selecionado
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',  # Cor dos pontos baseada na versão do booster
                         title=f'Correlation between Payload and Success for site {selected_site}')
    
    # Retorna o gráfico atualizado
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8060)

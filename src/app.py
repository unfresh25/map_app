import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(
        __name__, 
        external_stylesheets=[dbc.themes.CYBORG], 
        title="Analisys of the Average Percentage of Bee Colonies Affected in the U.S.", 
        update_title=None
    )
server = app.server

df_u = pd.read_csv("https://raw.githubusercontent.com/lihkir/Uninorte/main/AppliedStatisticMS/DataVisualizationRPython/Lectures/Python/PythonDataSets/intro_bees.csv")

df = df_u.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

affected_by = df["Affected by"].unique()

affected_by_cod = {
    'Disease': 'Disease',
    'Other': 'Other',
    'Pesticides': 'Pesticides',
    'Pests_excl_Varroa': 'Pests other than Varroa',
    'Unknown': 'Unknown',
    'Varroa_mites': 'Verroa Destructor'
}

df2 = df_u.groupby(['State', 'Affected by', 'Year'])[['Pct of Colonies Impacted']].mean()
df2.reset_index(inplace=True)

States = df2["State"].unique()

bento_style = {
    "background-color": "rgb(17, 17, 17, 0.7)",
    "backdrop-filter": "blur(2px)",
    "border-radius": "0.75rem",
    "border-color": "rgba(0, 0, 0, 0.1)",
    "box-shadow": "0 0 0 1px rgba(255, 255, 255, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "max-height": "435px"
}

app.layout = html.Div([
    html.Header([
        html.Article([
            html.Span("Jorge Borja S."),
            html.Span("Visualización Científica"),
            html.Span("Maestría en Estadística Aplicada")
        ], style={"display": "flex", "flex-direction": "column"}),
        html.Img(src="https://www.uninorte.edu.co/o/uninorte-theme/images/uninorte/footer_un/logo.png", style={"height": "50px"})
    ], style={"display": "flex", "justify-content": "space-between", "align-items": "center"}),

    html.Hr(),

    html.H1("Average Percentage of Bee Colonies Affected in the United States Over Years", 
            style={
                'text-align': 'center', 
                'font-size': '25px', 
                "text-wrap": "pretty",
                "color": "#9f9f9f",
            }
        ),
    
    html.Br(),

    html.Nav([
        html.Article([
            dcc.Dropdown(
                id="slct_year",
                options=[
                    {"label": "2015", "value": 2015},
                    {"label": "2016", "value": 2016},
                    {"label": "2017", "value": 2017},
                    {"label": "2018", "value": 2018}],
                multi=False,
                value=2015,
                style={"color": "black", "background-color": "transparent", "border": "none", "border-bottom": "1px solid #5f5f5f"},
                placeholder="Select a year..."
            )
        ], style={"width": "20%"}),

        html.Article([
            dcc.Dropdown(
                id="affected-by",
                options=[{'label': v, 'value': k} for k, v in affected_by_cod.items()],
                value=affected_by[0],
                style={"color": "black", "background-color": "transparent", "border": "none", "border-bottom": "1px solid #5f5f5f"},
                multi=True,
                placeholder="Select a cause..."
            )
        ], style={"width": "30%"}),

        html.Article([
            dcc.Dropdown(
                id='by-states',
                options=[{'label': i, 'value': i} for i in States],
                multi=True,
                style={"color": "black", "background-color": "transparent", "border": "none", "border-bottom": "1px solid #5f5f5f"},
                placeholder="Select a state...",
                className="custom-dropdown"
            )
        ])
        
    ], style={"display": "flex", "justify-content": "flex-start", "gap": "15px"}),

    html.Hr(),

    html.Section([
        html.Article([
            dcc.Graph(id='my_bee_map', style={"width": "90%", "margin": "0 auto"})
        ], style={**bento_style, "grid-column": "span 10"}, className="bento1"),

        html.Article([            
            dcc.Graph(id='pie_graph')
        ], style={**bento_style, "grid-column": "span 10"}, className="bento2"),

        html.Article([
            dcc.Graph(id='line_graph', style={"width": "90%", "margin": "0 auto"})
        ], style={**bento_style, "grid-column": "span 10"}, className="bento3")

    ], style={"wdith": "100%", "max-width": "1400px",
              "display": "grid",
              "grid-template-columns": "repeat(10, minmax(0, 1fr))",
              "grid-auto-rows": "28rem",
              "gap": "1rem",
              "margin": "0 auto",
              "padding": "10px"}),

    html.Hr(),

    html.Footer([
        html.Article([
            html.Span("Powered by Plotly Dash"),
        ])
    ], style={"margin-bottom": "20px", "font-size": "15px"}),

    html.Br()    
    
], style={"height": "100vh", "margin": "0 auto", "padding": "50px", "width": "90%"})

state = ""

@app.callback(
    Output('my_bee_map', 'figure'),
    Output('by-states', "value"),
    Input('slct_year', 'value'),
    Input('affected-by', 'value'),
    Input('my_bee_map', "clickData"),
    Input('by-states', "value")
)
def update_map_graph_and_dropdown(option_slctd, affected_by, selected_state, by_states_drop):
    global state
    if selected_state is None:
        by_states = []
        by_states.append(States[0])
        by_states.append(States[1])
    else:
        if state != selected_state['points'][0]['customdata'][0]:
            state = selected_state['points'][0]['customdata'][0]
            by_states = by_states_drop + [state]
        else: 
            by_states = by_states_drop

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    if isinstance(affected_by, list):
        dff = dff[dff["Affected by"].isin(affected_by)]
    else:
        dff = dff[dff["Affected by"] == affected_by]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.Mint,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='none',
        title=f'Average % of Bee Colonies Affected in the U.S. in {option_slctd}',
    )

    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0.0)', geo=dict(bgcolor = 'rgba(0, 0, 0, 0.0)'))

    return fig, by_states

@app.callback(
    Output('line_graph', 'figure'),
    Input('affected-by', 'value'),
    Input('by-states', 'value')
)
def update_line_graph(affected_by, selected_states):
    line_fig = go.Figure()
    dff2 = df2.copy()

    if not isinstance(affected_by, list):
        affected_by = [affected_by]

    if selected_states:
        colors = px.colors.sequential.Mint_r
        color_index = 0
        for state in selected_states:
            for effect in affected_by:
                temp_df = dff2[(dff2['State'] == state) & (dff2['Affected by'] == effect)]
                line_fig.add_trace(go.Scatter(
                    x=temp_df['Year'],
                    y=temp_df['Pct of Colonies Impacted'],
                    mode='lines+markers',
                    name=f'{state}, {affected_by_cod[effect]}',
                    text=temp_df['Pct of Colonies Impacted'].round(2),
                    textposition='top center',
                    marker=dict(color=colors[color_index])
                ))
                color_index = (color_index + 1) % len(colors)

    selected_states_str = 'Comparison of Average % of Bee Colonies Affected Over Years'
    line_fig.update_layout(
        xaxis_title='Year',
        yaxis_title='% of Bee Colonies Impacted',
        title=selected_states_str,
        xaxis=dict(
            showgrid=False,
            showline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False
        ),
        template='none'
    )
    line_fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0.0)', plot_bgcolor = 'rgba(0, 0, 0, 0.0)')

    return line_fig

@app.callback(
    Output('pie_graph', 'figure'),
    Input('by-states', 'value'),
    Input('slct_year', 'value')
)
def update_pie_graph(selected_states, selected_year):
    pie_fig = go.Figure()
    dff2 = df2.copy()

    if selected_states:
        for state in selected_states:
            temp_df = dff2[(dff2['State'] == state) & (dff2['Year'] == selected_year)]
            temp_df.loc[:, 'Affected by'] = temp_df['Affected by'].map(affected_by_cod)
            pie_fig.add_trace(go.Pie(
                labels=temp_df['Affected by'],
                values=temp_df['Pct of Colonies Impacted'],
                hole=.4,
                name=state,
                textinfo='label+percent',
                textposition='inside',
                marker=dict(colors=px.colors.sequential.Mint)
            ))

    selected_states_str = f'Average % of Bee Colonies Affected in {selected_year}'
    pie_fig.update_layout(
        title=selected_states_str,
        template='none',
        showlegend=False,
    )

    pie_fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0.0)', plot_bgcolor = 'rgba(0, 0, 0, 0.0)')

    return pie_fig

if __name__ == '__main__':
    #app.run_server(debug=True, host='0.0.0.0', port=5000)
    app.run_server(debug=True)
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

app.layout = html.Div([
dbc.Row([
        html.H1("Search a number and set precision threshold"),
            ], justify="center", align="center"
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Slider(
                    id='slider_threshold',
                    min=0,
                    max=52,
                    step=1,
                    marks={"1": "Precision 1",
                           "12": "Precision 12",
                           "24": "Precision 24",
                           "36": "Precision 36",
                           "48": "Precision 48"},
                    value=24,
                ),
            ),
        ),
        dbc.Col(children=[dbc.FormGroup(
    [
        dbc.Label("Select Languages"),
        dbc.Checklist(
            options=[
                {"label": "Latin", "value": 1},
                {"label": "English", "value": 2},
            ],
            value=[],
            id="language-input",
            switch=True,
        ),
    ]
)

        ])
    ]),
    dbc.Row([
        dbc.Col(children=[
             dbc.Input(id="id_no", type="string"),
             html.H4("ID_No"),
                ]),
        dbc.Col([
            dbc.Button("submit_number", id="search-button"),
            ]),
            ]),

    html.Div(id='container-button-basic')
     ])
@app.callback(
    Output('container-button-basic','children'),
    [Input("search-button", 'n_clicks'),
    Input('slider_threshold', 'value'),
    Input("language-input", "value")],
    State('id_no', 'value')
)

def make_table(n_clicks, slid_val, langval, id_no):
    v = str(slid_val)
    if n_clicks is not None:
        print(langval)
        base = "https://imgur.com/gallery/{}"
        frame = pd.read_csv('data/separated.csv')
        titles = []
        links = []
        for i, row in frame.iterrows():
            titles.append(row['key'])
            hl= base.format(row['item'])
            links.append(html.A(html.P('Link'), href=hl))
        dictionary={"title":titles,"link":links}
        linkframe = pd.DataFrame(dictionary)
        fullframe = pd.merge(frame, linkframe, left_on='key', right_on='title')
        filterframe = fullframe[fullframe['score']>=int(slid_val)]
        outframe = filterframe[['key','link', 'item', 'text' ]]
        table=dbc.Table.from_dataframe(outframe, striped=True, bordered=True, hover=True)
        return table

        n_clicks == None
    else:
        return "Please input Data"


if __name__ == "__main__":
    app.run_server(debug=True)
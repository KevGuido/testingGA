from dash.dependencies import Input, Output, State
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv('assets/testing.csv')

app.layout = html.Div(
    [
        html.Div(
            className="row header",
            children=[
                html.Span(
                    className="app-title",
                    children=[
                        dcc.Markdown("**Client Data Center**"),
                        html.Span(
                            id="subtitle",
                            children=dcc.Markdown("&nbsp | assigment distribution"),
                            style={"font-size": "1.8rem", "margin-top": "15px"},
                        ),
                    ],
                ),
                html.Img(src=app.get_asset_url("LogoIBM.png")),
            ],
        ),
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Link("Business Unit & Department", href="/"),
                dcc.Link("Management", href="/"),
                dcc.Link("Location", href="/"),
            ],
        ),
        html.Div(
            id="mobile_tabs",
            className="row tabs",
            style={"display": "none"},
            children=[
                dcc.Link("Opportunities", href="/"),
                dcc.Link("Leads", href="/"),
                dcc.Link("Cases", href="/"),
            ],
        ),
        dash_table.DataTable(
            id='table-filtering-be',
            style_data={'height': 'auto'},
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            sort_action='native',
            sort_mode='multi',
            row_selectable='multi',
            row_deletable=True,
            sort_by=[],
            selected_rows=[],
            style_table={'height': '300px', 'minWidth': '100%', 'overflowY': 'auto'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'height': 'auto', },
            style_cell_conditional=[{'if': {'column_id': c}, 'backgroundColor': 'rgb(130, 130, 130)', 'color': 'white'}
                                    for
                                    c in ['Name', 'Admin']],
            style_cell={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'center',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white', 'fontSize': 12, 'font-family': 'sans-serif'},
            style_filter={'backgroundColor': 'rgb(130, 130, 130)', 'color': 'white'},
            style_header_conditional=[
                {'if': {'column_id': c}, 'backgroundColor': 'rgb(130, 130, 130)', 'color': 'white'}
                for c in ['Name', 'Admin']],
            filter_action='custom',
            filter_query='',
            export_format='xlsx',
            export_columns='visible',),

])
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-filtering-be', "data"),
    [Input('table-filtering-be', "filter_query")])
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True)

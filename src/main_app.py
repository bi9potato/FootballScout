# import
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import pandas as pd

import altair as alt
alt.data_transformers.disable_max_rows()

from Panel1 import get_panel1_content

# dataset
data_add = '../data/processed/all_players___.csv'
df = pd.read_csv(data_add, index_col=0)

## panel 1
min_year = df.league_season.min()
max_year = df.league_season.max()

league_name_id = {'Serie A': 135,
                   'La Liga': 140,
                   'Super League': 169,
                   'Premier League':39,
                   'Ligue 1': 61,
                   'Bundesliga': 78}
league_names = df.league_name.unique()
league_ids = [ i for i in league_name_id.values() ]

team_name_id = df.drop_duplicates(subset=['team_name', 'team_id'])[['team_name', 'team_id']].set_index('team_name')['team_id'].to_dict()
team_names = df.team_name.unique()
team_ids = [ i for i in team_name_id.values() ]


# dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([

    # Panels
    dbc.Tabs([


        # Panel1
        dbc.Tab([

            get_panel1_content()

        ], label='Panel1'),


        # Panel2
        dbc.Tab([


        ], label='Panel2'),


        # Panel3
        dbc.Tab([


        ], label='Panel3')

    ])

])


# Panel1
## dropdown2 need dropdown1 has a value firstly
@ app.callback(
    Output('p1_dd_team', 'options'),
    Input('p1_dd_league', 'value'),
)
def p1_dd_league_get_options(p1_dd_league_value):

    temp_league_ids = []
    if p1_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p1_dd_league_value]

    # df_selected = df.query(f'`league_id` == {p1_dd_league_value}')
    df_selected = df.query(f'`league_id`.isin(@temp_league_ids)')
    specified_teams = df_selected.team_name.unique()
    return [{'label': 'ALL', 'value': 'ALL' }] + [{'label': team_name, 'value': team_name_id[team_name]} for team_name in specified_teams]

## Panel1 - plot 1
@ app.callback(
Output('p1_Iframe_1', 'srcDoc'),
    Input('p1_rs_year', 'value'),
    Input('p1_dd_league', 'value'),
    Input('p1_dd_team', 'value'),
)
def draw_plot1(p1_rs_year_value, p1_dd_league_value, p1_dd_team_value):

    temp_league_ids = []
    if p1_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p1_dd_league_value]

    temp_team_ids = []
    if p1_dd_team_value == 'ALL':
        temp_team_ids = df.query(f'`league_id`.isin(@temp_league_ids)').team_id.unique().tolist()
    else:
        temp_team_ids = [p1_dd_team_value]

    years = [i for i in range(p1_rs_year_value[0], p1_rs_year_value[1]+1)]

    # df_selected = df.query(f'`team_id` == {p1_dd_team_value} & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years)')
    df_selected = df.query('`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years)')

    # get top 5 ids
    df_mean = df_selected.groupby('player_id').mean('games_rating').reset_index()
    top5_ids = df_mean.nlargest(5, 'games_rating')['player_id'].to_list()

    # get
    df_target = df_selected[df_selected['player_id'].isin(top5_ids)]

    chart1 = alt.Chart(df_target).encode(
        x=alt.X('league_season:N', title='Season'),
        y=alt.Y('games_rating:Q', scale=alt.Scale(zero=False), title='Game Rating'),
        color='player_name:N'
    ).mark_line().properties(title = 'Games Rating by Season and Player')

    return (chart1 + chart1.mark_circle() ).to_html()

## Panel1 - plot 2
@ app.callback(
Output('p1_Iframe_2', 'srcDoc'),
    Input('p1_rs_year', 'value'),
    Input('p1_dd_league', 'value'),
    Input('p1_dd_team', 'value'),
)
def draw_plot2(p1_rs_year_value, p1_dd_league_value, p1_dd_team_value):
    # pass

    # drop na
    # df_dropna = df[['games_rating', 'league_season']].dropna().reset_index(drop=True)
    df_dropna = df.dropna(subset=['games_rating', 'league_season'])

    # args
    years = [i for i in range(p1_rs_year_value[0], p1_rs_year_value[1])]

    temp_league_ids = []
    if p1_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p1_dd_league_value]

    temp_team_ids = []
    if p1_dd_team_value == 'ALL':
        temp_team_ids = df.query(f'`league_id`.isin(@temp_league_ids)').team_id.unique().tolist()
    else:
        temp_team_ids = [p1_dd_team_value]

    # df_selected = df_dropna.query('`league_season`.isin(@years)')
    df_selected = df_dropna.query('`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years)')

    chart2 = alt.Chart(df_selected).transform_density(
        'games_rating',
        as_=['games_rating', 'density']
    ).encode(
        x=alt.X('games_rating:Q', title='Game Rating'),
        y=alt.Y('density:Q', title='Density')
    ).mark_area().properties(title='Density Plot of Game Rating')

    return chart2.to_html()

## Panel1 - plot 3
@ app.callback(
    Output('p1_Iframe_3', 'srcDoc'),
    Input('p1_rs_year', 'value'),
    Input('p1_dd_league', 'value'),
    Input('p1_dd_team', 'value'),
)
def draw_plot2(p1_rs_year_value,p1_dd_league_value, p1_dd_team_value):
    # pass

    # drop na
    # df_dropna = df[['games_rating', 'league_season']].dropna().reset_index(drop=True)
    df_dropna = df.dropna(subset=['games_rating', 'league_season'])

    # args
    years = [i for i in range(p1_rs_year_value[0], p1_rs_year_value[1])]

    temp_league_ids = []
    if p1_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p1_dd_league_value]

    temp_team_ids = []
    if p1_dd_team_value == 'ALL':
        temp_team_ids = df.query(f'`league_id`.isin(@temp_league_ids)').team_id.unique().tolist()
    else:
        temp_team_ids = [p1_dd_team_value]


    # df_selected = df_dropna.query('`league_season`.isin(@years)')
    df_selected = df_dropna.query('`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years)')

    chart3 = alt.Chart(df_selected).encode(
        x=alt.X('games_rating:Q', bin=alt.Bin(maxbins=200), title='Game Rating'),
        y=alt.Y('count()', scale=alt.Scale(type='log'), title='Count')
    ).mark_bar().properties(title='Histogram of Game Rating')

    return chart3.to_html()

## Panel1 - plot 4
@ app.callback(
    Output('p1_Iframe_4', 'srcDoc'),
    Input('p1_rs_year', 'value'),
    Input('p1_dd_league', 'value'),
    Input('p1_dd_team', 'value'),
)
def draw_plot2(p1_rs_year_value, p1_dd_league_value, p1_dd_team_value):
    # pass

    # args
    years = [i for i in range(p1_rs_year_value[0], p1_rs_year_value[1])]

    temp_league_ids = []
    if p1_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p1_dd_league_value]

    temp_team_ids = []
    if p1_dd_team_value == 'ALL':
        temp_team_ids = df.query(f'`league_id`.isin(@temp_league_ids)').team_id.unique().tolist()
    else:
        temp_team_ids = [p1_dd_team_value]


    # df_selected = df.query('`league_season`.isin(@years)')
    df_selected = df.query('`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years)')

    chart4 = alt.Chart(df_selected).encode(
        y = alt.Y('league_season:N', title='League Season'),
        x = alt.X('games_rating:Q', scale=alt.Scale(zero=False), title='Game Rating')
    ).mark_boxplot().properties(title='Boxplot of Game Rating by Season')

    return chart4.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
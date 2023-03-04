# import
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import pandas as pd

import altair as alt
alt.data_transformers.disable_max_rows()

# dataset
data_add = './data/processed/all_players___.csv'
df = pd.read_csv(data_add, index_col=0)

## Panel 2
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

player_name_id = df.drop_duplicates(subset=['player_name', 'player_id'])[['player_name', 'player_id']].set_index('player_name')['player_id'].to_dict()
player_names = df.player_name.unique().tolist()
player_ids = [ i for i in player_name_id.values() ]

stats = [
    'games_appearences',
    'games_lineups',
    'games_minutes',
    'games_rating',
    'substitutes_in',
    'substitutes_out',
    'substitutes_bench',
    'shots_total',
    'shots_on',
    'goals_total',
    'goals_conceded',
    'goals_assists',
    'goals_saves',
    'passes_total',
    'passes_key',
    'passes_accuracy',
    'tackles_total',
    'tackles_blocks',
    'tackles_interceptions',
    'duels_total',
    'duels_won',
    'dribbles_attempts',
    'dribbles_success',
    'dribbles_past',
    'fouls_drawn',
    'fouls_committed',
    'cards_yellow',
    'cards_yellowred',
    'cards_red',
    'penalty_won',
    'penalty_commited',
    'penalty_scored',
    'penalty_missed',
    'penalty_saved',
    # 'player_age',
    'player_height',
    'player_weight',
]

# dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_panel2_content():
    return dbc.Container([

        dbc.Row([

            # sidebar
            dbc.Col([

                # # title
                # html.Div([
                #     html.P('Panel2')
                # ]),
                html.Br(),

                # slider
                html.Label('Year Range'),
                html.Div([
                    dcc.RangeSlider(
                        id='p2_rs_year',
                        min=min_year, max=max_year,
                        value=[min_year, max_year],
                        step=1,
                        marks={i: str(i) for i in range(min_year, max_year + 1)}
                    )
                ]),
                html.Br(),

                # dropdown
                html.Div([

                    # dd league
                    html.Label('League'),
                    dcc.Dropdown(
                        id='p2_dd_league',
                        options=[{'label': 'ALL', 'value': 'ALL'}] + [
                            {'label': league_name, 'value': league_name_id[league_name]} for league_name in
                            league_names],
                        value='ALL',
                        placeholder='Select one league...',
                        # multi=True

                    ),

                    # dd team
                    html.Label('Team'),
                    dcc.Dropdown(
                        id='p2_dd_team',
                        # options=[{'label': 'plz Choose league first', 'value': ''},],
                        value='ALL',
                        placeholder='Select one team...',
                        # multi=True
                    ),

                    # dd players
                    html.Label('Players'),
                    dcc.Dropdown(
                        id='p2_dd_player',
                        # value=['', ],
                        placeholder='Select players...',
                        multi=True,
                    ),

                ]),

            ], width=4),

            # plots
            dbc.Col([

                # plot 1-2
                dbc.Row([

                    # plot 1
                    dbc.Col([

                        # test2
                        # html.Div(
                        #     id = 'p2_test_Div',
                        #     children = 'p2_test_Div'
                        # ),

                        # dd status 1
                        dcc.Dropdown(
                            id='p2_dd_stat1',
                            options=[{'label': stat.replace('_', ' '), 'value': stat} for stat in stats],
                            value='games_rating',
                            placeholder='Select one stat...',
                            # multi=True,
                        ),

                        # plot 1
                        html.Iframe(
                            id='p2_Iframe_1',
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        ),
                    ]),

                    # plot 2
                    dbc.Col([

                        # dd status 1
                        dcc.Dropdown(
                            id='p2_dd_stat2',
                            options=[{'label': stat.replace('_', ' '), 'value': stat} for stat in stats],
                            value='shots_on',
                            placeholder='Select one stat...',
                            # multi=True,
                        ),

                        html.Iframe(
                            id='p2_Iframe_2',
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        ),
                    ]),

                ]),

                # plot 3-4
                dbc.Row([

                    # plot 3
                    dbc.Col([

                        # dd status 3
                        dcc.Dropdown(
                            id='p2_dd_stat3',
                            options=[{'label': stat.replace('_', ' '), 'value': stat} for stat in stats],
                            value='goals_total',
                            placeholder='Select one stat...',
                            # multi=True,
                        ),

                        # plot 3
                        html.Iframe(
                            id='p2_Iframe_3',
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        ),

                    ]),

                    # plot 4
                    dbc.Col([

                        # dd status 4
                        dcc.Dropdown(
                            id='p2_dd_stat4',
                            options=[{'label': stat.replace('_', ' '), 'value': stat} for stat in stats],
                            value='penalty_scored',
                            placeholder='Select one stat...',
                            # multi=True,
                        ),

                        # plot 4
                        html.Iframe(
                            id='p2_Iframe_4',
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        ),

                    ]),

                ])

            ])

        ])


    ])



app.layout = get_panel2_content()



# Panel2
## dropdown2 need dropdown1 has a value firstly
@ app.callback(
    Output('p2_dd_team', 'options'),
    Input('p2_dd_league', 'value'),
)
def p2_dd_league_get_options(p2_dd_league_value):

    temp_league_ids = []
    if p2_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p2_dd_league_value]

    # df_selected = df.query(f'`league_id` == {p1_dd_league_value}')
    df_selected = df.query(f'`league_id`.isin(@temp_league_ids)')
    specified_teams = df_selected.team_name.unique()
    return [{'label': 'ALL', 'value': 'ALL' }] + [{'label': team_name, 'value': team_name_id[team_name]} for team_name in specified_teams]

# Panel2 - dropdown3 need dropdown1 & dropdown2 have value firstly
@ app.callback(
    Output('p2_dd_player', 'options'),
    Input('p2_dd_league', 'value'),
    Input('p2_dd_team', 'value'),
)
def p2_dd_player_get_options(p2_dd_league_value, p2_dd_team_value ):

    temp_league_ids = []
    if p2_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p2_dd_league_value]

    temp_team_ids = []
    if p2_dd_team_value == 'ALL':
        temp_team_ids = team_ids
    else:
        temp_team_ids = [p2_dd_team_value]

    # df_selected = df.query(f'`league_id` == {p1_dd_league_value}')
    df_selected = df.query('`league_id`.isin(@temp_league_ids) & `team_id`.isin(@temp_team_ids) ')
    specified_players = df_selected.player_name.unique()
    return [{'label': player_name, 'value': player_name_id[player_name]} for player_name in specified_players]

# Panel2 - plots
@ app.callback(
    Output('p2_Iframe_1', 'srcDoc'),
    Output('p2_Iframe_2', 'srcDoc'),
    Output('p2_Iframe_3', 'srcDoc'),
    Output('p2_Iframe_4', 'srcDoc'),

    Input('p2_rs_year', 'value'),
    Input('p2_dd_league', 'value'),
    Input('p2_dd_team', 'value'),
    Input('p2_dd_player', 'value'),
    Input('p2_dd_stat1', 'value'),
    Input('p2_dd_stat2', 'value'),
    Input('p2_dd_stat3', 'value'),
    Input('p2_dd_stat4', 'value'),
)
def draw_p2_plots(p2_rs_year_value, p2_dd_league_value, p2_dd_team_value, p2_dd_player_value,
                  p2_dd_stat1_value, p2_dd_stat2_value, p2_dd_stat3_value, p2_dd_stat4_value):
    # pass
    # df['player_height'] = df['player_height'].str.replace(r'[^\d\.]+', '', regex=True)
    # df['player_weight'] = df['player_weight'].str.replace(r'[^\d\.]+', '', regex=True)
    # df['player_height'] = df['player_height'].astype(float)
    # df['player_weight'] = df['player_weight'].astype(float)

    # args
    years = [i for i in range(p2_rs_year_value[0], p2_rs_year_value[1]+1 )]

    temp_league_ids = []
    if p2_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p2_dd_league_value]

    temp_team_ids = []
    if p2_dd_team_value == 'ALL':
        temp_team_ids = df.query(f'`league_id`.isin(@temp_league_ids)').team_id.unique().tolist()
    else:
        temp_team_ids = [p2_dd_team_value]

    if not p2_dd_player_value:
        temp_player_ids = []
    else:
        temp_player_ids = p2_dd_player_value

    # plot 1
    y = p2_dd_stat1_value

    df_selected = df.query(
        '`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years) & `player_id`.isin(@temp_player_ids)')

    chart1 = alt.Chart(df_selected).encode(
        x=alt.X('league_season:N', title = 'League Season'),
        y=alt.Y( y + ':Q', scale=alt.Scale(zero=False), title=y.replace('_', ' ').title() ),
        color=alt.Color('player_name:N')
    ).mark_line().properties(title=y.replace('_', ' ').title() + ' by Season')

    # plot 2
    y = p2_dd_stat2_value

    df_selected = df.query(
        '`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years) & `player_id`.isin(@temp_player_ids)')

    chart2 = alt.Chart(df_selected).encode(
        x=alt.X('league_season:N', title = 'League Season'),
        y=alt.Y(y + ':Q', scale=alt.Scale(zero=False), title=y.replace('_', ' ').title() ),
        color=alt.Color('player_name:N')
    ).mark_line().properties(title=y.replace('_', ' ').title() + ' by Season')

    # plot 3
    y = p2_dd_stat3_value

    df_selected = df.query(
        '`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years) & `player_id`.isin(@temp_player_ids)')

    chart3 = alt.Chart(df_selected).encode(
        x=alt.X('league_season:N', title = 'League Season'),
        y=alt.Y(y + ':Q', scale=alt.Scale(zero=False), title=y.replace('_', ' ').title()),
        color=alt.Color('player_name:N')
    ).mark_line().properties(title=y.replace('_', ' ').title() + ' by Season')

    # plot 4
    y = p2_dd_stat4_value

    df_selected = df.query(
        '`team_id`.isin(@temp_team_ids) & `league_id`.isin(@temp_league_ids) & `league_season`.isin(@years) & `player_id`.isin(@temp_player_ids)')

    chart4 = alt.Chart(df_selected).encode(
        x=alt.X('league_season:N', title = 'League Season'),
        y=alt.Y(y + ':Q', scale=alt.Scale(zero=False), title=y.replace('_', ' ').title()),
        color=alt.Color('player_name:N')
    ).mark_line().properties(title=y.replace('_', ' ').title() + ' by Season')

    return chart1.to_html(), chart2.to_html(), chart3.to_html(), chart4.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
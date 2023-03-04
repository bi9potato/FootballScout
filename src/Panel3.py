# import
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import pandas as pd
import statsmodels.api as sm

import altair as alt
alt.data_transformers.disable_max_rows()

# dataset
data_add = './data/processed/all_players___.csv'
df = pd.read_csv(data_add, index_col=0)

## Panel 3
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

# dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_panel3_content():
    return dbc.Container([

        dbc.Row([

            # sidebar
            dbc.Col([

                # title
                # html.Div([
                #     html.P('Panel3')
                # ]),
                html.Br(),

                # dropdown
                html.Div([

                    # dd league
                    html.Label('League'),
                    dcc.Dropdown(
                        id='p3_dd_league',
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
                        id='p3_dd_team',
                        # options=[{'label': 'plz Choose league first', 'value': ''},],
                        value='ALL',
                        placeholder='Select one team...',
                        # multi=True
                    ),

                    # dd player
                    html.Label('Player'),
                    dcc.Dropdown(
                        id='p3_dd_player',
                        # value='J. Gillet',
                        placeholder='Select players...',
                        # multi=True,
                    ),

                ]),

            ], width=4),

            # plot
            dbc.Col([

                # plot 1
                html.Iframe(
                    id='p3_Iframe_1',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                ),

            ]),

        ])

    ])

app.layout = get_panel3_content()

# Panel3
## dropdown2 need dropdown1 has a value firstly
@ app.callback(
    Output('p3_dd_team', 'options'),
    Input('p3_dd_league', 'value'),
)
def p3_dd_league_get_options(p3_dd_league_value):

    temp_league_ids = []
    if p3_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p3_dd_league_value]

    # df_selected = df.query(f'`league_id` == {p1_dd_league_value}')
    df_selected = df.query(f'`league_id`.isin(@temp_league_ids)')
    specified_teams = df_selected.team_name.unique()
    return [{'label': 'ALL', 'value': 'ALL' }] + [{'label': team_name, 'value': team_name_id[team_name]} for team_name in specified_teams]

## Panel3 - dropdown3 need dropdown1 & dropdown2 have value firstly
@ app.callback(
    Output('p3_dd_player', 'options'),
    Input('p3_dd_league', 'value'),
    Input('p3_dd_team', 'value'),
)
def p3_dd_player_get_options(p3_dd_league_value, p3_dd_team_value ):

    temp_league_ids = []
    if p3_dd_league_value == 'ALL':
        temp_league_ids = league_ids
    else:
        temp_league_ids = [p3_dd_league_value]

    temp_team_ids = []
    if p3_dd_team_value == 'ALL':
        temp_team_ids = team_ids
    else:
        temp_team_ids = [p3_dd_team_value]

    df_selected = df[df['games_appearences'] != 0]
    df_selected.dropna(subset=['games_rating'], inplace=True)
    # 过滤得到有多个game_rating的人（删掉只有一个game_rating的人），因为只有一个数据不能预测
    df_selected = df_selected.groupby('player_id').filter(lambda x: len(x) > 1) # Filter out individuals with only one game_rating value (delete individuals with only one game_rating value), as a single data point is not enough for prediction.
    # 过滤出只有一个赛季只有一个game_rating的人（删掉只有一个赛季有多个game_rating的人），因为无法用它预测
    df_selected = df_selected.groupby(['player_id', 'league_season']).filter(lambda x: len(x) == 1)  # Filter out individuals with only one game_rating value in one season (delete individuals with multiple game_rating values in one season), as it is not possible to make predictions based on such data.

    # for column in df_selected.columns:
    #     df_selected[column] = df_selected[column].fillna(0)

    df_selected = df_selected.query('`league_id`.isin(@temp_league_ids) & `team_id`.isin(@temp_team_ids)')
    specified_players = df_selected.player_name.unique()

    return [{'label': player_name, 'value': player_name_id[player_name]} for player_name in specified_players]

## Panel3 - plot
@ app.callback(
    Output('p3_Iframe_1', 'srcDoc'),
    Input('p3_dd_player', 'value'),
)
def p3_draw_plots(p3_dd_player_value):

    df_selected = df[df['games_appearences'] != 0]
    df_selected.dropna(subset=['games_rating'], inplace=True)
    # df_selected = df_selected.groupby('player_id').filter(lambda x: len(x) > 1)  # 删掉只有一个game——rating的人，因为无法用它预测

    if not p3_dd_player_value:
        return None
    else:
        df_selected = df_selected.query(f'`player_id`=={p3_dd_player_value}')

        df_pred = df_selected[['league_season', 'games_rating']]

        X = df_pred.loc[:, ['league_season']]
        X = sm.add_constant(X)
        y = df_pred.loc[:, ['games_rating']]
        model = sm.OLS(y, X).fit()
        # model_summary = model.summary()

        params = model.params.tolist()
        interplate = params[0]
        beta1 = params[1]

        games_rating = interplate + beta1 * (df_selected.league_season.max() + 1)
        new_row = {'league_season': df_selected.league_season.max() + 1, 'games_rating': games_rating}
        df_pred = df_pred.append(new_row, ignore_index=True)

        chart1 = alt.Chart(df_pred).encode(
            x=alt.X('league_season:N', title='League Season'),
            y=alt.Y('games_rating:Q', scale=alt.Scale(zero=False), title='Games Rating')
        ).mark_line().properties(title = "Prediction of the following year's Games Rating")

        return chart1.to_html()




if __name__ == '__main__':
    app.run_server(debug = True)
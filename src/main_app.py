# import
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import pandas as pd
import statsmodels.api as sm

import altair as alt
alt.data_transformers.disable_max_rows()

from Panel1 import get_panel1_content
from Panel2 import get_panel2_content
from Panel3 import get_panel3_content


# dataset
data_add = '../data/processed/all_players___.csv'
df = pd.read_csv(data_add, index_col=0)


## Panel 3
## Panel 2
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

server = app.server


app.layout = dbc.Container([

    # Panels
    dbc.Tabs([


        # Panel1
        dbc.Tab([


            get_panel1_content()


        ], label='Panel1'),


        # Panel2
        dbc.Tab([

            get_panel2_content()


        ], label='Panel2'),


        # Panel3
        dbc.Tab([


            get_panel3_content()


        ], label='Panel3')

    ])

])


# Panel3
# dropdown2 need dropdown1 has a value firstly
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

    return [{'label': 'ALL', 'value': 'ALL'}] + [{'label': team_name, 'value': team_name_id[team_name]} for team_name in specified_teams]


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
    df_selected = df_selected.groupby('player_id').filter(lambda x: len(x) > 1)  # Filter out individuals with only one game_rating value (delete individuals with only one game_rating value), as a single data point is not enough for prediction.
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
# import
import dash

import dash_bootstrap_components as dbc


# dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([

    # Panels
    dbc.Tabs([


        # Panel1
        dbc.Tab([

        ], label='Panel1'),


        # Panel2
        dbc.Tab([

        ], label='Panel2'),


        # Panel3
        dbc.Tab([

        ], label='Panel3')

    ])

])




if __name__ == '__main__':
    app.run_server(debug=True)
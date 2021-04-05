import sqlite3
import plotly.graph_objects as go
import pandas as pd
import copy
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------
#Connect to sqlite database
conn = sqlite3.connect("THT.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
#Turn State database graph info into a pandas dataframe object
cur.execute('''SELECT State.state, State.car_perc, State.miles_per_cap,
    State.seat_belt_perc, State.road_fatalities, State.dui_fatalities,
    Abbreviation.name FROM State JOIN Abbreviation ON State.abbreviation_id =
    Abbreviation.id''')
#print(cur.fetchall())

df0 = pd.read_sql('''SELECT State.state, State.car_perc, State.miles_per_cap,
    State.seat_belt_perc, State.road_fatalities, State.dui_fatalities,
    Abbreviation.name FROM State JOIN Abbreviation ON State.abbreviation_id =
    Abbreviation.id''', conn)

for col in df0.columns:
    df0[col] = df0[col].astype(str)
#-------------------------------------------------------------------------------
# Turn Metro database graph info into a pandas dataframe object
cur.execute('''SELECT distinct(Metropolitan_Statistica_Area.name),
    Metropolitan_Statistica_Area.latitude, Metropolitan_Statistica_Area.longitude,
    Metropolitan_Statistica_Area.vehicle_perc, Metropolitan_Statistica_Area.public_perc,
    Metropolitan_Statistica_Area.auto_fatality, Metropolitan_Statistica_Area.bike_perc,
    Metropolitan_Statistica_Area.bike_fatality, Metropolitan_Statistica_Area.pedestrian_perc,
    Metropolitan_Statistica_Area.ped_fatality, Street.complete_street
    FROM Metropolitan_Statistica_Area JOIN Street ON
    Metropolitan_Statistica_Area.street_id = Street.id''')

df1 = pd.read_sql('''SELECT distinct(Metropolitan_Statistica_Area.name),
    Metropolitan_Statistica_Area.latitude, Metropolitan_Statistica_Area.longitude,
     Metropolitan_Statistica_Area.vehicle_perc, Metropolitan_Statistica_Area.public_perc,
     Metropolitan_Statistica_Area.auto_fatality, Metropolitan_Statistica_Area.bike_perc,
     Metropolitan_Statistica_Area.bike_fatality, Metropolitan_Statistica_Area.pedestrian_perc,
     Metropolitan_Statistica_Area.ped_fatality, Street.complete_street
     FROM Metropolitan_Statistica_Area JOIN Street ON
     Metropolitan_Statistica_Area.street_id = Street.id''', conn)
#-------------------------------------------------------------------------------
# Turn Urban database graph info into a pandas dataframe object
cur.execute('''SELECT distinct(name), transit_trips, miles_per_cap, latitude,
    longitude FROM Urbanized_Area GROUP BY name ORDER BY transit_trips DESC''')

df2 = pd.read_sql('''SELECT distinct(name), transit_trips, miles_per_cap, latitude,
    longitude FROM Urbanized_Area GROUP BY name ORDER BY transit_trips DESC''', conn)
#-------------------------------------------------------------------------------
# Close sqlite database connection
conn.close()

df_dic = {'df0': df0, 'df1': df1, 'df2': df2}
#-------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Transportation Health Tool (THT) Dashboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_area",
                options= [
                {"label": "State data", "value": 0},
                {"label": "Metropolitan Statistica Area", "value": 1},
                {"label": "Urbanized Area", "value": 2}],
                multi=False,
                value= 0,
                style={'width': "40%"}
                ),


    html.Div(id='output_container', children=[]), #children=[] doesn't need to be typed for working program

    dcc.Graph(id='THT_graph', figure={}), #figure={} doesn't need to be typed for working program

    # html.Link(href="www.google.com")
    ])

#-------------------------------------------------------------------------------
# Connect with Plotly graphs with the Dash Component

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='THT_graph', component_property='figure')],
    [Input(component_id='slct_area', component_property='value')]
)


def update_graph(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))

    container = ""

    dff = df_dic.copy()
    # print(dff['df0'])


    if option_slctd == 0:
#-------------------------------------------------------------------------------
# Set up/execute State graph
        df0 = dff['df0']
        df0['text'] = df0['state'] + '<br>' + \
            'Commute by Car: ' + df0['car_perc'] + "%" + '<br>' + \
            'Seat Belt Usage: ' + df0['seat_belt_perc']+ '%' +'<br>' + \
            'Road Traffic Fatalities: ' + '<br>' + \
            'Auto Fatality (per 100,000): ' + df0['road_fatalities'] + '<br>' + \
            'DUI/DWI Fatality (per 10,000): ' + df0['dui_fatalities']

        fig = go.Figure(data=go.Choropleth(
            locations=df0['name'],
            z=df0['miles_per_cap'], #data to be color coded
            locationmode='USA-states',
            colorscale='Blues',
            autocolorscale=False,
            text=df0['text'], # hover text
            marker_line_color='white', # line markers between states
            colorbar_title="Miles Per Capita"
        ))

        fig.update_layout(
            title_text = 'Miles Driven by State <br>(Hover for more information)',
            geo_scope='usa', # limite map scope to USA
            annotations = [dict(
                x=0,
                y=0,
                xref='paper',
                yref='paper',
                text='Source:<a href="https://catalog.data.gov/dataset/transportation-and-health-tool-data">\
                    Transportation and Health Tool</a>',
                showarrow = False
            )]
        )

        return container, fig
#-------------------------------------------------------------------------------
# Set up/ execute Metro data
    if option_slctd == 1:
        df1 = dff['df1']

        df1['text'] = df1['name'] + '<br>' + \
            'Complete Streets Policy: ' + df1['complete_street'].astype(str) + '<br>' + \
            'Commute by Mode:' + '<br>' + \
            'Vehicle: ' + df1['vehicle_perc'].astype(str) + '%' + '<br>' + \
            'Public Transportation: ' + df1['public_perc'].astype(str) + '%' + '<br>' + \
            'Biking: ' + df1['bike_perc'].astype(str) + '%' + '<br>' + \
            'Walking: ' + df1['pedestrian_perc'].astype(str) + '%' + '<br>' + \
            'Traffic Fatalities per 100,000 Residents: ' + '<br>' + \
            'Auto Fatalities: ' + df1['auto_fatality'].astype(str) + '<br>' + \
            'Bike Fatalities: ' + df1['bike_fatality'].astype(str) + '<br>' + \
            'Pedestrian Fatalities: ' + df1['ped_fatality'].astype(str)


        fig = go.Figure(data=go.Scattergeo(
                lon = df1['longitude'],
                lat = df1['latitude'],
                text = df1['text'],
                mode = 'markers',
        #next line will color code markers based on street id
                #marker_color = df['street_id'],
                ))

        fig.update_layout(
                title = 'Transportation Data by Metropolitan Statistica Area<br>(Hover for more information)',
                geo_scope='usa',
                annotations = [dict(
                    x=0,
                    y=0,
                    xref='paper',
                    yref='paper',
                    text='Source:<a href="https://catalog.data.gov/dataset/transportation-and-health-tool-data">\
                        Transportation and Health Tool</a>',
                    showarrow = False
                )]
            )
        return container, fig
#-------------------------------------------------------------------------------
# Set up/execute Urban graph
    if option_slctd == 2:
        df2 = dff['df2']

        df2['text'] = df2['name'] + '<br>Transit Trips Per Capita: ' + df2['transit_trips'].astype(str) + '<br>Miles Per Capita: ' +  df2['miles_per_cap'].astype(str)
        limits = [(0,5),(6,15),(16,50),(51, 100),(101, 500)]
        colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
        cities = []
        scale = 1.25

        fig = go.Figure()

        for i in range(len(limits)):
            lim = limits[i]
            df_sub = df2[lim[0]:lim[1]]
            # print(df_sub)
            fig.add_trace(go.Scattergeo(
                locationmode = 'USA-states',
                lon = df_sub['longitude'],
                lat = df_sub['latitude'],
                text = df_sub['text'],
                marker = dict(
                    size = df_sub['transit_trips'] ** scale,
                    color = colors[i],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode = 'area'
                ),
                name = '{0} - {1}'.format(lim[0],lim[1])))

        fig.update_layout(
                title_text = 'Transit Trips per Capita by Urbanized Area<br>(Hover for more information or click legend to toggle fewer values)',
                showlegend = True,
                geo = dict(
                    scope = 'usa',
                    landcolor = 'rgb(217, 217, 217)',
                ),
                annotations = [dict(
                    x=0,
                    y=0,
                    xref='paper',
                    yref='paper',
                    text='Source:<a href="https://catalog.data.gov/dataset/transportation-and-health-tool-data">\
                        Transportation and Health Tool</a>',
                    showarrow = False
                )]
            )
        return container, fig
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)

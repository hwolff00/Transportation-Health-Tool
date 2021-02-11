import plotly.graph_objects as go
import sqlite3
import pandas as pd

#-------------------------------------------------------------------------------
conn = sqlite3.connect("state.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
#Turn select parts of database into a pandas object
cur.execute('''SELECT state, state_abv, miles_per_capita, road_traffic_fatalities,
    commute_by_car_percent, seat_belt_percent, dui_fatalities FROM Road_data''')

df= pd.read_sql('''SELECT state, state_abv, miles_per_capita, road_traffic_fatalities,
    commute_by_car_percent, seat_belt_percent, dui_fatalities FROM Road_data''', conn)

for col in df.columns:
    df[col] = df[col].astype(str)
    #print(df['state'])
#-------------------------------------------------------------------------------
#Set up the parameters of the graph
df['text'] = df['state'] + '<br>' + \
    'Commute by Car: ' + df['commute_by_car_percent'] + "%" + '<br>' + \
    'Seat Belt Usage: ' + df['seat_belt_percent']+ '%' +'<br>' + \
    'Road Traffic Fatalities: ' + '<br>' + \
    'Auto Fatality (per 100,000): ' + df['road_traffic_fatalities'] + '<br>' + \
    'DUI/DWI Fatality (per 10,000): ' + df['dui_fatalities']

fig = go.Figure(data=go.Choropleth(
    locations=df['state_abv'],
    z=df['miles_per_capita'], #data to be color coded
    locationmode='USA-states',
    colorscale='Blues',
    autocolorscale=False,
    text=df['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Miles Per Capita"
))
#-------------------------------------------------------------------------------
fig.update_layout(
    title_text = 'Miles Driven by State <br>(Hover for other information)',
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
#-------------------------------------------------------------------------------
#Launch graph in browser
fig.show()
conn.close()

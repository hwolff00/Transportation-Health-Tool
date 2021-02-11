
import sqlite3
import pandas as pd
import plotly.graph_objects as go

#-------------------------------------------------------------------------------
#Connect to
conn = sqlite3.connect("metro.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
#Turn sqlite database into a pandas dataframe object
cur.execute('''SELECT Metro_Area.area, Street.complete_street,
    Metro_Area.street_id, Metro_Area.latitude, Metro_Area.longitude,
    Metro_Area.vehicle_perc, Metro_Area.public_perc, Metro_Area.auto_fatality,
    Metro_Area.bike_perc, Metro_Area.bike_fatality, Metro_Area.pedestrian_perc,
    Metro_Area.ped_fatality
    FROM Metro_Area JOIN Street ON Metro_Area.street_id = Street.id''')
#print(cur.fetchall())

df = pd.read_sql('''SELECT Metro_Area.area, Street.complete_street,
    Metro_Area.street_id, Metro_Area.latitude, Metro_Area.longitude,
    Metro_Area.vehicle_perc, Metro_Area.public_perc, Metro_Area.auto_fatality,
    Metro_Area.bike_perc, Metro_Area.bike_fatality, Metro_Area.pedestrian_perc,
    Metro_Area.ped_fatality
    FROM Metro_Area JOIN Street ON Metro_Area.street_id = Street.id''', conn)
# #-------------------------------------------------------------------------------
#Set up the parameters of the graph

df['text'] = df['area'] + '<br>' + \
    'Complete Streets Policy: ' + df['complete_street'].astype(str) + '<br>' + \
    'Commute by Mode:' + '<br>' + \
    'Vehicle: ' + df['vehicle_perc'].astype(str) + '%' + '<br>' + \
    'Public Transportation: ' + df['public_perc'].astype(str) + '%' + '<br>' + \
    'Biking: ' + df['bike_perc'].astype(str) + '%' + '<br>' + \
    'Walking: ' + df['pedestrian_perc'].astype(str) + '%' + '<br>' + \
    'Traffic Fatalities per 100,000 Residents: ' + '<br>' + \
    'Auto Fatalities: ' + df['auto_fatality'].astype(str) + '<br>' + \
    'Bike Fatalities: ' + df['bike_fatality'].astype(str) + '<br>' + \
    'Pedestrian Fatalities: ' + df['ped_fatality'].astype(str)


fig = go.Figure(data=go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['text'],
        mode = 'markers',
#next line will color code markers based on street id
        #marker_color = df['street_id'],
        ))
#-------------------------------------------------------------------------------
fig.update_layout(
        title = 'Metro Area Transportation Numbers<br>(Hover for more info)',
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
#-------------------------------------------------------------------------------
fig.show()
conn.close()

import xlrd
import sqlite3
import geopy
from geopy.geocoders import Nominatim
import abbreviations

#-------------------------------------------------------------------------------
# Add in Abbreviations table if not exists
abbreviations.add_abbreviations()
#-------------------------------------------------------------------------------
# Connect to and open the database file
conn = sqlite3.connect("THT.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
# Set up database tables
cur.executescript('''
    DROP TABLE IF EXISTS Urbanized_Area;

    CREATE TABLE Urbanized_Area(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name TEXT,
    transit_trips INTEGER,
    miles_per_cap INTEGER,
    latitude INTEGER,
    longitude INTEGER,
    abbreviation_id INTEGER
    );

''')
#-------------------------------------------------------------------------------
# Create function that will clean certain data
def cleanup(x):
    str_x = str(x)[:5]
    y = float(str_x)
    return y
#-------------------------------------------------------------------------------
# Collect and clean the data
loc = ("THT_Data_508.xlsx")

# Open workbook and set up index[1] worksheet as object sheet
workbook = xlrd.open_workbook(loc)
sheet = workbook.sheet_by_index(2)

# Iterate through the rows of the worksheet
for row in range(sheet.nrows):
#skip over headers row
    if row != 0:
        city = sheet.cell_value(row, 0)
        if city != "[no data]" and city != 'Richmond, VA' and city!= 'Washington, DC-VA-MD': #Nominatim doesn't correctly map Richmond
                c = city.split(',')
                address = "{},{}".format(c[0], c[1][:3])
                abbrev_lst = c[1].strip().split("-")
# Place in lat, long coordinates using geopy
                try:
                    add = Nominatim(user_agent='THT_data').geocode(address)
                    lat = add.latitude
                    long = add.longitude
                except:
                    continue
                if sheet.cell_value(row, 1) == "[no data]":
                    continue
                else:
                    t = sheet.cell_value(row, 1)
                    trips = cleanup(t)
                if sheet.cell_value(row, 3) == "[no data]":
                    continue
                else:
                    m = sheet.cell_value(row, 3)
                    miles = cleanup(m)
# Sanity/data check
                print(address, lat, long, trips, miles)
#-------------------------------------------------------------------------------
# Insert the data into database (still in above loop)
                for abbrev in abbrev_lst:

                    cur.execute('SELECT id FROM Abbreviation WHERE name = ? ', (abbrev, ))
                    abb = cur.fetchone()[0]

                    cur.execute('''INSERT OR REPLACE INTO Urbanized_Area
                        (name, transit_trips, miles_per_cap, latitude,
                        longitude, abbreviation_id ) VALUES
                        ( ?, ?, ?, ?, ?, ?)''',
                        ( city, trips, miles, lat, long, abb)
                        )
# #-------------------------------------------------------------------------------
# # Save the database file (still in above loops)
                    conn.commit()
conn.close()

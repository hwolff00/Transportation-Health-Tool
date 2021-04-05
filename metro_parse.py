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
    DROP TABLE IF EXISTS Street;
    DROP TABLE IF EXISTS Metropolitan_Statistica_Area;

    CREATE TABLE Street(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    complete_street TEXT UNIQUE
    );

    CREATE TABLE  Metropolitan_Statistica_Area(
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    name TEXT,
    latitude INTEGER,
    longitude INTEGER,
    vehicle_perc INTEGER,
    public_perc INTEGER,
    auto_fatality INTEGER,
    bike_perc INTEGER,
    bike_fatality INTEGER,
    pedestrian_perc INTEGER,
    ped_fatality INTEGER,
    abbreviation_id INTEGER,
    street_id  INTEGER
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
sheet = workbook.sheet_by_index(1)

# Iterate through the rows of the worksheet
for row in range(sheet.nrows):
#skip over headers row
    if row != 0:
        metro = sheet.cell_value(row, 0)
        if metro != "[no data]" and metro != "Richmond, VA" and metro!= 'Washington-Arlington-Alexandria, DC-VA-MD-WV':
            # Nominatim doesn't like Richmond, and DC doesn't have a spot in the state abb
                met = metro.split(',')
                address = "{},{}".format(met[0], met[1][:3])
                abbrev_lst = met[1].strip().split("-")
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
                    veh = sheet.cell_value(row, 1) * 100
                    vehicle = cleanup(veh)
                if sheet.cell_value(row, 3) == "[no data]":
                    continue
                else:
                    pu = sheet.cell_value(row, 3) * 100
                    pub = cleanup(pu)
                if sheet.cell_value(row, 5) == "[no data]":
                    continue
                else:
                    bi = sheet.cell_value(row, 5) * 100
                    bike = cleanup(bi)
                if sheet.cell_value(row, 7) == "[no data]":
                    continue
                else:
                    pe = sheet.cell_value(row, 7) * 100
                    ped = cleanup(pe)
                if sheet.cell_value(row, 9) == "[no data]":
                    continue
                else:
                    streets = sheet.cell_value(row, 9)
                if sheet.cell_value(row, 19) == "[no data]":
                    continue
                else:
                    afate = sheet.cell_value(row, 19)
                    auto_fate = cleanup(afate)
                if sheet.cell_value(row, 21) == "[no data]":
                    continue
                else:
                    bfate = sheet.cell_value(row, 21)
                    bike_fate = cleanup(bfate)
                if sheet.cell_value(row, 23) == "[no data]":
                    continue
                else:
                    pfate = sheet.cell_value(row, 23)
                    ped_fate = cleanup(pfate)
# Sanity/data check
                print(vehicle, lat, long)
#-------------------------------------------------------------------------------
# Insert the data into database (still in above loop)
                for abbrev in abbrev_lst:
                    cur.execute('''INSERT OR IGNORE INTO Street (complete_street)
                        VALUES ( ? )''', ( streets, ) )

                    cur.execute('SELECT id FROM Street WHERE complete_street = ? ', (streets, ))
                    street_id = cur.fetchone()[0]

                    cur.execute('SELECT id FROM Abbreviation WHERE name = ? ', (abbrev, ))
                    abb = cur.fetchone()[0]

                    cur.execute('''INSERT OR REPLACE INTO Metropolitan_Statistica_Area
                        (name, latitude, longitude, vehicle_perc, public_perc,
                        auto_fatality, bike_perc, bike_fatality, pedestrian_perc,
                        ped_fatality, abbreviation_id, street_id ) VALUES
                        ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        ( metro, lat, long, vehicle, pub, auto_fate, bike,
                        bike_fate, ped, ped_fate, abb, street_id )
                        )
#-------------------------------------------------------------------------------
# Save the database file (still in above loops)
                    conn.commit()
conn.close()

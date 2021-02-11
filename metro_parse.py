import xlrd
import sqlite3
import geopy
from geopy.geocoders import Nominatim

#-------------------------------------------------------------------------------
#Connect to and open the database file
conn = sqlite3.connect("metro.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
#Set up database tables
cur.executescript('''
    DROP TABLE IF EXISTS Street;
    DROP TABLE IF EXISTS Metro_Area;

    CREATE TABLE Street(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    complete_street TEXT UNIQUE
    );

    CREATE TABLE Metro_Area(
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    area TEXT UNIQUE,
    street_id  INTEGER,
    latitude INTEGER,
    longitude INTEGER,
    vehicle_perc INTEGER,
    public_perc INTEGER,
    auto_fatality INTEGER,
    bike_perc INTEGER,
    bike_fatality INTEGER,
    pedestrian_perc INTEGER,
    ped_fatality INTEGER
    );

''')
#-------------------------------------------------------------------------------
#Collect and clean the data
loc = ("THT_Data_508.xlsx")

# Open workbook and set up index[1] worksheet as object sheet
workbook = xlrd.open_workbook(loc)
sheet = workbook.sheet_by_index(1)

#Iterate through the rows of the worksheet
for row in range(sheet.nrows):
#skip over headers row
    if row != 0:
        metro = sheet.cell_value(row, 0)
        if metro != "[no data]":
                met = metro.split(',')
                address = "{},{}".format(met[0], met[1][:3])
#Place in lat, long coordinates using geopy
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
                    str_veh = str(veh)[:5]
                    vehicle = float(str_veh)
                if sheet.cell_value(row, 3) == "[no data]":
                    continue
                else:
                    pu = sheet.cell_value(row, 3) * 100
                    str_pub = str(pu)[:5]
                    pub = float(str_pub)
                if sheet.cell_value(row, 5) == "[no data]":
                    continue
                else:
                    bi = sheet.cell_value(row, 5) * 100
                    str_bike = str(bi)[:5]
                    bike = float(str_bike)
                if sheet.cell_value(row, 7) == "[no data]":
                    continue
                else:
                    pe = sheet.cell_value(row, 7) * 100
                    str_ped = str(pe)[:5]
                    ped = float(str_ped)
                if sheet.cell_value(row, 9) == "[no data]":
                    continue
                else:
                    streets = sheet.cell_value(row, 9)
                if sheet.cell_value(row, 19) == "[no data]":
                    continue
                else:
                    afate = sheet.cell_value(row, 19)
                    str_afate = str(afate)[:5]
                    auto_fate = float(str_afate)
                if sheet.cell_value(row, 21) == "[no data]":
                    continue
                else:
                    bfate = sheet.cell_value(row, 21)
                    str_bfate = str(bfate)[:5]
                    bike_fate = float(str_bfate)
                if sheet.cell_value(row, 23) == "[no data]":
                    continue
                else:
                    pfate = sheet.cell_value(row, 23)
                    str_pfate = str(pfate)[:5]
                    ped_fate = float(str_pfate)
#Sanity/data check
                print(address, lat, long)
#-------------------------------------------------------------------------------
#Insert the data into database (still in above loop)
                cur.execute('''INSERT OR IGNORE INTO Street (complete_street)
                    VALUES ( ? )''', ( streets, ) )

                cur.execute('SELECT id FROM Street WHERE complete_street = ? ', (streets, ))
                street_id = cur.fetchone()[0]

                cur.execute('''INSERT OR REPLACE INTO Metro_Area
                    (area, street_id, vehicle_perc, latitude, longitude,
                    public_perc, auto_fatality, bike_perc, bike_fatality,
                    pedestrian_perc, ped_fatality ) VALUES
                    ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    ( metro, street_id, vehicle, lat, long, pub, auto_fate, bike,
                    bike_fate, ped, ped_fate )
                    )
#-------------------------------------------------------------------------------
#Save the database file (still in above loop)
                conn.commit()
conn.close()

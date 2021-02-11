import sqlite3
import xlrd

#-------------------------------------------------------------------------------
#Connect/open the database
conn = sqlite3.connect("state.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
#Create the table for our data
cur.executescript("""
DROP TABLE IF EXISTS Road_data;

CREATE TABLE Road_data (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    state TEXT UNIQUE,
    state_abv TEXT UNIQUE,
    commute_by_car_percent INTEGER,
    miles_per_capita INTEGER,
    seat_belt_percent INTEGER,
    road_traffic_fatalities INTEGER,
    dui_fatalities INTEGER
 );

""")
#-------------------------------------------------------------------------------
#Hard coding way to enter in state ids w/o altering original xlsx
code_lst = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR",
    "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
#-------------------------------------------------------------------------------
loc = ("THT_Data_508.xlsx")
#Parse through and lightly clean workbook data and add in state ids
workbook = xlrd.open_workbook(loc)
sheet = workbook.sheet_by_index(0)
x = 0
for row in range(sheet.nrows):
#Ignore headers row
    if row != 0:
        states = sheet.cell_value(row, 0)
        state_id = code_lst[x]
        x +=1
        int_commute = sheet.cell_value(row, 1) *100
        commute = str(int_commute)[:5]
        int_seat_belt = sheet.cell_value(row, 33) *100
        belt = str(int_seat_belt)[:5]
        capita = sheet.cell_value(row, 39)
        cap = str(capita)[:8]
        int_roadfate = sheet.cell_value(row, 21)
        roadfate = str(int_roadfate)[:4]
        int_dui = sheet.cell_value(row, 11)
        dui = str(int_dui)[:4]

#Insert the data into the new database
        cur.execute('''INSERT OR IGNORE INTO Road_data
            (state, state_abv, commute_by_car_percent, miles_per_capita,
            seat_belt_percent, road_traffic_fatalities, dui_fatalities )
            VALUES ( ?, ?, ?, ?, ?, ?, ?)''',
            (states, state_id, commute, cap, belt, roadfate, dui ) )
#-------------------------------------------------------------------------------
#Commit/Save database
conn.commit()

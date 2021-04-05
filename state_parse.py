import sqlite3
import xlrd
import abbreviations

#-------------------------------------------------------------------------------
# Add in Abbreviations table if not exists
abbreviations.add_abbreviations()
#-------------------------------------------------------------------------------
# Connect/open the database
conn = sqlite3.connect("THT.sqlite")
cur = conn.cursor()
#-------------------------------------------------------------------------------
# Create the table for our data
cur.executescript("""
DROP TABLE IF EXISTS State;

CREATE TABLE State (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    state TEXT UNIQUE,
    car_perc INTEGER,
    miles_per_cap INTEGER,
    seat_belt_perc INTEGER,
    road_fatalities INTEGER,
    dui_fatalities INTEGER,
    abbreviation_id INTEGER
 );

""")
#-------------------------------------------------------------------------------
abbrev_lst = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR",
    "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
#-------------------------------------------------------------------------------
loc = ("THT_Data_508.xlsx")
# Parse through and lightly clean workbook data and add in state ids
workbook = xlrd.open_workbook(loc)
sheet = workbook.sheet_by_index(0)
x = 0
for row in range(sheet.nrows):
# Ignore headers row
    if row != 0:
        states = sheet.cell_value(row, 0)
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
        abbrev = abbrev_lst[x]
        x += 1

# Insert the data into the new database
        cur.execute('SELECT id FROM Abbreviation WHERE name = ? ', (abbrev, ))
        abb = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO State
            (state, car_perc, miles_per_cap,
            seat_belt_perc, road_fatalities, dui_fatalities, abbreviation_id)
            VALUES ( ?, ?, ?, ?, ?, ?, ?)''',
            (states, commute, cap, belt, roadfate, dui, abb) )
#-------------------------------------------------------------------------------
# Commit/Save database
        conn.commit()
conn.close()

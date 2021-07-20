import sqlite3

abbrev_lst = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
              "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI",
              "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
              "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
              "VT", "VA", "WA", "WV", "WI", "WY"]


def add_abbreviations():
    conn = sqlite3.connect("THT.sqlite")
    cur = conn.cursor()

    cur.executescript('''
        CREATE TABLE IF NOT EXISTS Abbreviation(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        name TEXT UNIQUE
        );''')

    for abbrev in abbrev_lst:
        # print(abbrev)
        cur.execute('''INSERT OR IGNORE INTO Abbreviation (name)
            VALUES ( ? )''', (abbrev, ))

        conn.commit()
    conn.close()


if __name__ == "__main__":
    add_abbreviations()

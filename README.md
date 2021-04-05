# Transportation-Health-Tool 

Used to analyze a Transportation and Health Tool (THT) xlsx worksheet and visualize
the data in a dropdown Dash dashboard, using a Chloropleth Map, Scatterplot Map, and a Bubble Map.

This is a set of tools to help better understand sections of the metadata at:

https://catalog.data.gov/dataset/transportation-and-health-tool-data

A copy of the information xlsx file is also on this repository as 'THT_Data_508.xlsx'.

According to the website:

"The Transportation and Health Tool (THT) was developed by the U.S. Department
of Transportation and the Centers for Disease Control and Prevention to provide
easy access to data that practitioners can use to examine the health impacts of
transportation systems. The tool provides data on a set of transportation and
public health indicators for each U.S. state and metropolitan area that describe
how the transportation environment affects safety, active transportation, air
quality, and connectivity to destinations. You can use the tool to quickly see
how your state or metropolitan area compares with others in addressing key
transportation and health issues. It also provides information and resources
to help agencies better understand the links between transportation and health
and to identify strategies to improve public health through transportation
planning and policy."

This project has three data aspects: State Data, Metropolitan Statistica Area Data, and Urbanized Area Data.

1.) State Data

State Data includes:

"Commute Mode Share: the percentage of workers aged 16 years and over who commute
either
  1. by bicycle
  2. by private vehicle, including car, truck, van, taxicab, and motorcycle
  3. by public transportation, including bus, rail, and ferry
  4. by foot
 Data on commute mode share come from the 2012 one-year estimates from the
 American Community Survey (ACS))"
 
"Complete Streets Policies:
The Complete Streets Policies indicator provides information on whether or not
a state or the metropolitan planning organization that serves the region or a 
given metro area has adopted a complete streets policy that requires or encourages 
a safe, comfortable, integrated transportation network for all users, regardless of 
age, ability, income, ethnicity, or mode of transportation. Data come from the 
National Complete Streets Coalition’s list of complete streets policies. A score of 
either 0 (no policy) or 100 (policy in place) is provided for this indicator."

"Seat Belt Use:
Seat belt use measures the percentage of drivers and front-seat passengers that wear 
seat belts. Data come from the National Highway Traffic Safety Administration (NHTSA) 
Seat Belt Use in 2012—Use Rates in the States and Territories report."

"Person Miles Traveled by Mode:
Person miles traveled by mode measures the amount that the average person either 
  1) walks in a year or 
  2) drives in a year in private vehicles, including cars, vans, sport utility vehicles, 
  pickup tricks, taxicabs, other trucks, recreational vehicles, motorcycles, and light 
  electric vehicles such as golf carts. Data come from the 2009 National Household Travel 
  Survey (NHTS). If more than one person travels together on a trip, each person is 
  considered as making one person trip with associated person miles traveled."

"Road Traffic Fatalities by Mode:
Road traffic fatalities by mode measures the rate of fatalities from traffic collisions 
involving of 
  1) a driver or passenger in a vehicle that is either moving or parked, 
  2) a bicyclist, or 
  3) a pedestrian. 
Data on fatalities come from the National Highway Traffic Safety Administration (NHTSA) 
Fatality Analysis Reporting System (FARS).  The THT uses a 5-year average of data from 
2008-2012. Population data come from the 2008-2012 American Community Survey (ACS) 5-year 
estimates."

"Alcohol-Impared Fatalities:
The alcohol-impaired fatalities indicator measures the rate of fatal traffic 
crashes that involve a driver who is impaired by alcohol. Alcohol-impaired 
driving is defined by National Highway Traffic Safety Administration (NHTSA) 
as the number of fatalities from vehicle crashes involving a person with a 
blood alcohol concentration (BAC) of at least 0.08 g/dL. “Driver”’ refers to 
the operator of any motor vehicle and fatalities can be those of the driver, 
occupant, or non-occupant. Data on fatalities come from the 2012 Fatality 
Analysis Reporting System (FARS). Population data come from the 2012 American 
Community Survey (ACS) 1-year estimates."

'state_parse.py' retrieves and filters information from the THT_Data_508.xlsx worksheet[0]
(State) section, and after cleaning it, writes it to a SQLite database. If not already 
executed, the 'abbreviation.py' will insert an "Abbreviations" join table to the database
during 'state_parse.py execution.


2.)Metropolitan Statistica Area Data

For Metro Data, the information used includes:

"Complete Streets Policies:
The Complete Streets Policies indicator provides information on whether or not
a state or the metropolitan planning organization that serves the region or a
given metro area has adopted a complete streets policy that requires or
encourages a safe, comfortable, integrated transportation network for all users,
regardless of age, ability, income, ethnicity, or mode of transportation. Data
come from the National Complete Streets Coalition’s list of complete streets
policies. A score of either 0 (no policy) or 100 (policy in place) is provided
for this indicator."

"Commute Mode Share: the percentage of workers aged 16 years and over who commute
either
  1. by bicycle
  2. by private vehicle, including car, truck, van, taxicab, and motorcycle
  3. by public transportation, including bus, rail, and ferry
  4. by foot
 Data on commute mode share come from the 2012 one-year estimates from the
 American Community Survey (ACS))"

"Road Traffic Fatalities:
Raw value data of Road Traffic Fatalities per 100,000 Residents either
  1. by bicycle
  2. by automobile
  3. by foot"

'metro_parse.py' pulls the desired information from the THT_Data_508.xlsx worksheet[1]
(Metropolitan Statistica Area) section, and turns it into a SQLite database. Using the
geopy library, latitude and longitude coordinates for each metro area are also inserted
into the SQLite database. If not already executed, the 'abbreviation.py' will insert an 
"Abbreviations" join table to the database during 'metro_parse.py execution.

3.) Urbanized Area Data

Vehicle Miles Traveled Per Capita:
"Vehicle miles traveled (VMT) per capita is calculated as the total annual miles of 
vehicle travel divided by the total population in a state or in an urbanized area. Data 
for this indicator come from the Federal Highway Administration (FHWA), 2011 Highway 
Statistics. The reports are based on individual state reports on traffic data counts 
collected through permanent automatic traffic recorders on public roadways. Data on VMT 
for urbanized areas are available from the FHWA Highway Statistics Series. These data are 
calculated as the total daily miles of vehicle travel in an urbanized area divided by the 
total population. An urbanized area is defined as an area with 50,000 persons that at a 
minimum encompasses the land area delineated as the urbanized area by the U.S. Census Bureau."

Public Transportation Trips Per Capita:
"This indicator measures the average number of public transportation trips that a resident 
takes per year in a given state or urbanized area. Data for this indicator come from the 2013 
American Public Transit Association (APTA) Public Transportation Fact Book, which uses 2011 
data from the National Transit Database."

'state_parse.py' pulls, filters, and cleans data from the THT_Data_508.xlsx worksheet[2]
(Urbanized Area) section, and turns it into a SQLite database. Using the
geopy library, latitude and longitude coordinates for each urbanized area are also inserted
into the SQLite database. If not already executed, the 'abbreviation.py' will include an 
"Abbreviations" join table to the database during 'urban_parse.py execution.

A schema for the final database is saved in this repository as "THT.jpeg" and a copy of the
SQLite database is saved as 'THT.sqlite'.

In order to view and modify the database, you should install the SQLite browser
from:

http://sqlitebrowser.org/

"dash_graph.py" uses Dash as a framework to create a web analytics app from the THT
data. First it queries the "THT.sqlite" database and turns it into a Pandas dataframe.
It then uses Plotly's Open Source Graphing Libray to create three seperate map graphs:
State data is converted to a cholorpleth map colored by vehicles driven per capita,
Metropolitan Statistica Area data is converted to a scatterplot map, and Urbanized Area
data is converted to a bubble map sized by the amount of public transportation trips per
capita.

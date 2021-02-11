# Transportation-Health-Tool 

Used to analyze a Transportation and Health Tool (THT) xlsx worksheet and visualizing
the data.

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

This project has two aspects currently: the State Data and the Metro Data.


1.) State Data includes:

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

'state_parse.py' pulls the desired information from the THT_Data_508.xlsx worksheet[0]
(State) section, and turns it into a SQLite database. In the process, it also adds 
in the state codes to help graph the information in 'state_graphy.py'.

A copy of the final SQLite database is saved in this repository as 'state.sqlite'.

In order to view and modify the database, you should install the SQLite browser
from:

http://sqlitebrowser.org/

'state_graph.py' turns the SQLite database into a Pandas dataframe, and then uses
plotly to create a chloropleth map of the data. When the script is ran, the graph
will appear in the brower, with the states colored by vehicles driven per capita.


2.)Metro Data:

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
geopy library, it also pulls in the latitude and longitude coordinates for each metro
area and add this information into the SQLite database, along with the xlsx worksheet
data.

A copy of the final database is saved on this repository as 'metro.sqlite'.

'metro_graph.py' takes the information from the 'metro.sqlite' database and turns it
into a Pandas dataframe. It then uses the Plotly graphing library to turn the dataframe
into a scatter plot on map. Running the script will cause this graph to appear in the
browser.

# London Tube

# Introduction - 

This application will determine the quickest path between two London Tube stations. Initially, there were three csv files with data for all the stations, as well as links between stations and which line they were on.


# Working of Application - 
1. All the rows of csv files are fetched and stored against three lists using the static method "importData" of class CSV.
2. The "convertStringToInt" and "convertStringToFloat" methods are used to convert the values into integer and float.
3. Using “hub_id” as a matching property, data from the stations and connections lists is merged in the "master data" list.
4. A dictionary “all_stations” is initialised and modified such that all the objects of Station class are stored in it against tuple(station_id, line_id).
5. Another dictionary “all_connections” is initialised and modified such that all the objects of Connection class are stores in it against “connection_id”.
6. Establishing a connection between “all_stations” and “all_connections” by filling neighbours and connection attributes of station objects.
7. A dictionary “hubs” is declared and modified such that each key represents a unique hub i.e. station_id and its value represents a tuple of station_id and line_id.
8. After all these as soon as user enter some value in “Source” and “Destination” station and clicks “Get Time” button “findRoute” method of class Graph is called. On GUI a pop-up message will come showing time required to travel from source to destination.
9. Input values are checked against all the station names present in CSV file using “checkInputs” static method of class Graph. Appropriate message is displayed if input values are not correct.
10. Dijkstra algorithm is applied to get the fasted route and minimum time between start and end stations.
11. Second pop-up message comes and asks user if they are interested in seeing graph for the route. As soon as user clicks “Yes” graph showing route between source and destination is displayed. If user is not interested in seeing graph and clicks “No” then program will terminate.

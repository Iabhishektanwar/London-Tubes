import csv
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkinter import *


class Station:
    def __init__(self, name, hub_id, station_id, latitude, longitude):
        self.name = name
        self.hub_id = hub_id  # Station ID
        self.station_id = station_id  # Tuple(Station ID, Line ID)
        self.latitude = latitude
        self.longitude = longitude
        self.time = False
        self.neighbours = []  # station_id
        self.connections = []  # connection_id


class Connection:
    def __init__(self, connection_id, station1, station2, time, line):
        self.connection_id = connection_id
        self.station1 = station1
        self.station2 = station2
        self.time = time
        self.line = line
        self.coordinates = None


class Graph:
    def __init__(self):
        self.all_stations = all_stations
        self.all_connections = all_connections

    def getStation(self, station_id):
        """
        Returns an object of class Station which is stored against station_id key in all_stations dictionary.
        """
        return self.all_stations[station_id]

    def getCoordinates(self, connection, from_id):
        """
        Returns the coordinates of two adjacent stations.
        """
        s1 = self.getStation(connection.station1)
        s2 = self.getStation(connection.station2)  # type Station
        if from_id == s1.station_id:
            connection.coordinates = {'lat_from': s1.latitude, 'long_from': s1.longitude, 'lat_to': s2.latitude,
                                      'long_to': s2.longitude}
        if from_id == s2.station_id:
            connection.coordinates = {'lat_from': s2.latitude, 'long_from': s2.longitude, 'lat_to': s1.latitude,
                                      'long_to': s1.longitude}
        return connection.coordinates

    def getConnectionBetween(self, station1, station2):
        """
        Returns connection between station1 and station2.
        """
        if station1.station_id not in station2.neighbours:
            message = 'No direct link between given stations.'
            messagebox.showinfo("showinfo", message)
            return
        else:
            for connection_id in station1.connections:
                connection = self.all_connections[connection_id]
                if station2.station_id in [connection.station2, connection.station1] and station1.station_id in \
                        [connection.station2, connection.station1]:
                    return connection

    @staticmethod
    def checkInputs(station_name):
        """
        Validates whether name provided by user is present in stations or not.
        """
        for station_info in stations:
            if station_info['name'].lower() == station_name.lower():
                return 1
        return 0

    def findRoute(self, start, end):  # Dijkstra algorithm implementation to navigate the London tube Network
        """
        Returns the fastest route and time between start to end station.
        ---------------------------------------------------------------------------
        1. Transverse stations and check the input provided by user
        ===========================================================================
        2. Input is converted into corresponding stations:
        
        """

        global next_station
        try:
            if Graph.checkInputs(start):
                starting_station_id = int(CSV.getStationIdFromName(start))  # 198
                for station_id in self.all_stations:
                    if station_id[0] == starting_station_id:
                        start = self.getStation(station_id)
                        break
            else:
                message = 'Source station does not exist. Please enter a valid station name.'
                messagebox.showinfo("showinfo", message)
                return message
            if Graph.checkInputs(end):
                ending_station_id = int(CSV.getStationIdFromName(end))
                for station_id in self.all_stations:
                    if station_id[0] == ending_station_id:
                        end = self.getStation(station_id)
                        break
            else:
                message = 'Destination station does not exist. Please enter a valid station name.'
                messagebox.showinfo("showinfo", message)
                return message

            unvisited_stations = dict([(station_hub_id, 1000) for (station_hub_id, time) in self.all_stations.items()])
            # Queue containing all the stations where initial time for all the stations is set to 100 minutes.
            unvisited_stations[start.station_id] = 0  # Setting time of start station to 0
            time = []  # Empty List whose last element will hold total time between two stations.
            current = start
            routes = {current.station_id: [{'name': current.name, 'station_id': current.station_id}]}

            """
            3. Traverse all Stations:
            """
            while not end.time:

                for neighbour_id in current.neighbours:
                    neighbour = self.getStation(neighbour_id)
                    connection_to_neighbour = self.getConnectionBetween(current, neighbour)  # []

                    # Store the quickest path to each time station in a dict called Routes.
                    if neighbour.station_id in unvisited_stations:
                        if unvisited_stations[neighbour.station_id] > (
                                unvisited_stations[current.station_id] + connection_to_neighbour.time):
                            unvisited_stations[neighbour.station_id] = unvisited_stations[
                                                                  current.station_id] + connection_to_neighbour.time
                            routes[neighbour.station_id] = routes[current.station_id][:]
                            routes[neighbour.station_id].append(
                                {"name": neighbour.name, 'station_id': neighbour.station_id})

                # Close the loop by changing current to ensure visited station is not visited again.
                current.time = True
                time.append(unvisited_stations.pop(current.station_id))
                for station_id, overall_time in unvisited_stations.items():
                    if overall_time == min(unvisited_stations.values()):
                        next_station = station_id
                current = self.getStation(next_station)

            def plot_route(route):
                """
                Plot the graph between start and end station by using stations stored in route dictionary.
                """
                try:
                    coordinates_limits = dict(
                        zip(['min_lat', 'max_lat', 'min_long', 'max_long'], [1000, -1000, 1000, -1000]))
                    latest_line_colour = None
                    getLineColour = lambda line_id: '#999999' if line_id is None else str(
                        '#' + lines[line_id]['colour'])
                    getLineName = lambda line_id: None if line_id is None else str(lines[line_id]['name'])
                    ax = plt.subplot()
                    for r in range(1,
                                   len(route)):  # Loop through a list of dictionaries, one for each station on the
                        # selected route
                        station1 = self.getStation(route[r - 1]['station_id'])
                        station2 = self.getStation(route[r]['station_id'])
                        connection = self.getConnectionBetween(station1, station2)
                        self.getCoordinates(connection, station1.station_id)

                        if True:
                            if connection.coordinates['lat_from'] > coordinates_limits['max_lat']:
                                coordinates_limits['max_lat'] = connection.coordinates['lat_from']
                            if connection.coordinates['lat_from'] < coordinates_limits['min_lat']:
                                coordinates_limits['min_lat'] = connection.coordinates['lat_from']
                            if connection.coordinates['long_from'] > coordinates_limits['max_long']:
                                coordinates_limits['max_long'] = connection.coordinates['long_from']
                            if connection.coordinates['long_from'] < coordinates_limits['min_long']:
                                coordinates_limits['min_long'] = connection.coordinates['long_from']
                            if connection.coordinates['lat_to'] > coordinates_limits['max_lat']:
                                coordinates_limits['max_lat'] = connection.coordinates['lat_to']
                            if connection.coordinates['lat_to'] < coordinates_limits['min_lat']:
                                coordinates_limits['min_lat'] = connection.coordinates['lat_to']
                            if connection.coordinates['long_to'] > coordinates_limits['max_long']:
                                coordinates_limits['max_long'] = connection.coordinates['long_to']
                            if connection.coordinates['long_to'] < coordinates_limits['min_long']:
                                coordinates_limits['min_long'] = connection.coordinates['long_to']

                        line_colour = getLineColour(connection.line)
                        if line_colour == latest_line_colour:
                            line_name = None
                        else:
                            line_name = getLineName(connection.line)
                        latest_line_colour = line_colour
                        plt.plot([connection.coordinates['long_from'], connection.coordinates['long_to']],
                                 [connection.coordinates['lat_from'], connection.coordinates['lat_to']], marker='o',
                                 linestyle='--',
                                 color=line_colour, label=line_name)

                        ax.annotate(station1.name,
                                    xy=(connection.coordinates['long_from'], connection.coordinates['lat_from']),
                                    xytext=(
                                        connection.coordinates['long_from'] + 0.002,
                                        connection.coordinates['lat_from'] - 0.002))

                        ax.annotate(station2.name,
                                    xy=(connection.coordinates['long_to'], connection.coordinates['lat_to']),
                                    xytext=(
                                        connection.coordinates['long_to'] + 0.002,
                                        connection.coordinates['lat_to'] - 0.002))

                    ax.set_xticks(
                        [-0.60, -0.55, -0.50, -0.45, -0.40, -0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05,
                         0.10,
                         0.15, 0.20])

                    ax.set_yticks([51.40, 51.45, 51.50, 51.55, 51.60, 51.65, 51.70])
                    ax.set_xlim((coordinates_limits['min_long'] - 0.02), (coordinates_limits['max_long'] + 0.02))
                    ax.set_ylim((coordinates_limits['min_lat'] - 0.02), (coordinates_limits['max_lat'] + 0.02))
                    plt.xlabel('Longitude')
                    plt.ylabel('Latitude')
                    plt.legend()
                    plt.show()

                except EXCEPTION as ex:
                    print(ex)

            messagebox.showinfo("showinfo",
                                f"Journey from {start.name} to {end.name} will take {time[-1]} minutes.")
            a = messagebox.askyesno("askyesno", "Would you like to see the map?")
            if a:
                plot_route(route=routes[end.station_id])
            else:
                root.destroy()
            return

        except EXCEPTION:
            messagebox.showerror("showerror",
                                 "To view the route, please re-run the programme with valid inputs.")


class CSV:
    @staticmethod
    def importData(file_name, list_name):
        """
        Open CSV file and append all the rows as unique dictionary.
        ========= ===============================================================
        Arguments Meaning
        --------- ---------------------------------------------------------------
        file_name = File to be read.
        list_name = List where rows will be appended.
        """
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                list_name.append(row)
            csv_file.close()

    @staticmethod
    def convertStringToInt(list_name, column):
        """
        Typecast all the values corresponding to a key into Integer.
        """
        for li in list_name:
            a = int(li[column])
            li[column] = a

    @staticmethod
    def convertStringToFloat(list_name, column):
        """
        Typecast all the values corresponding to a key into Float.
        """
        for li in list_name:
            a = float(li[column])
            li[column] = a

    @staticmethod
    def getStationAttributeFromId(station_id, attribute_name):
        """
        Returns all the attributes of station from Station ID.
        """
        for station_info in stations:
            if station_info['hub_id'] == station_id:
                return station_info[attribute_name]

    @staticmethod
    def getStationIdFromName(station_name):
        """
        Returns Station ID from Station name.
        """
        for station_info in stations:
            if station_info['name'].lower() == station_name.lower():
                return station_info['hub_id']


if __name__ == '__main__':
    stations = []  # Empty list which will hold all the rows as dictionary from 'londonstations.csv'.
    connections = []  # Empty list which will hold all the rows as dictionary from 'londonconnections.csv'.
    linesList = []  # Empty list which will hold all the rows as dictionary from 'londonlines.csv'.

    CSV.importData('londonstations.csv', stations)
    CSV.importData('londonconnections.csv', connections)
    CSV.convertStringToInt(stations, 'id')
    CSV.convertStringToFloat(stations, 'latitude')
    CSV.convertStringToFloat(stations, 'longitude')
    CSV.convertStringToInt(connections, 'station1')
    CSV.convertStringToInt(connections, 'station2')
    CSV.convertStringToInt(connections, 'line_id')
    CSV.convertStringToInt(connections, 'time')
    CSV.importData('londonlines.csv', linesList)
    CSV.convertStringToInt(linesList, 'line_id')

    lines = {}  # A dictionary of all the rows of 'londonlines.csv' stored with line_id as key
    for i in linesList:
        for j in range(1, 14):
            if i['line_id'] == j:
                lines[j] = i

    for i in range(len(stations)):  # Replacing 'id' key by 'hub_id' in stations list.
        stations[i]['hub_id'] = stations[i].pop('id')

    master_data = []  # Empty list which will hold dictionary of merged data from 'londonstations.csv' and
    # 'londonconnections.csv'.

    for i in range(0, len(connections)):  # Data from stations and connections is merged and added to master
        # data based on hub id.
        temp = {}
        for j in range(0, len(stations)):
            if connections[i]['station1'] == stations[j]['hub_id']:
                temp = connections[i] | stations[j]
        master_data.append(temp)

    for i in range(len(master_data)):  # In order to create all links, a key value pair was added to all
        # dictionaries of merged data.
        master_data[i]['connection_id'] = i

    all_stations = {}  # Empty dictionary which will hold all the objects of Station class against a tuple
    # of station id and line_id
    all_connections = {}  # Empty dictionary which will hold all the objects of Connection class against
    # connection_id.
    for i in range(len(master_data)):
        all_stations[tuple([master_data[i]['station1'], master_data[i]['line_id']])] = Station(master_data[i]['name'],
                                                                                               master_data[i][
                                                                                                   'station1'],
                                                                                               tuple(
                                                                                                   [master_data[i][
                                                                                                        'station1'],
                                                                                                    master_data[i][
                                                                                                        'line_id']]),
                                                                                               master_data[i][
                                                                                                   'latitude'],
                                                                                               master_data[i][
                                                                                                   'longitude'])

        all_stations[tuple([master_data[i]['station2'], master_data[i]['line_id']])] = Station(
            CSV.getStationAttributeFromId(
                master_data[i]['station2'], 'name'), master_data[i]['station2'], tuple(
                [master_data[i]['station2'], master_data[i]['line_id']]),
            CSV.getStationAttributeFromId(master_data[i]['station2'],
                                          'latitude'),
            CSV.getStationAttributeFromId(master_data[i]['station2'], 'longitude'))

        all_connections[i] = Connection(master_data[i]['connection_id'],
                                        tuple([master_data[i]['station1'], master_data[i]['line_id']]),
                                        tuple([master_data[i]['station2'], master_data[i]['line_id']]),
                                        master_data[i]['time'],
                                        master_data[i]['line_id'])

    # Establishing a link between class Station and class Connection by filling
    # station.neighbours and station.connections:

    for i in range(len(master_data)):
        station_to_update = all_stations[tuple([master_data[i]['station1'], master_data[i]['line_id']])]
        station_to_update2 = all_stations[tuple([master_data[i]['station2'], master_data[i]['line_id']])]
        station_to_update.connections.append(i)
        station_to_update2.connections.append(i)
        station_to_update.neighbours.append(tuple([master_data[i]['station2'], master_data[i]['line_id']]))
        station_to_update2.neighbours.append(tuple([master_data[i]['station1'], master_data[i]['line_id']]))

    # Connections representing interchangeable stations - 'Hubs' (Stations with more than one line).

    keys = range(1, len(stations) + 2)
    values = [[] for i in keys]
    hubs = dict(zip(keys, values))
    for id_tuple, station in all_stations.items():
        hubs[id_tuple[0]].append(id_tuple)

    i = 1000
    time_to_change_lines = 0  # Ignoring time taken to change stations
    for hub in hubs.values():  # hub example: 1: [[1, 10], [1, 6], [1, 9]] where first
        # element of list is station id and second is line id.
        for station in hub:  # station example: [1, 10]
            for s in hub:
                if station != s:
                    all_stations[station].neighbours.append(s)
                    all_stations[station].connections.append(i)
                    all_connections[i] = Connection(i, station, s, time_to_change_lines, None)
                    i += 1

    root = Tk()
    root.title("Tube - Transport for London")


    def getInputs():
        Graph().findRoute(source_value.get(), destination_value.get())  # Calling findRoute function
        # with inputs provided through GUI.


    root.geometry("600x200")
    root.maxsize(600, 200)
    root.minsize(600, 200)
    root.resizable(False, False)

    Label(root, text="Welcome to London Tube Network", font="comicsansms 20 bold", pady=15).grid(row=0, column=3)
    Label(root, text="Source Station:        ").grid(row=3, column=2)
    Label(root, text="Destination Station: ").grid(row=4, column=2)

    source_value = StringVar()
    destination_value = StringVar()
    Entry(root, textvariable=source_value).grid(row=3, column=3)
    Entry(root, textvariable=destination_value).grid(row=4, column=3)

    Button(text="Get Time", command=getInputs).grid(row=9, column=3)
    Button(text="Quit", command=root.destroy).grid(row=11, column=3)

    root.mainloop()
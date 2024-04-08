from mbta_api import MBTA_API
import matplotlib.pyplot as plt

class Stop:
    """
        Defines a stop in route. Used to hold all the attributes of the stops.
    """
    def __init__(self, stop_id, attributes):
        self.stop_id = stop_id
        self.attributes = attributes
    def get_name(self):
        return self.attributes.get("name", None)
    def get_longitude(self):
        return self.attributes.get("longitude", None)
    def get_latitude(self):
        return self.attributes.get("latitude", None)
    
class MBTAGraphBuilder:
    """
        Builds a graph of the MBTA and provides utility funtions (like search for routes, etc) 
    """
    def __init__(self, mbta_api: MBTA_API):
        self.mbta_api = mbta_api
        self.subway_map = {}
        self.stop_id_to_stop_data_map = {}
        self.stop_name_to_id_map = {}

    def get_all_stops(self):
        # Return a list of all stops
        return list(self.subway_map.keys())

    def get_stop_data_from_name(self, stop_name):
        # Return the stop data (i.e Stop class)
        stop_id = self.stop_name_to_id_map.get(stop_name)
        stop = self.stop_id_to_stop_data_map.get(stop_id)
        return stop
    
    def add_connection(self, stop1, stop2, route):
        """
            Builds connections in the graph by adding 'route' between two stops. 
        """
        # Add stop2 to the neighbors of stop1
        if stop1 not in self.subway_map:
            self.subway_map[stop1] = {}
        self.subway_map[stop1][stop2] = route
        
        # Add stop1 to the neighbors of stop2
        if stop2 not in self.subway_map:
            self.subway_map[stop2] = {}
        self.subway_map[stop2][stop1] = route

    def add_stops_to_graph(self, route_id, stop_ids):
        """
            Builds connections for all the stops in given route id and stop ids. 
        """
        for i in range(len(stop_ids) - 1):
            stop1 = stop_ids[i]
            stop2 = stop_ids[i + 1]
            if stop1 not in self.stop_id_to_stop_data_map:
                stop_api_data = self.mbta_api.make_stops_api_call(stop1)
                self.stop_id_to_stop_data_map[stop1] = Stop(stop1, stop_api_data["data"]["attributes"])
            if stop2 not in self.stop_id_to_stop_data_map:
                stop_api_data = self.mbta_api.make_stops_api_call(stop2)
                self.stop_id_to_stop_data_map[stop2] = Stop(stop2, stop_api_data["data"]["attributes"])
            stop1name = self.stop_id_to_stop_data_map[stop1].get_name()
            stop2name = self.stop_id_to_stop_data_map[stop2].get_name()

            self.stop_name_to_id_map[stop1name] = stop1
            self.stop_name_to_id_map[stop2name] = stop2

            self.add_connection(stop1name, stop2name, route_id)

    def explore_stops_in_route(self, route_id):
        """
            Explores the stops in route and builds the connections for the given route_id  
        """
        # Make the request
        data = self.mbta_api.make_trips_api_call(route_id)

        # Extract number of stops for each trip
        if "data" in data and data["data"]: 
            for trip in data['data']:
                stop_ids = [item["id"] for item in trip['relationships']['stops']['data']] 
                self.add_stops_to_graph(route_id, stop_ids)
        else:
            print("No trip data found.")

    def build_subway_graph(self):
        """
            Builds the entire subway graph.
        """
        # Make the request to get the routes
        data = self.mbta_api.make_route_api_call()

        # Build set of uniquie route ids
        route_ids = set()
        for item in data['data']:
            route_ids.add(item['id'])

        # Build every route id
        for route_id in route_ids:
            print("Exploring route id ", route_id)
            self.explore_stops_in_route(route_id)
        print("List of stops ", self.get_all_stops())
    
    def find_all_routes(self, start, end):
        """
            Utility function to find routes between two stops.
        """
        visited = set()
        all_routes = set()

        if start == end:
            return ["You are already at your destination."]

        queue = [[start]]

        while queue:
            path = queue.pop(0)
            current_stop = path[-1]

            if current_stop not in visited:
                for next_stop in self.subway_map.get(current_stop, {}):
                    new_path = list(path)
                    new_path.append(next_stop)
                    queue.append(new_path)

                    if next_stop == end:
                        prev_stop = start
                        for stop in new_path:
                            if(prev_stop != stop):
                                route = self.subway_map[prev_stop][stop]
                                all_routes.add(route)
                            prev_stop = stop

                visited.add(current_stop)

        if all_routes:
            return all_routes
        else:
            return ["No routes found."]
    def route_to_color(self, route):
        """
            Utility function to pick a color for route.
        """
        color_map = {
            "Red": (1.0, 0.0, 0.0),             # Red
            "Green-E": (0.0, 1.0, 0.0),         # Green
            "Orange": (1.0, 0.65, 0.0),         # Orange
            "Green-D": (0.0, 0.8, 0.0),         # Light Green
            "Green-B": (0.0, 0.5, 0.0),         # Medium Green
            "Mattapan": (0.0, 0.2, 0.0),        # Dark Green
            "Blue": (0.0, 0.0, 1.0),            # Blue
            "Green-C": (0.0, 0.7, 0.1)          # Another shade of Green
        }
        # Get color for this route
        color = color_map.get(route, (0.0, 0.0, 0.0))

        # Convert RGB tuple to string
        color_str = '#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255))

        return color_str

    def display_stop_graph(self):
        """
            Utility function to display graph of stops in a plot.
        """
        # Initialize plot
        fig, ax = plt.subplots()

        # Plot each stop
        for stop_name, neighbors in self.subway_map.items():
            stop = self.get_stop_data_from_name(stop_name)
            latitude = stop.get_latitude()
            longitude = stop.get_longitude()
            stop_name = stop.get_name()
            if longitude == 0 or longitude == 0 : 
                continue
            # Plot stop with text
            ax.plot(longitude, latitude, 'bo')  
            ax.text(longitude, latitude, stop_name, fontsize=8, ha='right')

            # Plot connections between this stop and its neighbors
            for neighbor_name, route in neighbors.items():
                neighbor = self.get_stop_data_from_name(neighbor_name)
                neighbor_latitude = neighbor.get_latitude()
                neighbor_longitude = neighbor.get_longitude()

                # Plot colored line
                ax.plot([longitude, neighbor_longitude], [latitude, neighbor_latitude], self.route_to_color(route))  

        # Set labels
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('MBTA Stops')

        # Show plot
        plt.show(block=False)
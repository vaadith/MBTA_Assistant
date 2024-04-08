from mbta_api import MBTA_API

class Stop:
    def __init__(self, stop_id, attributes):
        self.stop_id = stop_id
        self.attributes = attributes

    def get_name(self):
        return self.attributes.get("name", None)
    
class MBTAGraphBuilder:
    def __init__(self, mbta_api: MBTA_API):
        self.mbta_api = mbta_api
        self.subway_map = {}
        self.stopid_to_stop_map = {}
        self.stop_name_to_id = {}

    def add_connection(self, stop1, stop2, route):
        # Add stop2 to the neighbors of stop1
        # print("Adding ", stop1, " & ", stop2, " to route ", route)
        if stop1 not in self.subway_map:
            self.subway_map[stop1] = {}
        self.subway_map[stop1][stop2] = route
        
        # Add stop1 to the neighbors of stop2
        if stop2 not in self.subway_map:
            self.subway_map[stop2] = {}
        self.subway_map[stop2][stop1] = route

    def get_stop_name(self, stop_id):
        return self.stopid_to_stop_map[stop_id].get_name()

    def get_stop_ids(self):
        # Return a list of all stop IDs
        return list(self.subway_map.keys())
    
    def get_stop_names(self, stop_ids):
        stop_names = [] 
        for stop_id in stop_ids : 
            name = self.get_stop_name(stop_id)
            if name not in self.stop_name_to_id:
                self.stop_name_to_id[name] = stop_id
                stop_names.append(name)
        return stop_names

    def get_stop_id(self, stop_name):
        return self.stop_name_to_id[stop_name]

    def get_stop_platform_name(self, stop_id):
        stop = self.stops.get(stop_id)
        if stop:
            return stop.get_platform_name()
        else:
            return None
    
    def add_stops_to_graph(self, routeId, stop_ids):
        for i in range(len(stop_ids) - 1):
            stop1 = stop_ids[i]
            stop2 = stop_ids[i + 1]
            if stop1 not in self.stopid_to_stop_map:
                stop_api_data = self.mbta_api.make_stops_api_call(stop1)
                self.stopid_to_stop_map[stop1] = Stop(stop1, stop_api_data["data"]["attributes"])
            if stop2 not in self.stopid_to_stop_map:
                stop_api_data = self.mbta_api.make_stops_api_call(stop2)
                self.stopid_to_stop_map[stop2] = Stop(stop2, stop_api_data["data"]["attributes"])
            self.add_connection(stop1, stop2, routeId)

    def explore_stops_in_route(self, routeId):
        # Make the request
        data = self.mbta_api.make_trips_api_call(routeId)

        # Extract number of stops for each trip
        if "data" in data and data["data"]: 
            for trip in data['data']:
                stop_ids = [item["id"] for item in trip['relationships']['stops']['data']] 
                self.add_stops_to_graph(routeId, stop_ids)
        else:
            print("No trip data found.")

    def build_subway_graph(self):
        # Make the request 
        data = self.mbta_api.make_route_api_call()

        # Build set of uniquie route ids
        route_ids = set()
        for item in data['data']:
            route_ids.add(item['id'])

        for route_id in route_ids:
            print("Exploring route id ", route_id)
            self.explore_stops_in_route(route_id)
        print("List of stop ids ", self.get_stop_names(self.get_stop_ids()))
    
    def find_all_routes(self, start, end):
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
                        route = self.subway_map[start][new_path[1]]
                        all_routes.add(route)

                visited.add(current_stop)

        if all_routes:
            return all_routes
        else:
            return ["No routes found."]
    
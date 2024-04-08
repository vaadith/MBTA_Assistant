import requests

class MBTA_API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-v3.mbta.com"  

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"x-api-key": self.api_key}
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def make_route_api_call(self):
        # Define the URL and parameters
        endpoint = "routes"
        params = {"filter[type]": "0,1"}

        # Make the request 
        data = self._make_request(endpoint, params) 
        return data

    def make_trips_api_call(self, routeId):
        # Define the URL and parameters
        endpoint = "trips"

        params = { 
        "include": "stops",
        "fields[trip]": "id,relationships/stops",
        "filter[route]": routeId
        }

        # Make the request 
        data = self._make_request(endpoint, params) 
        return data

    def make_stops_api_call(self, routeId):
        # Define the URL and parameters
        endpoint = "stops/"+routeId

        # Make the request 
        data = self._make_request(endpoint) 
        return data

    def get_num_stops(self, routeId):
        # Make the request
        data = self.make_trips_api_call(routeId)

        # Extract number of stops for each trip
        if "data" in data and data["data"]: 
            for trip in data['data']:
                stop_ids = [item["id"] for item in trip['relationships']['stops']['data']] 
                num_stops = len(stop_ids)
                return num_stops
        else:
            print("No trip data found.")

    def print_stops_in_route(self, route_ids):
        # Find route with min and max stops
        min_stops = 10000;
        max_stops = 0;

        min_stops_route_id = []
        max_stops_route_id = []

        for id in route_ids:
            num_stops = self.get_num_stops(id)
            if(num_stops < min_stops): 
                min_stops = num_stops
                min_stops_route_id = [id]
            elif num_stops == min_stops:
                min_stops_route_id.append(id)

            if(num_stops > max_stops): 
                max_stops = num_stops
                max_stops_route_id = [id]
            elif num_stops == max_stops:
                max_stops_route_id.append(id)
        print("Route ", min_stops_route_id," has ", min_stops, " stops" )
        print("Route ", max_stops_route_id," has ", max_stops, " stops" )

    def get_stops_in_route(self):
        # Make the request 
        data = self.make_route_api_call()

        # Build set of uniquie route ids
        route_ids = set()
        for item in data['data']:
            route_ids.add(item['id'])

        # Print 
        self.print_stops_in_route(route_ids)

    def get_long_names(self):
        # Make the request 
        data = self.make_route_api_call()

        # Extract output
        long_names = [item['attributes']['long_name'] for item in data['data']]
        return long_names


from mbta_api import MBTA_API
from mbta_graph_builder import MBTAGraphBuilder

def print_main_screen(): 
    print("----------------------------------------------")
    print("1. List all the subway route names")
    print("2. Trivia")
    print("3. Which train should I take?")
    print("4. I dont need help, exit.")

def get_user_input():
    val = input("Please enter a number 1, 2, 3 or 4 : ") 
    return val

def get_start_station(mbta_graph):
    start_name = input("Please enter start station name : ")
    start_id = mbta_graph.get_stop_id(start_name) 
    return start_id

def get_stop_station(mbta_graph):
    end_name = input("Please enter end station name : ") 
    end_id = mbta_graph.get_stop_id(end_name)
    return end_id

def run_cli(mbta: MBTA_API, mbta_graph: MBTAGraphBuilder):
    running = True 
    while running:
        print_main_screen()
        user_input = get_user_input()

        match user_input:
            case "1":
                print("----------------------------------------------")
                print("Getting names of the routes....")
                print("----------------------------------------------")
                long_names = mbta.get_long_names()
                for name in long_names:
                    print(name)
                
            case "2": 
                print("----------------------------------------------")
                print("Getting number of stops in every routes...")
                print("----------------------------------------------")
                mbta.get_stops_in_route()

            case "3": 
                print("----------------------------------------------")
                print("Finding route between two stops...")
                print("----------------------------------------------")
                start = get_start_station(mbta_graph)
                end = get_stop_station(mbta_graph)
                print("You can take the following routes : ", mbta_graph.find_all_routes(start, end))

            case "4": 
                print("Goodbye!")
                running = False
            
            case _:
                print("ERROR : Invalid input, please enter a valid value")
                print("Try again")

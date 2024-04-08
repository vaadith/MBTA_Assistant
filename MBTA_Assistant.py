from mbta_cli import run_cli
from mbta_api import MBTA_API
from mbta_graph_builder import MBTAGraphBuilder

def initialize_mbta_api(api_key) -> MBTA_API:
    mbta = MBTA_API(api_key)
    return mbta

def initialize_mbta_graph(mbta_api: MBTA_API) -> MBTAGraphBuilder:
    mbta_graph = MBTAGraphBuilder(mbta_api)
    mbta_graph.build_subway_graph()
    mbta_graph.display_stop_graph()
    return mbta_graph

if __name__ == "__main__":
    api_key = "494bcbad1fc2431d98a3e45860ce301f"
    mbta_api = initialize_mbta_api(api_key)
    mbta_graph = initialize_mbta_graph(mbta_api)
    run_cli(mbta_api, mbta_graph)
# MBTA_Assistant
1. Run the following command `./setup.sh` to install all the requirements of the MBTA_Assistant

> [!TIP]
> Run `chmod +x setup.sh` to ensure the scripts has write permissions

2. Run `./start.sh` to start the MBTA_Assistant.py

## MBTA_Assistant : Architecture overview
### mbta_assistant.py 
mbta_assistant is the main python file, creates mbta_api and mbta_graph_builder classes 

###  mbta_api.py 
mbta_api is a wrapper class around api calls to mbta
> [!NOTE] 
> make_route_api_call function rely on the server to filer thr routes to type 0 or 1, this choise was made to minimize the data trasfer between mbta server and mbta_assistant 

### mbta_graph_builder.py 
mbta_graph_builder builds a graph of subway and Provides search functionality
> [!NOTE] 
> mbta_graph_builder uses mbta_api to get required the data to build the graph

### mbta_cli.py 
Contains all the interactions with the user.
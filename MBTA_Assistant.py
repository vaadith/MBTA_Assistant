import requests
import json

print("Hi! I am the MBTA Assistant! How can I help you?")
print("1. List all the subway route names")
print("2. Trivia")
print("3. Which train should I take?")
print("4. I dont need help, exit.")
check = True
while check:
    val = input("Please enter a number 1, 2, 3 or 4 : ") 

    match val:
        case "1":
            r = requests.get('https://api-v3.mbta.com/lines?sort=long_name')
            input_dict = json.loads(r.text)
            long_names = [item['attributes']['long_name'] for item in input_dict['data']]
            for name in long_names:
                print(name)

        case "2": 
            print("TODO")
 
        case "3": 
            print("TODO")
        case "4": 
            print("Goodbye!")
            check = False
        case _: 
            print("Please enter 1,2,3")
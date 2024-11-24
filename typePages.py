from flask import render_template
import requests 

def typeFetch():
    # Define the number of batches or types to fetch (you can adjust this based on your needs)
    typeBatch = 2
    
    # Define the Pokémon type to fetch (in this case, "grass")
    poketype = "grass"
    
    # Loop through the range for fetching multiple batches if needed
    for id in range(1, typeBatch + 1):  # Adjust to process the correct range
        # Construct the API URL
        url = f"https://pokeapi.co/api/v2/type/{poketype}"
        
        # Send the request to the API
        response = requests.get(url)
        
        # Parse the JSON response
        if response.status_code == 200:
            type_data = response.json()
            
            # List to store Pokémon names and URLs
            pokemons = []
            
            # Loop through the Pokémon data in the response
            for entry in type_data["pokemon"]:
                # Extract Pokémon name and URL
                pokemon_name = entry["pokemon"]["name"]
                pokemon_url = entry["pokemon"]["url"]
                
                # Append the data as a dictionary
                pokemons.append({"name": pokemon_name, "url": pokemon_url})
            
            # Print the names of all Pokémon in the current batch
            for pokemon in pokemons:
                print(pokemon["name"])
                
            # Return the list of Pokémon (optional, if you want to use this data elsewhere)
            return pokemons
        
        else:
            print(f"Failed to fetch data for type {poketype}")
            return []

# Call the function to fetch Pokémon data
pokemons = typeFetch()

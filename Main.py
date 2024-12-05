# Import necessary libraries for web framework (Quart) and asynchronous operations (asyncio, aiohttp)
from quart import Quart, render_template, abort 
import asyncio
import aiohttp
# Initialize the Quart web application
app = Quart(__name__)

# Asynchronous function to fetch a batch of Pokémon data from the API
async def fetch_batch(batch, offset, session):
    try:
        # Make an asynchronous GET request to fetch a batch of Pokémon
        url = f"https://pokeapi.co/api/v2/pokemon/?limit={batch}&offset={offset}"
        async with session.get(url) as response:
            return await response.json()  # Return the batch data in JSON format
    except Exception as e:
        print(f"ann error as occurred : {str(e)} ")
# Output: Url of batch value many pokemon urls from the offset value point 

# Asynchronous function to fetch detailed information for a specific Pokémon
async def fetched_details(session, url):
    try:
        # Make an asynchronous GET request to fetch detailed data for the Pokémon
        async with session.get(url) as response:
            return await response.json()  # Return detailed data in JSON format
    except Exception as e:
        print(f"ann error as occurred : {str(e)} ")

# Asynchronous function to fetch all Pokémon data in batches
async def fetch_all_pokemon(offset, batch):
    try:
        # Open a session to handle multiple HTTP requests concurrently
        async with aiohttp.ClientSession() as session:
            # Fetch the batch of Pokémon data from the API
            batch_data = await fetch_batch(batch, offset, session)
            
            # If there is no 'results' key, return an empty list
            if "results" not in batch_data:
                return []

            # Create a list of tasks to fetch detailed information for each Pokémon concurrently
            tasks = [fetched_details(session, pokemon["url"]) for pokemon in batch_data["results"]]
            
            # Gather all tasks and return the detailed data for all Pokémon
            return await asyncio.gather(*tasks)
    except Exception as e:
        print(f"an error has occured : {str(e)}")

    # Main function to fetch, process, and display Pokémon data
async def index():
    # Fetch the first batch of 100 Pokémon starting from offset 0
    pokemon_data = await fetch_all_pokemon(0, 100)
    
    pokemon_list = []
    
    for pokemon in pokemon_data:
        img = pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        name = pokemon["name"]
        weight = pokemon["weight"]
        height = pokemon["height"]
        types = [type_info["type"]["name"] for type_info in pokemon["types"]]
        mtype = types[0] if types else "Unknown"
        
        # Append the processed Pokémon information into the list
        pokemon_list.append({
            "name": name.capitalize(),
            "image": img,
            "weight": weight,
            "height": height,
            "types": types,
            "mtype": mtype
        })
    

@app.route('/pokemon/<int:pokemon_id>')  # Dynamic route with integer type
async def pokemon_detail(pokemon_id):
    # Ensure Pokémon ID is within valid range
    if pokemon_id < 1 or pokemon_id > 1026:
        return "Pokémon not found!", 404

    try:
        # Asynchronous HTTP request to fetch Pokémon data
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    abort(404, f"Pokémon with ID {pokemon_id} not found.")
                
                pokemon = await response.json()  # Parse JSON response

        # Extract relevant data
        name = pokemon["name"]
        img = pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        height = pokemon["height"] / 10  # Convert to meters
        weight = pokemon["weight"] / 10  # Convert to kilograms
        types = [type_info["type"]["name"] for type_info in pokemon["types"]]
        mtype = types[0] if types else "Unknown"

        # Pokémon dictionary for rendering
        pokemon = {
            "id": pokemon_id,
            "name": name.capitalize(),
            "height": height,
            "weight": weight,
            "types": ", ".join(types),
            "mtype": mtype,
            "img": img,
        }

        # Render template with Pokémon data
        return await render_template('pokemon_singlePage.html', pokemon=pokemon)

    except aiohttp.ClientError as e:
        return f"An error occurred while fetching Pokémon data: {e}", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500


@app.route('/pokemon/<string:pokemon_mtype>')
async def typesort(pokemon_mtype):
    try:
        # Asynchronous HTTP request to fetch Pokémon data
        url = f"https://pokeapi.co/api/v2/type/{pokemon_mtype}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    abort(404, f"Pokémon with type {pokemon_mtype} not found.")
                
                pokemon1 = await response.json()  # Parse JSON response
                pokemon_urls = [entry['pokemon']['url'] for entry in pokemon1['pokemon']]  # Extract URLs

        # Fetch each Pokémon's data
        pokemon_data_list = []
        async with aiohttp.ClientSession() as session:
            for pokemon_url in pokemon_urls:
                async with session.get(pokemon_url) as response1:
                    if response1.status == 200:
                        pokemon = await response1.json()
                        # Collect relevant data for each Pokémon

                    match pokemon_mtype:
                        case "normal":
                            backColor = "rgba(168, 168, 120, 0.6)"  # Normal
                        case "fire":
                            backColor = "rgba(255, 87, 34, 0.6)"  # Fire
                        case "water":
                            backColor = "rgba(30, 144, 255, 0.6)"  # Water  
                        case "flying":
                            backColor = "rgba(135, 206, 235, 0.6)"  # Flying
                        case "fighting":
                            backColor = "rgba(211, 47, 47, 0.6)"  # Fighting
                        case "poison":
                            backColor = "rgba(156, 39, 176, 0.6)"  # Poison
                        case "electric":
                            backColor = "rgba(255, 235, 59, 0.6)"  # Electric
                        case "ground":
                            backColor = "rgba(139, 69, 19, 0.6)"  # Ground
                        case "rock":
                            backColor = "rgba(161, 136, 127, 0.6)"  # Rock
                        case "psychic":
                            backColor = "rgba(156, 39, 176, 0.6)"  # Psychic
                        case "ice":
                            backColor = "rgba(0, 188, 212, 0.6)"  # Ice
                        case "bug":
                            backColor = "rgba(139, 195, 74, 0.6)"  # Bug
                        case "ghost":
                            backColor = "rgba(156, 39, 176, 0.6)"  # Ghost
                        case "steel":
                            backColor = "rgba(176, 190, 197, 0.6)"  # Steel
                        case "dragon":
                            backColor = "rgba(3, 169, 244, 0.6)"  # Dragon
                        case "dark":
                            backColor = "rgba(33, 33, 33, 0.6)"  # Dark
                        case "fairy":
                            backColor = "rgba(244, 143, 177, 0.6)"  # Fairy
                        case "grass":
                            backColor = "rgba(0, 128, 0, 0.6)"  # Grass
                        case _:
                            backColor = "rgba(255, 255, 255, 0.6)"  # Default white
                    pokemon_data_list.append({
                    'id': pokemon["id"],
                    'name': pokemon["name"],
                    'types': [type_info["type"]["name"] for type_info in pokemon["types"]],
                    'img': pokemon["sprites"]["other"]["official-artwork"]["front_default"],
                    'height': pokemon["height"] / 10,  # Convert height from decimeters to meters
                    'weight': pokemon["weight"] / 10,  # Convert weight from hectograms to kilograms
                    'bcolor': backColor 
                })


        # Render template with the collected Pokémon data
        return await render_template('typesPage.html', pokemon_data_list=pokemon_data_list)

    except aiohttp.ClientError as e:
        return f"An error occurred while fetching Pokémon data: {e}", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500


@app.route('/')
async def index():
    pokemon_data = await fetch_all_pokemon(0, 10000)
    
    pokemon_list = []
    
    for pokemon in pokemon_data:
        id = pokemon["id"]
        img = pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        name = pokemon["name"]
        weight = pokemon["weight"] / 10
        height = pokemon["height"]  / 10
        types = [type_info["type"]["name"] for type_info in pokemon["types"]]
        mtype = types[0] if types else "Unknown"
        match mtype:
                    case "normal":
                        backColor = "rgba(168, 168, 120, 0.6)"  # Normal
                    case "fire":
                        backColor = "rgba(255, 87, 34, 0.6)"  # Fire
                    case "water":
                        backColor = "rgba(30, 144, 255, 0.6)"  # Water  
                    case "flying":
                        backColor = "rgba(135, 206, 235, 0.6)"  # Flying
                    case "fighting":
                        backColor = "rgba(211, 47, 47, 0.6)"  # Fighting
                    case "poison":
                        backColor = "rgba(156, 39, 176, 0.6)"  # Poison
                    case "electric":
                        backColor = "rgba(255, 235, 59, 0.6)"  # Electric
                    case "ground":
                        backColor = "rgba(139, 69, 19, 0.6)"  # Ground
                    case "rock":
                        backColor = "rgba(161, 136, 127, 0.6)"  # Rock
                    case "psychic":
                        backColor = "rgba(156, 39, 176, 0.6)"  # Psychic
                    case "ice":
                        backColor = "rgba(0, 188, 212, 0.6)"  # Ice
                    case "bug":
                        backColor = "rgba(139, 195, 74, 0.6)"  # Bug
                    case "ghost":
                        backColor = "rgba(156, 39, 176, 0.6)"  # Ghost
                    case "steel":
                        backColor = "rgba(176, 190, 197, 0.6)"  # Steel
                    case "dragon":
                        backColor = "rgba(3, 169, 244, 0.6)"  # Dragon
                    case "dark":
                        backColor = "rgba(33, 33, 33, 0.6)"  # Dark
                    case "fairy":
                        backColor = "rgba(244, 143, 177, 0.6)"  # Fairy
                    case "grass":
                        backColor = "rgba(0, 128, 0, 0.6)"  # Grass
                    case _:
                        backColor = "rgba(255, 255, 255, 0.6)"  # Default white
        
        pokemon_list.append({
            "bcolor": backColor,
            "id": id,
            "name": name.capitalize(),
            "image": img,
            "weight": weight,
            "height": height,
            "types": types,
            "mtype": mtype
        })
    return await render_template('index.html', pokemon=pokemon_list)
if __name__ == '__main__':
    app.run()
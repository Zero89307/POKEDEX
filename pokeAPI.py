from flask import Flask, render_template
import requests

app = Flask(__name__)

def pokedata():
    pokebatch = 10  # How Many Pokemons to call for later use (dynamic loading)
    category = "pokemon"
    pokemon_data = []

    for id in range(1, pokebatch):  # Loop to get data for each Pokemon from the API
        try:
            url = f"https://pokeapi.co/api/v2/{category}/{str(id)}"
            response = requests.get(url)  # Getting response as JSON
            req_data = response.json()

            # Creating values for specific Pokemon data
            name = req_data["name"]
            img = req_data["sprites"]["other"]["official-artwork"]["front_default"]
            height = req_data["height"] / 10
            weight = req_data["weight"] / 10
            types = [type_info["type"]["name"] for type_info in req_data["types"]]
            main_type = types[0] if types else "Unknown"

            # Determining the background color based on main type
            try:
                match main_type:
                    case "normal":
                        backColor = "#A8A878"  
                    case "fire":
                        backColor = "#FF5722"  
                    case "water":
                        backColor = "#1E90FF"  
                    case "flying":              
                        backColor = "#87CEEB"  
                    case "fighting":
                        backColor = "#D32F2F"  
                    case "poison":
                        backColor = "#9C27B0"  
                    case "electric":
                        backColor = "#FFEB3B"  
                    case "ground":
                        backColor = "#8B4513"  
                    case "rock":
                        backColor = "#A1887F" 
                    case "psychic":
                        backColor = "#9C27B0"  
                    case "ice":
                        backColor = "#00BCD4" 
                    case "bug":
                        backColor = "#8BC34A" 
                    case "ghost":
                        backColor = "#9C27B0" 
                    case "steel":
                        backColor = "#B0BEC5" 
                    case "dragon":
                        backColor = "#03A9F4"  
                    case "dark":
                        backColor = "#212121"  
                    case "fairy":
                        backColor = "#F48FB1"  
                    case _:
                        backColor = "#FFFFFF"  # Default to white if type not found
            except Exception as e:
                print(f"Error determining color: {e}")
                backColor = "#FFFFFF"  # Default color if something goes wrong

            # Store each Pokémon's data
            pokemon_data.append({
                "name": name,
                "height": height,
                "weight": weight,
                "types": ", ".join(types),
                "main_type": main_type,
                "img": img,
                "backColor": backColor
            })

        except Exception as e:
            print(f"An error occurred with Pokémon ID {id}: {e}")

    return pokemon_data

@app.route('/')
def index():
    # Fetch the Pokémon data
    data = pokedata()
    return render_template('index.html', pokemon_list=data)

if __name__ == '__main__':
    app.run(debug=True)

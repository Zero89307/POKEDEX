from flask import Flask, render_template
import requests

app = Flask(__name__) 

def pokedata():
    pokebatch = 30 # How Many Pokemons to call for later use (dynamic loading)
    category = "pokemon"
    pokemon_data = []   #creating empty array that will store the pokemon data 

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
            except Exception as e:
                print(f"Error determining color: {e}")
                backColor = "#FFFFFF"  # Default color if something goes wrong

            # Adding each value to the array via the append method 
            pokemon_data.append({
                "id": id,
                "name": name,
                "height": height,
                "weight": weight,
                "types": ", ".join(types),
                "main_type": main_type,
                "img": img,
                "backColor": backColor,
            })
            print
        except Exception as e:
            print(f"An error occurred with Pokémon ID {id}: {e}")

    return pokemon_data #returns the array with all the data stored 
@app.route('/pokemon/<int:pokemon_id>')
def pokemon_detail(pokemon_id):
    if pokemon_id < 1 or pokemon_id > 1026:  # id clause so no out od bound errors can happend 
        return "Pokémon not found!", 404
    # Fetch data for the specific Pokémon for the single pages 
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)
        req_data = response.json()  

        name = req_data["name"]
        img = req_data["sprites"]["other"]["official-artwork"]["front_default"]
        height = req_data["height"] / 10
        weight = req_data["weight"] / 10
        types = [type_info["type"]["name"] for type_info in req_data["types"]]
        main_type = types[0] if types else "Unknown"

        pokemon = {
            "id": int(pokemon_id),
            "name": name,
            "height": height,
            "weight": weight,
            "types": ", ".join(types),
            "img": img,
            
        }
        #returning the array pokemon via flask render template into the single page html 
        return render_template('pokemon_singlePage.html',pokemon=pokemon)

    except Exception as e:
        return f"An error occurred: {e}", 404

@app.route('/') # app route for the curren directory 
def index():
    # Fetch the Pokémon data
    data = pokedata()
    return render_template('index.html', pokemon_list=data) # returning the pokemin data to the index.html as pokemon_list 

if __name__ == '__main__':
    app.run(debug=True)

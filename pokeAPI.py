from flask import Flask, render_template, request  
import requests 

def pokedata():
    pokebatch = 1000
    
    catagory = "pokemon"
    for id in range(1, pokebatch):
        global req_data, name, img, height, weight, type
        url = f"https://pokeapi.co/api/v2/{catagory}/{str(id)}"
        response = requests.get(url)    
        req_data = response.json()
        name = req_data["name"]
        img = req_data["sprites"]["other"]["official-artwork"]["front_default"]
        height = req_data["height"] / 10 
        weight = req_data["weight"] / 10
        type = ", ".join([type_info["type"]["name"] for type_info in req_data["types"]]) 
        print(str(name) + "\n" +str(img) + "\n" + str(type) + "\n" + str(height) + "m\n" + str(weight) +"Kg\n" )



pokedata()

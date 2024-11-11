from flask import Flask, render_template, request  
import requests



space = """

"""
def pokedata():
    pokebatch = 100
    id = 5
    catagory = "pokemon"
    for id in range(1, pokebatch):
        url = f"https://pokeapi.co/api/v2/{catagory}/{str(id)}"
        response = requests.get(url)    
        req_data = response.json()
        name = req_data["name"]
        img = req_data["sprites"]["other"]["official-artwork"]["front_default"]
        type = ", ".join([type_info["type"]["name"] for type_info in req_data["types"]]) 
        print(str(name) + "\n" +str(img) + "\n" + str(type) + "\n" )
        
        



    




pokedata()
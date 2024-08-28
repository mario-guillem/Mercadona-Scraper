import os
import requests
import json
import pandas as pd

def getCategories():
    # Obtener los datos de la API. En nuestro caso mediante el código postal 46980 nos corresponden los datos del Warehouse 'Valencia 1'
    response = requests.get("https://tienda.mercadona.es/api/categories/?lang=es&wh=vlc1")
    # Convertir el texto a un objeto JSON
    categories = response.json()
    # Guardar el objeto JSON en un archivo llamado 'categories.json'
    with open("categories.json", "w", encoding="utf-8") as json_file:
        json.dump(categories, json_file, ensure_ascii=False, indent=4)

    # Crear una lista para almacenar las categorías 
    categories_list = []
    subcategories_list = []
    # Iterar sobre las categorías principales y las subcategorías
    for item in categories['results']:
        categories_list.append(item['id'])  # Agregar la categoría principal
        for subcategory in item['categories']:
            subcategories_list.append(subcategory['id'])  # Agregar la subcategoría
    
    ids = []
    def extract_ids(item):
        if isinstance(item, dict):
            if 'id' in item:
                ids.append(item['id'])
            for value in item.values():
                extract_ids(value)
        elif isinstance(item, list):
            for i in item:
                extract_ids(i)

    names = []
    def extract_names(item):
        if isinstance(item, dict):
            if 'name' in item:
                names.append(item['name'])
            for value in item.values():
                extract_names(value)
        elif isinstance(item, list):
            for i in item:
                extract_names(i)

    extract_names(categories)
    extract_ids(categories)

    data = pd.DataFrame({
    'ID': ids,
    'Name': names
    })

    data.to_csv('./categoriesData.csv', index=False)
    os.remove("categories.json")
    return subcategories_list

"""
Devuelve los ids de las subcategorías, puesto que cuando tu realizas la búsqueda de los productos
Mercadona no te deja mostrar todos los productos de las categorías. Pienso que es lo más orgánico.

"""
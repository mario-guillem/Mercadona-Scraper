from getCategories import getCategories
import requests
import pandas as pd
import json
import os

def getProducts():

    # Listas para guardar los nombres y precios
    display_names = []
    unit_prices = []
    unit_sizes = []
    sizes_format = []

    ids = getCategories()
    for i in ids:
        response = requests.get(f"https://tienda.mercadona.es/api/categories/{i}/?lang=es&wh=vlc1")
        products = response.json()

        with open("products.json", "w", encoding="utf-8") as json_file:
                json.dump(products, json_file, ensure_ascii=False, indent=4)

    # Recorrer cada categoría y luego cada producto
        for category in products['categories']:
            for product in category['products']:
                display_names.append(product['display_name'])
                unit_prices.append(product['price_instructions']['unit_price'])
                unit_sizes.append(product['price_instructions']['unit_size'])
                sizes_format.append(product['price_instructions']['size_format'])

    allProducts = pd.DataFrame({
        'producto': display_names,
        'precio': unit_prices,
        'tamaño': unit_sizes,
        'sizes_format': sizes_format
            })

    allProducts.to_csv('./allProductsData.csv', index=False)
    os.remove("products.json")

getProducts()

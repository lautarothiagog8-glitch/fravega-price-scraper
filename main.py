import time
import requests
import random
import csv
from datetime import datetime
from pathlib import Path

producto_buscado = "Heladera"
pagina = 0
limite = 15
paginas_procesadas = 0

user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/19.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:153.0) Gecko/20100101 Firefox/153.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36'
]

# Ruta principal y creación de carpeta organizadora
ruta_principal = Path(__file__).parent
carpeta_scraper = ruta_principal / "Carpeta_Scraper_Organizada"
carpeta_scraper.mkdir(exist_ok=True, parents=True)

# Obtener la fecha y hora exacta en la cual ejecutas el programa, y crear un nombre que se va a usar en el archivo.
momento_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
nombre_dinamico = f"Fravega_{producto_buscado}_{momento_actual}.csv"

# Inicio del bloque with(En donde se abre el archivo .csv)
with open(carpeta_scraper / nombre_dinamico, "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    # Escribimos un encabezado predeterminado
    escritor.writerow(["Fecha", "Busqueda", "Titulo", "Precio"])

    while True:
        headers = {
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'content-type': 'application/json',
            'fravega-search-source': 'webstoreSearch',
            'origin': 'https://www.fravega.com',
            'priority': 'u=1, i',
            'referer': 'https://www.fravega.com/l/?keyword=bicicleta%20rodado%2029',
            'user-agent': random.choice(user_agent)
        }
        json_data = {
            'operationName': 'GetItems',
            'variables': {
                'filters': {
                    'keywords': producto_buscado,
                    'zones': [],
                },
                'presentationFilters': {
                    'priceChannel': 'fravega-ecommerce',
                    'cockadeTag': 'listing',
                    'collections': {
                        'aggregable': True,
                        'onlyThoseWithCockade': True,
                    },
                    'stockZoneIds': [],
                },
                'pagination': {
                    'size': limite,
                    'from': pagina
                },
                'sorting': 'TOTAL_SALES_IN_LAST_30_DAYS',
                'sessionId': 'ae748e3f-7df2-40a7-984e-6bea73273eb3',
            },
            'query': 'query GetItems($sessionId: String, $filters: Filters, $presentationFilters: PresentationFilters, $pagination: Pagination, $sorting: SortOption) {\n  items(\n    sessionId: $sessionId\n    filters: $filters\n    presentationFilters: $presentationFilters\n    pagination: $pagination\n    sorting: $sorting\n  ) {\n    total\n    listUniqueId\n    applicableFilters\n    facets {\n      categories {\n        name\n        value\n        count\n        filtered\n        __typename\n      }\n      brands {\n        value\n        name\n        count\n        filtered\n        __typename\n      }\n      sellerConditions {\n        name\n        value\n        count\n        filtered\n        __typename\n      }\n      installments {\n        name\n        value\n        count\n        filtered\n        __typename\n      }\n      price {\n        min\n        max\n        __typename\n      }\n      discounts {\n        name\n        value\n        slug\n        count\n        filtered\n        __typename\n      }\n      collections {\n        name\n        value\n        count\n        filtered\n        __typename\n      }\n      attributes {\n        name\n        value\n        values {\n          name\n          value\n          paths\n          count\n          filtered\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    results {\n      ...itemResultFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment itemResultFragment on SkuItem {\n  code\n  cockades(tag: "listing") {\n    image\n    position\n    tags\n    __typename\n  }\n  collections {\n    id\n    name\n    slug\n    cockade {\n      image\n      position\n      tags\n      __typename\n    }\n    tags\n    __typename\n  }\n  item {\n    id\n    type\n    active\n    gtin {\n      ... on EAN {\n        number\n        __typename\n      }\n      __typename\n    }\n    title\n    slug\n    katalogCategoryId\n    primaryCategoryId\n    brand {\n      id\n      name\n      slug\n      image\n      __typename\n    }\n    images\n    triggers\n    sellerConditions\n    __typename\n  }\n  seller {\n    id\n    commercialName\n    slug\n    __typename\n  }\n  marketplace\n  images\n  enabledChannels\n  categorization {\n    id\n    name\n    slug\n    __typename\n  }\n  pricing {\n    salePrice\n    listPrice\n    channel\n    discount\n    withoutTax\n    __typename\n  }\n  stock {\n    labels\n    __typename\n  }\n  sponsored\n  resolvedBidId\n  campaignId\n  __typename\n}\n',
        }
        try:
            # Llamada a la api de la pagina y obtensión de datos
            response = requests.post('https://www.fravega.com/api/v2', headers=headers, json=json_data)
            response.raise_for_status()
            json_res = response.json()
            todo = json_res.get("data", {}).get("items", {})
            resultado = todo.get("results", [])

            if paginas_procesadas == 0 and not resultado:
                print("Algo cambio en la calve del JSON!!!")
                break

            if not resultado:
                print("Has llegado al fin de la paginacion")
                break

            for r in resultado:
                fecha_extraccion = momento_actual
                busqueda = producto_buscado
                titulo = r["item"]["title"]
                precio = r["pricing"]["salePrice"]
                precio_formateado = f"${precio:,.0f}".replace(",", ".")

                lista_producto = [fecha_extraccion, busqueda, titulo, precio_formateado]
                escritor.writerow(lista_producto)

            paginas_procesadas += 1
            pagina += limite
            time.sleep(random.uniform(2.0, 4.0))

        except requests.exceptions.HTTPError as e:
            codigo_status = response.status_code
            if codigo_status == 429:
                print("Rate Limit (429)! Demasiadas peticiones. Pausando 30 segundos...")
                time.sleep(30)
            elif codigo_status == 403:
                print("Acceso prohibido (403). Posible bloqueo anti-bot.")
                break
            else:
                print(f"Error HTTP inesperado: {codigo_status}")
                break

        except requests.exceptions.ConnectionError:
            print("Error de conexión. Verificá tu internet.")
            break

        except requests.exceptions.RequestException as e:
            print(f"Error no identificado en requests: {e}")
            break
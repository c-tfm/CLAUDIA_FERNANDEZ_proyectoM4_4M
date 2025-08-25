# Importación de librerías necesarias (Explicación a mayor detalle en el readme):


#Se importan las librerías
import requests
import json
import os
import time
import random
import pandas as pd
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap

#Se ingresa nuestra API Pokémon
API_POKEMON = "https://pokeapi.co/api/v2/pokemon/{pokemon}"

@sleep_and_retry
@limits(calls=100, period=60)
def call_api(url):
#Hacemos llamado a la API para las consultas
    response = requests.get(url)

    if response.status_code == 404:
        return "Not Found"
#Recordemos que 404 es que no existe, es decir es un error en peticiones HTTP    

    if response.status_code != 200:
        print("Tus resultados:", response.status_code, url)
        raise Exception("API response: {}".format(response.status_code))
    return response

def mostrar_imagen_con_info(imagen_base64, info):

#Muestra la imagen del Pokémon con su información en la parte superior y ajustando el ancho del texto

    if not imagen_base64:
        print("No hay imagen disponible.")
        print()
        return

    imagen_bytes = base64.b64decode(imagen_base64)
    imagen = Image.open(BytesIO(imagen_bytes)).convert("RGBA")

#Aquí solicitamos que nos devuelva la API los datos en donde van

    lineas = [
        f"Nombre: {info.get('nombre', '')}",
        f"Altura: {info.get('altura', '')}",
        f"Peso: {info.get('peso', '')}",
        f"Tipos: {', '.join(info.get('tipos', []))}",
        f"Habilidades: {', '.join(info.get('habilidades', []))}",
        f"Movimientos: {', '.join(info.get('movimientos', []))}"
    ]
    
    font = ImageFont.load_default()
    line_height = 15
    padding = 10
    max_line_width = 50  
#Límite el número de cáracteres antes de hacer wrap en el texto para que no se pierda ni se corte
    wrapped_lines = []
    for linea in lineas:
        wrapped_lines.extend(textwrap.wrap(linea, width=max_line_width))

#Si hay mucho texto, la imagen se hace más ancha usando draw.textbbox
    temp_img = Image.new("RGB", (1,1))
    draw_temp = ImageDraw.Draw(temp_img)
    texto_ancho = max([draw_temp.textbbox((0,0), l, font=font)[2] for l in wrapped_lines]) + 2*padding

    ancho = max(imagen.width, texto_ancho)
    alto = imagen.height + len(wrapped_lines)*line_height + 2*padding
    lienzo = Image.new("RGBA", (ancho, alto), (0,0,0,255))
    draw = ImageDraw.Draw(lienzo)

#Definimos que el texto se escriba en la parte superior de la imagen
    y_text = padding
    for linea in wrapped_lines:
        draw.text((padding, y_text), linea, fill=(255,255,255,255), font=font)
        y_text += line_height

#Y asignamos la imagen debajo del texto, centrada horizontalmente
    x_image = (ancho - imagen.width)//2
    lienzo.paste(imagen, (x_image, len(wrapped_lines)*line_height + 2*padding), imagen)

    lienzo.show()
    print()  
#En varias partes del código se muestra una línea en blanco, esto lo hice para dar un aspecto más cómodo de leer
#Esto se repite varias veces para que al correr el script, se vea menos amontonado

def consultar_pokemon(nombre):
    url = API_POKEMON.format(pokemon=nombre.lower().strip())
    response = call_api(url)

    if not os.path.exists("pokedex"):
        os.makedirs("pokedex")
    ruta_json = os.path.abspath(f"pokedex/{nombre.lower()}.json")

    if response == "Not Found":
        pokemon_data = {
            "nombre_ingresado": nombre,
            "no_existe": True
        }
        with open(ruta_json, "w") as f:
            json.dump(pokemon_data, f, indent=4)
        print(f"\nVaya, que pena, {nombre} no poke-existe")
        print()
        print(f"Se ha guardado un registro en: {ruta_json}")
        print()
        return None

    if response.status_code == 200:
        data = response.json()

        nombre = data["name"].capitalize()
        peso = data["weight"]
        altura = data["height"]
        tipos = [t["type"]["name"] for t in data["types"]]
        habilidades = [h["ability"]["name"] for h in data["abilities"]]
        movimientos = [m["move"]["name"] for m in data["moves"][:5]]
        imagen_url = data["sprites"]["front_default"]

        imagen_base64 = None
        if imagen_url:
            img_data = requests.get(imagen_url).content
            imagen_base64 = base64.b64encode(img_data).decode('utf-8')

        print(f"\n{nombre.upper()} encontrado:")
        print(f"Altura: {altura}")
        print(f"Peso: {peso}")
        print(f"Tipos: {', '.join(tipos)}")
        print(f"Habilidades: {', '.join(habilidades)}")
        print(f"Movimientos: {', '.join(movimientos)}")
        print()  

        pokemon_data = {
            "nombre": nombre,
            "altura": altura,
            "peso": peso,
            "tipos": tipos,
            "habilidades": habilidades,
            "movimientos": movimientos,
            "imagen_base64": imagen_base64,
            "no_existe": False
        }

        with open(ruta_json, "w") as f:
            json.dump(pokemon_data, f, indent=4)
        print(f"Hemos actualizado exitosamente tu '{ruta_json}'")
        print() 

        mostrar_imagen_con_info(imagen_base64, pokemon_data)
        return pokemon_data

    return None

def consultar_varios_pokemon(lista_nombres):
    lista_info = []

    for nombre in tqdm(lista_nombres, desc="Consultando Pokemon"):
        info = consultar_pokemon(nombre)
        if info:
            lista_info.append(
                {
                    "id": len(lista_info) + 1,
                    "name": info["nombre"],
                    "height": info["altura"],
                    "weight": info["peso"],
                    "tipos": ", ".join(info["tipos"]),
                    "imagen_base64": info["imagen_base64"],
                }
            )
        time.sleep(random.uniform(0.2, 0.5))

    if lista_info:
        df = pd.DataFrame(lista_info)
        print() 
        return df
    return None

#Aquí es donde comienza el menú, para que en caso de querer hacer mas consultas se pueda repetir
#Aunque use librerías de limitación de petición, también quise incluir un máximo de 10 consultas 
#La decisión la tomé porque python muestra la imagen aparte de descargar el json y no quise saturar

def main():
    print("¡Hola! Veo que has encontrado nuevos pokeamigos en tu viaje")
    print("Puedes consultar información de 1 a 10 pokemon.")
    print() 


    try:
        cantidad = int(input("¿Cuántos Pokeamigos deseas consultar? (1 a 10): "))

#Aquí ya esta desplegado el menú, donde se limita el número peticionado, de ahi le dará la opción de escribir en cada número un nombre

        if cantidad == 1:
            nombre = input("Escribe el nombre del Pokémon: ")
            consultar_pokemon(nombre)

        elif 2 <= cantidad <= 10:
            nombres = []
            for i in range(cantidad):
                nombres.append(input(f"Escribe el nombre del pokemon #{i+1}: "))

            df = consultar_varios_pokemon(nombres)
            if df is not None:
                print("Después de mucho investigar, aquí está todo lo que sabemos de esos Pokémon:")
                print(df)
                print() 

#En caso de pedir un número mayor a 10, el programa no continua, pide ingresar datos correctos

        else:
            print("Recuerda que somos un pokecentro de investigación pequeño, solo puedes consultar de 1 a 10 pokeamigos.")
            print()

#Así mismo, si se ingresa una letra o cualquier cosa que no sea el valor dicho, manda también un error

    except ValueError:
        print("Para investigar, primero necesitamos saber cuántos piensas buscar, ingresa un número del 1 al 10")
        print()

#En caso de haber recibido uno de los mensajes de error, o finalizado la consulta el programa pregunta si se desea continuar.
if __name__ == "__main__":
    while True:
        main()
        opcion = input("¿Quieres investigar más pokeamigos? (si/no): ").lower().strip()
        if opcion != "si":

#Si el resultado es diferente a "si" Se termina el programa y se despide del usuario

            print("Gracias por usar la Pokédex, nuestros pokeinvestigadores te desean un agradable viaje, entrenador.")
            break
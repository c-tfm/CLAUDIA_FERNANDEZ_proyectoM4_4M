# CLAUDIA_FERNANDEZ_proyectoM4_4M


# Pokédex M4_4M

## Descripción

Este proyecto es una Pokédex interactiva desarrollada en Python.  
Permite consultar cualquier Pokémon existente a través de peticiones HTTP, obteniendo información como:

- Nombre  
- Altura  
- Peso  
- Tipo  
- Habilidades  
- Movimientos  

Además, integra una **imagen del Pokémon** con sus datos presentados de forma visual.

---

## Librerías necesarias

El proyecto utiliza las siguientes librerías de Python:

- **requests** → Permite realizar consultas a la API mediante peticiones HTTP.  
- **tqdm** → Muestra una barra de progreso durante las consultas.  
- **ratelimit** → Permite limitar la frecuencia de peticiones y evitar saturar la CPU.  
- **pandas** → Facilita la manipulación y análisis de datos mediante estructuras como los DataFrames.  
- **pillow** → Permite la edición de imágenes e inclusión de texto sobre ellas.  

### Instalación de librerías

Para instalar las dependencias, sigue estos pasos en la terminal (CMD):

```bash
pip install requests tqdm ratelimit pandas pillow
````

---

## Ejecución del programa

1. Instala todas las librerías necesarias.
2. Ejecuta el archivo `pokedex_2.py`.
3. El programa pedirá el **número de consultas** (entre 1 y 10).
4. Luego solicitará el **nombre de cada Pokémon**.
5. Para cada consulta, se mostrará:

   * Los datos principales del Pokémon.
   * Una barra de progreso de carga.
   * Una ventana emergente con la imagen y la información integrada.

Además:

* Con cada consulta, se guarda un archivo `.json` dentro de la carpeta `pokedex/`.
* El archivo tendrá como nombre el Pokémon consultado. Ejemplo: `pikachu.json`.
* Estos archivos permanecen guardados para futuras consultas.

---

## Aprendizajes del proyecto

Durante el desarrollo se trabajó en aspectos técnicos importantes:

* Uso de **requests** para realizar peticiones HTTP a la PokeAPI.
* Implementación de `try/except` para manejar errores de conexión o nombres inválidos.
* Manejo de **respuestas en formato JSON** y extracción de información relevante.
* Validación de entradas de usuario para evitar valores vacíos o fuera de rango.
* Uso de **ratelimit** para controlar la frecuencia de peticiones y proteger el sistema.
* Organización de datos con **pandas** en estructuras tabulares (DataFrame).
* Exportación de resultados en archivos `.json` para almacenamiento persistente.
* Uso de **Pillow** para decodificar imágenes en base64 y editarlas.
* Creación de imágenes compuestas con texto informativo sobre la imagen del Pokémon.
* Cálculo dinámico de dimensiones de texto para evitar cortes y mantener la legibilidad.
* Implementación de **tqdm** para barras de progreso en múltiples consultas.
* Importancia de **validar cada módulo** (API, lógica, visualización) antes de avanzar en el desarrollo.

---

## Nota final

Este proyecto está diseñado como una forma **didáctica y accesible** para aprender:

* Cómo funciona una API.
* Cómo procesar datos y mostrarlos de forma organizada.
* Como posterizar un registro en formato json.
* Cómo trabajar con imágenes en Python.

No se requiere experiencia previa en programación para probarlo.

```

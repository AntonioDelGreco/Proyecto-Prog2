from flask import Flask, jsonify,request,Response,render_template
from http import HTTPStatus
import json

app = Flask(__name__)

with open('Archivos_JSON_Proyecto/peliculas.json', encoding='utf-8') as archivo_json1:
    peliculas = json.load(archivo_json1)

@app.route("/")
def home():
    lista_nombres_peliculas=[]
    lista_imagenes_peliculas=[]
    for i in peliculas[::-1]:
        if (len(lista_nombres_peliculas)<10) and (i["nombre"] not in lista_nombres_peliculas):
            lista_nombres_peliculas.append(i["nombre"])
            lista_imagenes_peliculas.append(i["img"])
    #print(lista_nombres_peliculas)
    return Response (render_template("index.html",nombre_peliculas=lista_nombres_peliculas, imagenes_peliculas=lista_imagenes_peliculas),status = HTTPStatus.OK)
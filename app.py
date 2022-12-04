from flask import Flask,request,Response,render_template,redirect,url_for
from http import HTTPStatus
import json

app = Flask(__name__)

with open('Archivos_JSON_Proyecto/peliculas.json', encoding='utf-8') as archivo_json1:
    peliculas = json.load(archivo_json1)


@app.route("/")
@app.route("/peliculas.html",methods=["GET"])
@app.route("/peliculas",methods=["GET"])
def index():
    lista_nombres_peliculas=[]
    lista_imagenes_peliculas=[]
    for i in peliculas[::-1]:
        if (len(lista_nombres_peliculas)<10) and (i["nombre"] not in lista_nombres_peliculas):
            lista_nombres_peliculas.append(i["nombre"])
            lista_imagenes_peliculas.append(i["img"])
    #print(lista_nombres_peliculas)
    
    return Response (render_template("peliculas.html",nombre_peliculas=lista_nombres_peliculas, imagenes_peliculas=lista_imagenes_peliculas),status = HTTPStatus.OK)

@app.route("/peliculas/<info>",methods=["GET"])
def buscar(info):
    return "<h1>" + info + "</h1>"

@app.route("/peliculas",methods=["POST"])
def buscar_post():
    info=request.form["info_buscar"]
    return info
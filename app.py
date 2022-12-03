from flask import Flask, jsonify,request,Response
from http import HTTPStatus
import json

app = Flask(__name__)

with open('Archivos_JSON/usuarios.json', encoding='utf-8') as archivo_json:
    usuarios = json.load(archivo_json)

@app.route("/")
def home():
   return "SISTEMA DE VENTAS DE ENTRADAS PARA EVENTOS ARTISTICOS"

@app.route("/usuarios")
def devolver_usuarios():
    return jsonify(usuarios)

@app.route("/usuarios/<id>", methods=["GET"])
def devolver_usuario(id):
    lista_encontrados=[]
    id_int=int(id)
    for i in usuarios:
        for j in usuarios[i]:
            if j["id"]==id_int:
                lista_encontrados.append(j)
    if len(lista_encontrados)>0:
        return jsonify({"Encontrados":[({"Persona":i}) for i in lista_encontrados]})
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    #Recibir los datos cliente
    datos_cliente=request.get_json()
    #  print(datos_cliente)
    #  print(type(datos_cliente))

    #Encuentro el mayor ID
    mayor=0
    for i in usuarios:
        for j in usuarios[i]:
            if j["id"]>mayor:
                mayor=j["id"]

    # print(mayor)
    id=mayor+1
    # print(id)
    if "Nombre" in datos_cliente:

        [usuarios[i].append({
            "id":id,
            "Nombre":datos_cliente["Nombre"],
            "Apellido":datos_cliente["Apellido"],
            "DNI":datos_cliente["DNI"]
        }) for i in usuarios]

        with open('Archivos_JSON/usuarios.json',"w", encoding='utf-8') as archivo_json:
            json.dump(usuarios,archivo_json)
        
        return Response("Recibido", status=HTTPStatus.OK)
    else:
        return Response("{}", status=HTTPStatus.BAD_REQUEST)

@app.route("/usuarios/actualizar/<string:NombrePersona>", methods=["PUT"])
def actualizar_usuario(NombrePersona):
    encontrado=False
    datos_cliente=request.get_json()
    persona=str(NombrePersona)
    for usuario in usuarios["usuarios"]:
        #print(usuario)
        if usuario["Nombre"] == persona:
            encontrado=True
            usuario["Nombre"]=datos_cliente["Nombre"]
            usuario["Apellido"]=datos_cliente["Apellido"]
            usuario["DNI"]=datos_cliente["DNI"]

    with open('Archivos_JSON/usuarios.json',"w", encoding='utf-8') as archivo_json:
        json.dump(usuarios,archivo_json)

    if encontrado==True:
        return Response("Actualizado", status=HTTPStatus.OK)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)

@app.route("/usuarios/eliminar", methods = ["DELETE"])
def eliminar_usuario():
    datos_cliente = request.get_json()
    if (("Nombre" in datos_cliente) and ("DNI" in datos_cliente)):
        for i in usuarios:
            for usuario in usuarios[i]:
                if ((usuario["Nombre"] == datos_cliente["Nombre"]) and (usuario["DNI"] == datos_cliente["DNI"])):
                    usuarios["usuarios"]=[j for j in usuarios["usuarios"] if j!=usuario]

        with open('Archivos_JSON/usuarios.json',"w", encoding='utf-8') as archivo_json:
            json.dump(usuarios,archivo_json)
        
        return Response("{}", status = HTTPStatus.OK) 
    else:    
        return Response("{}", status = HTTPStatus.BAD_REQUEST)
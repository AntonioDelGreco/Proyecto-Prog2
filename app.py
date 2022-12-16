from flask import Flask,request,Response,render_template,redirect,url_for, session
from http import HTTPStatus
import controller.funciones
import secrets
import json

app = Flask(__name__)
app.secret_key = 'c13d6b2d33bc0b22412c0c723fe5acdd2fb3c941052ce7aed61be9e6cb457d1e' # python -c 'import secrets; print(secrets.token_hex())'

@app.route("/")
def retornar():
  return redirect(url_for("index"),Response=HTTPStatus.OK) #Busca la funcion "index ya definida en 'app'."
  #302 Found indica que el recurso solicitado ha sido movido temporalmente a la URL.

@app.route("/peliculas",methods=["GET"])
def index():
  return Response (render_template("peliculas.html", user=controller.funciones.verify(), nombre_peliculas=controller.funciones.nombresPeliculas(), imagenes_peliculas=controller.funciones.imgPeliculas()), status = HTTPStatus.OK)

@app.route("/buscar/<int:info>",methods=["GET"])
@app.route("/buscar/<info>",methods=["GET"])
def buscar(info):
    lista_encontradas=[]
    peliculas = controller.funciones.moviesFiles()
    for i in peliculas[::-1]:
        #print(i.values())
        for j in i.values():
            if str(info).isnumeric():
                if ((str(info) in str(j)) and (i not in lista_encontradas)) and (len(lista_encontradas)<10):
                    lista_encontradas.append(i)
            else:
                if ((info in str(j)) and (i not in lista_encontradas)) and (len(lista_encontradas)<10):
                      lista_encontradas.append(i)

    return Response (render_template("peliculas.html",
      nombre_peliculas=[i["nombre"] for i in lista_encontradas],
      imagenes_peliculas=[i["img"] for i in lista_encontradas],
      user=controller.funciones.verify()),
      status = HTTPStatus.OK)

@app.route("/buscar", methods=["POST"])
def buscar_post():
    informacion=request.form["info_buscar"]
    #print(informacion)
    return redirect(url_for("buscar", info=informacion, next="edit"), Response=HTTPStatus.OK) 
    #302 Found indica que el recurso solicitado ha sido movido temporalmente a la URL.

#Directores, Generos y Imagenes
# ///////////////////////////////////////////////////////////////////////////////////////////////////
@app.route("/dgi")
def dGI():
  return Response (render_template("dir_gen_img.html", 
  user=controller.funciones.verify(),directores=controller.funciones.directores,
  generos=controller.funciones.generos, imagenes=controller.funciones.pelisConImg()),status=HTTPStatus.OK)

# LOGIN
# ///////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/login', methods=['GET', 'POST'])
@app.route('/perfil', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return redirect(url_for('index'))
  if request.method == 'POST':
    dataUser = {
      "username": request.form['username'],
      "password": request.form['password']
    }
    users = controller.funciones.usersFiles()
    for user in users:
      if dataUser["username"] == user["usuario"] and dataUser["password"] == user["contrasenia"]:
        session["username"] = dataUser['username']
        user = dataUser['username']
      else:
        user = ""
    return Response (render_template("peliculas.html", user=user, nombre_peliculas=controller.funciones.nombresPeliculas(), imagenes_peliculas=controller.funciones.imgPeliculas()), status = HTTPStatus.OK)
  return render_template('perfil.html', user=controller.funciones.verify())


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

# UNA Peli
# ///////////////////////////////////////////////////////////////////////////////////////////////////
  
@app.route('/pelicula/<nombrePelicula>', methods=['GET', 'POST'])
def pelicula(nombrePelicula):
  if request.method == "POST":
    coment = {
      "usuario":session["username"],
      "comentario":request.form["comentario"]
    }
    controller.funciones.hacerComentario(coment, nombrePelicula)
    return redirect(url_for('index'))
  pelis = controller.funciones.moviesFiles()
  for peli in pelis:
    if peli["nombre"] == nombrePelicula:
      unaPeli = peli
      return render_template('comentarios.html', unaPeli=unaPeli, user=controller.funciones.verify(), comentarios=controller.funciones.siHayComentarios(nombrePelicula))
  
# Agregar Pelicula
# ///////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/pelicula/agregar', methods=['GET', 'POST'])
def agregarPelicula():
  if request.method == 'POST':
    pelicula = {
        "id":secrets.token_hex(),
        "nombre":request.form['nombre'],
        "anio":request.form['anio'],
        "fecha_estreno":request.form['estreno'],
        "director":request.form['director'],
        "genero":request.form['genero'],
        "img":request.form['imagen'],
        "comentarios":[
          {
            "idComent":secrets.token_hex(),
            "opinion":request.form['opinion']
          }
        ],
        "sinopsis":request.form['sinopsis']
    }
    controller.funciones.agregarPeliculas(pelicula, session['username'])
  return render_template('agregarPeli.html', directores=controller.funciones.directores, generos=controller.funciones.generos)

# EDICION Y ELIMINACION DE PELICULAS
# ///////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/pelicula/eliminar/<peli>', methods=["GET","POST"])
def eliminarPeli(peli):
  if request.method == "POST":
    controller.funciones.eliminarPeli(peli)
    return redirect(url_for('index'))
  return render_template('eliminarPeli.html', peli=peli, user=controller.funciones.verify())

@app.route("/pelicula/editar/<peli>",methods=["GET","POST"])
def editarPeli(peli):
  pelicula_mod_id=controller.funciones.retornarPeli(peli)["id"]
  if request.method=="POST":
    peliculaEdicion = {
      "id":pelicula_mod_id,
      "nombre":request.form['nombre'],
      "anio":request.form['anio'],
      "fecha_estreno":request.form['estreno'],
      "director":request.form['director'],
      "genero":request.form['genero'],
      "img":request.form['imagen'],
      "sinopsis":request.form['sinopsis']
    }
    controller.funciones.update(peliculaEdicion)
    return redirect(url_for('index'))
  return render_template("editarPeli.html", pelicula_encontrada=controller.funciones.retornarPeli(peli))

# ///////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/all')
def allPelis():
  peliculas = controller.funciones.moviesFiles()
  return Response (render_template("all.html", user=controller.funciones.verify(), all=peliculas), status = HTTPStatus.OK)
# ///////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
  app.run(debug=True)
from flask import Flask,request,Response,render_template,redirect,url_for, session
from http import HTTPStatus
import json

app = Flask(__name__)
app.secret_key = 'secretKey1234567890'

with open('Archivos_JSON_Proyecto/peliculas.json', encoding='utf-8') as archivo_json1:
    peliculas = json.load(archivo_json1)
with open('Archivos_JSON_Proyecto/usuarios.json', encoding='utf-8') as file:
    users = json.load(file)

@app.route("/")
def retornar():
  return redirect(url_for("index"),Response=HTTPStatus.OK) #Busca la funcion "index ya definida en 'app'."
  #302 Found indica que el recurso solicitado ha sido movido temporalmente a la URL.

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

    return Response (render_template("peliculas.html",
    nombre_peliculas=lista_nombres_peliculas,
    imagenes_peliculas=lista_imagenes_peliculas),
    status = HTTPStatus.OK,)

@app.route("/buscar/<int:info>",methods=["GET"])
@app.route("/buscar/<info>",methods=["GET"])
def buscar(info):
    lista_encontradas=[]
    for i in peliculas[::-1]:
        #print(i.values())
        for j in i.values():
            if (info in str(j)) and (i not in lista_encontradas):
                lista_encontradas.append(i)

    return Response (render_template("peliculas.html",
    nombre_peliculas=[i["nombre"] for i in lista_encontradas],
    imagenes_peliculas=[i["img"] for i in lista_encontradas]),
    status = HTTPStatus.OK,)

@app.route("/buscar",methods=["POST"])
def buscar_post():

    informacion=request.form["info_buscar"]
    #print(informacion)

    return redirect(url_for("buscar", info=informacion,next="edit"),Response=HTTPStatus.OK) 
    #302 Found indica que el recurso solicitado ha sido movido temporalmente a la URL.

# LOGIN
# ///////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/login', methods=['GET', 'POST'])
@app.route('/perfil', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return Response(f'Su usuario ya se encuentra en sesion y es {session["username"]}')
  if request.method == 'POST':
    dataUser = {
      "username": request.form['username'],
      "password": request.form['password']
    }
    for user in users:
      if dataUser["username"] in user["usuario"] and dataUser["password"] in user["contrasenia"]:
        session['username'] = dataUser['username']
        return Response(f'Usuario logueado correctamente, su usuario es: {session["username"]}')
      else:
        return Response("Usuario o contraseña incorrectos, intente de nuevo.")
  return render_template('perfil.html')

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('peliculas'))
# ///////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
  app.run(debug=True)
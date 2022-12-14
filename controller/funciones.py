import json
from flask import session

generos = ["accion","aventuras","ciencia ficcion","comedia","documental","drama","fantasia","musical","suspenso","terror","cine mudo","cine 2d","cine 3d","animacion","religiosas","futuristas","policiacas","crimen","belicas","historicas","deportivas","western"]

directores = ['Oriol Paulo', 'Gary Dauberman', 'Justin Lin', 'Chris Sanders, Dean DeBlois', 'Jim Sheridan', 'Joe Russo, Anthony Russo', 'Mel Gibson', 'Luca Guadagnino', 'Rian Johnson', 'Ryan Coogler', 'Rodrigo Sorogoyen', 'Elena López Riera', 'David Owen Russell', 'Álex de la Iglesia', 'Jaume Collet-Serra', 'Isaki Lacuesta', 'Francois Ozon', 'David Gordon Green', 'Carlota Martínez Pereda, Carlota Pereda', 'Jaime Rosales', 'Oriol Paulo', 'Juan Diego Botto', 'Santiago Mitre', 'Alberto Rodríguez Librero']

def moviesFiles():
  with open('./Archivos_JSON_Proyecto/peliculas.json', encoding='utf-8') as archivo_json1:
    peliculas = json.load(archivo_json1)
  return peliculas

def usersFiles():
  with open('./Archivos_JSON_Proyecto/usuarios.json', encoding='utf-8') as archivo_json1:
    users = json.load(archivo_json1)
  return users

def nombresPeliculas():
  nombres = []
  peliculas = moviesFiles()
  for i in peliculas[::-1]:
    if (len(nombres)<10) and (i["nombre"] not in nombres):
        nombres.append(i["nombre"])
  return nombres

def imgPeliculas(): 
  img = []
  peliculas = moviesFiles()
  for i in peliculas[::-1]:
    if (len(img)<10) and (i["img"] not in img):
      img.append(i["img"])
  return img

def agregarPeliculas(pelicula, userSession):
  movies = moviesFiles()
  movies.append(pelicula)
  with open('./Archivos_JSON_Proyecto/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()
  for idCom in pelicula['comentarios']:
    idComentario = idCom['idComent']
  users = usersFiles()
  for user in users:
    if userSession == user['usuario']:
      user['peliculas_comentadas'] = [{
        "idPeli":pelicula['id'],
        "idComentario":idComentario
      }]
  with open('./Archivos_JSON_Proyecto/usuarios.json', 'w') as f:
    json.dump(users, f, indent=4)
    f.close()

def verify():
  if 'username' in session:
    user = session['username']
  else:
    user = ""
  return user

def pelisConImg():
  imagenes=[]
  for i in moviesFiles():
    if i["img"]!="":
      imagenes.append(i["nombre"])
  return imagenes

def retornarPeli(peli):
    for i in moviesFiles():
        if i["nombre"] == peli:
            return i

def siHayComentarios(nombrePeli):
  movies = moviesFiles()
  for movie in movies:
    if movie['nombre'] == nombrePeli:
      if len(movie['comentarios']) > 0:
        return 1
      else:
        return 2

def eliminarPeli(peli):
  movies = moviesFiles()
  for movie in movies:
    if movie['nombre'] == peli:
      movies.remove(movie)
  with open('./Archivos_JSON_Proyecto/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()

def update(peli):
  dataMovies = moviesFiles()
  for movie in dataMovies:
    if peli["id"] == movie["id"]:
      movie["nombre"] = peli["nombre"]
      movie["anio"] = peli["anio"]
      movie["fecha_estreno"] = peli["fecha_estreno"]
      movie["img"] = peli["img"]
      movie["director"] = peli["director"]
      movie["genero"] = peli["genero"]
      movie["sinopsis"] = peli["sinopsis"]
  with open('./Archivos_JSON_Proyecto/peliculas.json', "w") as file:
   json.dump(dataMovies, file, indent=4)
   file.close()

import json
from flask import session

generos = ["accion","aventuras","ciencia ficcion","comedia","documental","drama","fantasia","musical","suspenso","terror","cine mudo","cine 2d","cine 3d","animacion","religiosas","futuristas","policiacas","crimen","belicas","historicas","deportivas","western"]

directores = ['martin scorsese', 'billy wilder', 'steven spielberg', 'federico fellini', 'roman polanski', 'michael haneke', 'francis ford coppola', 'alfred hitchcock', 'terry gilliam', 'stanley kubrick', 'hayao miyazaki', 'isao takahata', 'woody allen', 'george cuckor', 'quentin tarantino', 'darren aronofsky', 'charles chaplin', 'pedro almodovar', 'm. night shyamalan', 'george a. romero']

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
      user['peliculas_comentadas'] = {
        "idPeli":pelicula['id'],
        "idComentario":idComentario
      }
  with open('./Archivos_JSON_Proyecto/usuarios.json', 'w') as f:
    json.dump(users, f, indent=4)
    f.close()
  

def verify():
  if 'username' in session:
    user = session['username']
  else:
    user = ""
  return user

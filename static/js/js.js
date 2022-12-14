const eliminar = document.querySelector(".eliminarPeli");
const eliminacion = document.querySelector("#eliminacion");
const editar = document.querySelector('.editarPeli');
const edicion = document.querySelector('#edicion');
document.addEventListener('DOMContentLoaded',e => {
  if (e.path[0].URL.includes("http://127.0.0.1:5000/pelicula/editar/")) {
    const inicio = editar;
    init(inicio)
  }
  else if (e.path[0].URL.includes("http://127.0.0.1:5000/pelicula/eliminar/")) {
    const inicio = eliminar;
    init(inicio)
  }
  else{
    return null
  }
})


async function init(inicio){
  await inicio.addEventListener("click", e => {
    e.preventDefault();
    const pelicula = e.target.value;
    if (e.target.className === "eliminarPeli") {
      const form = {
        formulario:`
        <label for="eliminar">Esta seguro que desea eliminar: <strong>${pelicula}</strong>? presione eliminar para completar, de lo contrario vuelva al inicio.</label>
        <input type="submit" value="Eliminar" name="eliminar">
        `,
        clas:"eliminar_peli",
        desde: eliminar,
        hacia: eliminacion
      }
      mensaje(form);
    } else {
      const form = {
        formulario:`
        <div>
          <label for="nombre">Nombre de la pelicula:</label>
          <input type="text" name="nombre">
        </div>
        <div>
          <label for="imagen">Imagen:</label>
          <input type="text" name="imagen" required placeholder="La URL de la imagen">
        </div>
        <div>
          <label for="anio">Anio:</label>
          <input type="text" name="anio">
        </div>
        <div>
          <label for="estreno">Fecha de estreno:</label>
          <input type="text" name="estreno" placeholder="1 de Septiembre" required>
        </div>
        <div>
          <label for="estreno">Sinopsis</label>
          <input type="text" name="sinopsis" required>
        </div>
        <div>
            <label for="nombre">Directores disponibles</label>
            <select name="director" required>
              <option disabled selected>Director</option>
              <option value="Oriol Paulo">Oriol Paulo</option>
              <option value="Gary Dauberman">Gary Dauberman</option>
              <option value="Justin Lin">Justin Lin</option>
              <option value="Chris Sanders, Dean DeBlois">Chris Sanders, Dean DeBlois</option>
              <option value="Jim Sheridan">Jim Sheridan</option>
              <option value="Joe Russo, Anthony Russo">Joe Russo, Anthony Russo</option>
              <option value="Mel Gibson">Mel Gibson</option>
              <option value="Luca Guadagnino">Luca Guadagnino</option>
              <option value="Rian Johnson">Rian Johnson</option>
              <option value="Ryan Coogler">Ryan Coogler</option>
              <option value="Rodrigo Sorogoyen">Rodrigo Sorogoyen</option>
              <option value="Elena López Riera">Elena López Riera</option>
              <option value="David Owen Russell">David Owen Russell</option>
              <option value="Álex de la Iglesia">Álex de la Iglesia</option>
              <option value="Jaume Collet-Serra">Jaume Collet-Serra</option>
              <option value="Isaki Lacuesta">Isaki Lacuesta</option>
              <option value="Francois Ozon">Francois Ozon</option>
              <option value="David Gordon Green">David Gordon Green</option>
              <option value="Carlota Martínez Pereda, Carlota Pereda">Carlota Martínez Pereda, Carlota Pereda</option>
              <option value="Jaime Rosales">Jaime Rosales</option>
              <option value="Oriol Paulo">Oriol Paulo</option>
              <option value="Juan Diego Botto">Juan Diego Botto</option>
              <option value="Santiago Mitre">Santiago Mitre</option>
              <option value="Alberto Rodríguez Librero">Alberto Rodríguez Librero</option>
            </select>
          </div>
          <div>
            <label for="nombre">Generos disponibles</label>
            <select name="genero" required>
            <option value="accion">accion</option>
            <option value="aventuras">aventuras</option>
            <option value="ciencia ficcion">ciencia ficcion</option>
            <option value="comedia">comedia</option>
            <option value="documental">documental</option>
            <option value="drama">drama</option>
            <option value="fantasia">fantasia</option>
            <option value="musical">musical</option>
            <option value="suspenso">suspenso</option>
            <option value="terror">terror</option>
            <option value="cine mudo">cine mudo</option>
            <option value="cine 2d">cine 2d</option>
            <option value="cine 3d">cine 3d</option>
            <option value="animacion">animacion</option>
            <option value="religiosas">religiosas</option>
            <option value="futuristas">futuristas</option>
            <option value="policiacas">policiacas</option>
            <option value="crimen">crimen</option>
            <option value="belicas">belicas</option>
            <option value="historicas">historicas</option>
            <option value="deportivas">deportivas</option>
            <option value="western">western</option>
            </select>
          </div>
        <input type="submit" value="editar">
        `,
        clas:"editar_peli",
        desde:editar,
        hacia:edicion
      }
      mensaje(form)
    }
  });
}


function mensaje(form){
  const { formulario, clas, desde, hacia } = form;
  desde.remove();
  const exist = document.querySelector("#alerta-roja");
  if (!exist) {
    const msj = document.createElement("form");
    msj.classList.add(clas);
    msj.id = "alerta-roja";
    msj.method = "POST";
    msj.innerHTML = formulario;
    hacia.appendChild(msj);
  }
}

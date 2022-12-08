var nombre = document.getElementById("nombre").value;
var email = document.getElementById("email").value;
var contraseña = document.getElementById("contraseña").value;
var confirmarcontraseña = document.getElementById("confirmarcontraseña").value;
var telefono = document.getElementById("telefono").value;
var direccion = document.getElementById("direccion").value;

var espacios = false;
var cont = 0;

while (!espacios && (cont < contraseña.length)) {
  if (contraseña.charAt(cont) == " ")
    espacios = true;
  cont++;
}

while (!espacios && (cont < confirmarcontraseña.length)) {
    if (confirmarcontraseña.charAt(cont) == " ")
      espacios = true;
    cont++;
  }
   
if (espacios) {
  alert ("La contraseña no puede contener espacios en blanco");
}

if (nombre.length == 0 || email.length == 0 || contraseña.length == 0 || confirmarcontraseña.length == 0 || telefono.length == 0 || direccion.length == 0) {
    alert("Los campos no pueden quedar vacios");
  }

  if (contraseña != confirmarcontraseña) {
    alert("Las contraseñas deben de coincidir");
  } else {
    alert("Todo esta correcto");
  }
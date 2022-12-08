
var email = document.getElementById("email").value;
var contraseña = document.getElementById("contraseña").value;

var espacios = false;
var cont = 0;

while (!espacios && (cont < contraseña.length)) {
  if (contraseña.charAt(cont) == " ")
    espacios = true;
  cont++;
}

if (espacios) {
  alert ("La contraseña no puede contener espacios en blanco");
}

if (email.length == 0 || contraseña.length == 0 ) {
    alert("Los campos no pueden quedar vacios");
  }

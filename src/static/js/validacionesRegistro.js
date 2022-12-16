const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const nombre = document.getElementById("nombre");
const email = document.getElementById("email");
const password = document.getElementById("password");
const password2 = document.getElementById("password_confirm");
const telefono = document.getElementById("telefono");
const direccion = document.getElementById("direccion");

const campos = {
	email : false,
	password: false,
	nombre: false,
	password2: false,
	telefono: false,
	direccion: false,
}

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const nombreValue = nombre.value.trim();
	const emailValue = email.value.trim();
	const passwordValue = password.value.trim();
	const password2Value = password2.value.trim();
	const telefonoValue = telefono.value.trim();
	const direccionValue = direccion.value.trim();

	// Comparacion del nombre
	if (nombreValue === "") {
		setErrorFor(nombre, "No puede dejar el nombre en blanco.");
		campos['nombre'] = false;
	} else if (!comprobarNombre(nombreValue)) {
		setErrorFor(nombre, "El nombre solo puede tener letras mayusculas, minusculas y espacios.");
		campos['nombre'] = false;
	} else {
		setSuccessFor(nombre);
		campos['nombre'] = true;
	}

	// Comparacion del email
	if (emailValue === "") {
		setErrorFor(email, "No puede dejar el email en blanco.");
		campos['email'] = false;
	} else if (!comprobarEmail(emailValue)) {
		setErrorFor(email, "No ingreso un un formato de email válido.");
		campos['email'] = false;
	} else {
		setSuccessFor(email);
		campos['email'] = true;
	}

	// Comparacion del password
	if (passwordValue === "") {
		setErrorFor(password, "No puede dejar la contraseña en blanco.");
		campos['password'] = false;
	} else if (!comprobarPassword(passwordValue)) {
		setErrorFor(password, "La contraseña debe de contener una minuscula, mayuscula, un numero y un caracter especial, con una longitud minima de 8.");
		campos['password'] = false;
	} else {
		setSuccessFor(password);
		campos['password'] = true;
	}

	// Comparacion del password_confirm
	if (password2Value === "") {
		setErrorFor(password2, "No puede dejar el password en blanco.");
		campos['password2'] = false;
	} else if (passwordValue !== password2Value) {
		setErrorFor(password2, "Las contraseñas no coinciden.");
		campos['password2'] = false;
	} else {
		setSuccessFor(password2);
		campos['password2'] = true;
	}

	// Comparacion del telefono
	if (telefonoValue === "") {
		setErrorFor(telefono, "No puede dejar el teléfono en blanco.");
		campos['telefono'] = false;
	} else if (!comprobarTelefono(telefonoValue)) {
		setErrorFor(telefono, "El telefono debe de contener unicamente valores numericos, sin espacios o caracteres entre números.");
		campos['telefono'] = false;
	} else {
		setSuccessFor(telefono);
		campos['telefono'] = true;
	}

	// Comparacion del Direccion.
	if (direccionValue === "") {
		setErrorFor(direccion, "No puede dejar la dirección en blanco.");
		campos['direccion'] = false;
	} else if (!comprobarDireccion(direccionValue)) {
		setErrorFor(direccion, "No ingreso una dirección válida.");
		campos['direccion'] = false;
	} else {
		setSuccessFor(direccion);
		campos['direccion'] = true;
	}
}

function setErrorFor(input, message) {
	const formControl = input.parentElement;
	const small = formControl.querySelector("small");
	formControl.className = "form-control error";
	small.innerText = message;
}

function setSuccessFor(input) {
	const formControl = input.parentElement;
	formControl.className = "form-control success";
}


function comprobarNombre(nombre) {
    return /^[a-zA-Záéíóú ]{3,50}$/.test(nombre);
}

function comprobarEmail(email) {
	return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}

function comprobarPassword(password) {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,15}$/.test(password);
}

function comprobarTelefono(telefono) {
    return /^[1-9]{2}[0-9]{8}$/.test(telefono);
}

function comprobarDireccion(direccion) {
    return /^[a-zA-Záéíóú0-9./# ]{3,80}$/.test(direccion);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if(campos.email == true  && campos.password == true  && campos.password == true  && campos.nombre == true  && campos.password2 == true  && campos.telefono == true  && campos.direccion == true){
		form.submit();
	}
});
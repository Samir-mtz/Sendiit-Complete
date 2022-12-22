const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const nombre = document.getElementById("Destinatario");
const email = document.getElementById("EmailDestinatario");
const telefono = document.getElementById("TelefonoDestinatario");

const campos = {
	nombre: false,
	email : false,
	telefono: false,
}

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const nombreValue = nombre.value.trim();
	const emailValue = email.value.trim();
	const telefonoValue = telefono.value.trim();

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


function comprobarTelefono(telefono) {
    return /^[1-9]{2}[0-9]{8}$/.test(telefono);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if(campos.email == true  && campos.nombre == true  && campos.telefono == true){
		form.submit();
	}
});
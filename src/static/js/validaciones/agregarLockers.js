const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const ubicacion = document.getElementById("Ubicacion");
const direccion = document.getElementById("Direccion");
const cantidad = document.getElementById("Cantidad");
const latitud = document.getElementById("Latitud");
const longitud = document.getElementById("Longitud");

const campos = {
	ubicacion: false,
	direccion : false,
	cantidad: false,
	latitud: false,
	longitud: false,
}

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const ubicacionValue = ubicacion.value.trim();
	const direccionValue = direccion.value.trim();
	const cantidadValue = cantidad.value.trim();
	const latitudValue = latitud.value.trim();
	const longitudValue = longitud.value.trim();
	
	// Comparacion del Ubicacion.
	if (ubicacionValue === "") {
		setErrorFor(ubicacion, "No puede dejar el campo de ubicaciónn en blanco.");
		campos["ubicacion"] = false;
	}else if (ubicacionValue.length < 8) {
		setErrorFor(ubicacion, "La ubicación debe de tener una longitud mínima de 8 caracteres.");
		campos["ubicacion"] = false;
	}else if (ubicacionValue.length > 40) {
		setErrorFor(ubicacion, "La ubicación debe de tener una longitud máxima de 50 caracteres.");
		campos["ubicacion"] = false;
	}else if (!comprobarUbicacion(ubicacionValue)) {
		setErrorFor(ubicacion, "No ingreso una ubicación válida.");
		campos["ubicacion"] = false;
	} else {
		setSuccessFor(ubicacion);
		campos["ubicacion"] = true;
	}

	// Comparacion del Direccion.
	if (direccionValue === "") {
		setErrorFor(direccion, "No puede dejar el campo de dirección en blanco.");
		campos["direccion"] = false;
	}else if (direccionValue.length < 8) {
		setErrorFor(direccion, "La dirección debe de tener una longitud mínima de 8 caracteres.");
		campos["direccion"] = false;
	}else if (direccionValue.length > 40) {
		setErrorFor(direccion, "La dirección debe de tener una longitud máxima de 50 caracteres.");
		campos["direccion"] = false;
	}else if (!comprobarDireccion(direccionValue)) {
		setErrorFor(direccion, "No ingreso una dirección válida.");
		campos["direccion"] = false;
	} else {
		setSuccessFor(direccion);
		campos["direccion"] = true;
	}

	// Comparacion del Cantidad.
	if (cantidadValue === "") {
		setErrorFor(cantidad, "No puede dejar el campo de cantidad en blanco.");
		campos["cantidad"] = false;
	}else if (cantidadValue < 1) {
		setErrorFor(cantidad, "La cantidad de lockers no puede ser menor a 1.");
		campos["cantidad"] = false;
	}else if (cantidadValue > 10) {
		setErrorFor(cantidad, "La cantidad de lockers no puede ser mayor a 10.");
		campos["cantidad"] = false;
	}else if (!comprobarCantidad(cantidadValue)) {
		setErrorFor(cantidad, "No ingreso una cantidad válida.");
		campos["cantidad"] = false;
	} else {
		setSuccessFor(cantidad);
		campos["cantidad"] = true;
	}

	// Comparacion del Latitud.
	if (latitudValue === "") {
		setErrorFor(latitud, "No puede dejar el campo de latitud en blanco.");
		campos["latitud"] = false;
	}else if (!comprobarLatitud(latitudValue)) {
		setErrorFor(latitud, "No ingreso una latitud válida.");
		campos["latitud"] = false;
	} else {
		setSuccessFor(latitud);
		campos["latitud"] = true;
	}

	// Comparacion del Longitud.
	if (longitudValue === "") {
		setErrorFor(longitud, "No puede dejar el campo de longitud en blanco.");
		campos["longitud"] = false;
	}else if (!comprobarLongitud(longitudValue)) {
		setErrorFor(longitud, "No ingreso una longitud válida.");
		campos["longitud"] = false;
	} else {
		setSuccessFor(longitud);
		campos["longitud"] = true;
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

function comprobarUbicacion(ubicacion) {
	return /^[a-zA-Záéíóú0-9.,/# ]{8,40}$/.test(ubicacion);
}

function comprobarDireccion(direccion) {
	return /^[a-zA-Záéíóú0-9.,/# ]{8,40}$/.test(direccion);
}

function comprobarCantidad(cantidad) {
	return /^\d+$/.test(cantidad);
}

function comprobarLatitud(latitud) {
	return /^[+-]?\d*\.\d+$/.test(latitud);
}

function comprobarLongitud(longitud) {
	return /^[+-]?\d*\.\d+$/.test(longitud);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if(campos.ubicacion == true  && campos.direccion == true  && campos.cantidad == true && campos.latitud == true && campos.longitud == true){
		form.submit();
	}
});
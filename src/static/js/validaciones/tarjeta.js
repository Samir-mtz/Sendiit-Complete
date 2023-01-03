const inputs = document.querySelectorAll("#formulario-tarjeta input");
const selects = document.querySelectorAll("#formulario-tarjeta select");
const form = document.getElementById("formulario-tarjeta");
const numero = document.getElementById("inputNumero");
const nombre = document.getElementById("inputNombre");
const cvv = document.getElementById("inputCCV");
const mes = document.getElementById("selectMes");
const anio = document.getElementById("selectYear");

const campos = {
	numero: false,
	nombre: false,
	cvv: false,
	mes: false,
	anio: false,
};

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

selects.forEach((select) => {
	select.addEventListener("change", checkInputs);
	if(select.id == 'Mes'){
		select.addEventListener("change", mes);
	}
	if(select.id == 'Año'){
		select.addEventListener("change", anio);
	}
});

function checkInputs() {
	const nombreValue = nombre.value.trim();
	const numeroValue = numero.value.trim();
	const cvvValue = cvv.value.trim();

	// Comparacion del nombre
	if (nombreValue === "") {
		setErrorFor(nombre, "No puede dejar el campo de nombre en blanco.");
		campos["nombre"] = false;
	} else if (nombreValue.length < 5) {
		setErrorFor(nombre, "El nombre debe de tener una longitud mínima de 5 caracteres.");
		campos["nombre"] = false;
	} else if (nombreValue.length > 30) {
		setErrorFor(nombre, "El nombre debe de tener una longitud máxima de 30 caracteres.");
		campos["nombre"] = false;
	} else if (!comprobarNombre(nombreValue)) {
		setErrorFor(nombre, "El nombre solo puede tener letras mayusculas, minusculas y espacios.");
		campos["nombre"] = false;
	} else {
		setSuccessFor(nombre);
		campos["nombre"] = true;
	}
	
	// Comparacion del numero de tarjeta
	if (numeroValue === "") {
		setErrorFor(numero, "No puede dejar el campo de número de tarjeta en blanco.");
		campos["numero"] = false;
	} else if (numeroValue.length <= 18) {
		setErrorFor(numero, "El número de tarjeta debe de tener una longitud de 16 caracteres numéricos.");
		campos["numero"] = false;
	}else {
		setSuccessFor(numero);
		campos["numero"] = true;
	}
	
	// Comparacion del CVV
	if (cvvValue === "") {
		setErrorFor(cvv, "Capture el CVV.");
		campos["cvv"] = false;
	} else {
		setSuccessFor(cvv);
		campos["cvv"] = true;
	}

	//comprobar tamaño
	let opcion1 = mes.selectedIndex;
	if(mes.options[opcion1].text != "Mes") {
		campos['mes'] = true;
		setSuccessFor(mes);
	}else{
		setErrorFor(mes, "Selecciona el mes.");
		campos['mes'] = false;
	}

	//comprobar tamaño
	let opcion2 = anio.selectedIndex;
	if(anio.options[opcion2].text != "Año") {
		campos['anio'] = true;
		setSuccessFor(anio);
	}else{
		setErrorFor(anio, "Selecciona el año.");
		campos['anio'] = false;
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
	return /^[a-zA-Záéíóú ]{5,30}$/.test(nombre);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if (
		campos.nombre == true &&
		campos.numero == true &&
		campos.cvv == true &&
		campos.mes == true &&
		campos.anio == true
	) {
		form.submit();
	}
});

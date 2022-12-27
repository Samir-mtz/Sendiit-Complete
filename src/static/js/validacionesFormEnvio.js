const inputs = document.querySelectorAll("#formulario input");
const selects = document.querySelectorAll("#formulario select");
const form = document.getElementById("formulario");
const nombre = document.getElementById("Destinatario");
const email = document.getElementById("EmailDestinatario");
const telefono = document.getElementById("TelefonoDestinatario");
const origen = document.getElementById("Origen");
const destino = document.getElementById("Destino");
const tamano = document.getElementById("Tamaño");
let sucursales = [];
const campos = {
	nombre: false,
	email : false,
	telefono: false,
	origen: false,
	destino: false,
	tamano: false
}

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

selects.forEach((select) => {
	select.addEventListener("change", checkInputs);
	if(select.id == 'Origen'){
		select.addEventListener("change", selecciones);
	}
	if(select.id == 'Destino'){
		select.addEventListener("change", ruta);
		select.addEventListener("change", tamanos);
	}
	
});
function tamanos(){
	let inicio = origen.options[origen.selectedIndex].text
	let fin = destino.options[destino.selectedIndex].text
	const url ="http://127.0.0.1:5000/tamanos/" + inicio + "/"+ fin;
	// console.log(url);
	fetch(url).then(response => response.json())
	.then(data => {
		// sucursales = data.ubicaciones
		var opciones = document.querySelectorAll('#Tamaño option');
		opciones.forEach(o => o.remove());
		let option0 = document.createElement("option");
		option0.text = "Seleccionar";
		tamano.add(option0);
		data.tamanos.forEach((dato)=>{
			
			let option = document.createElement("option");
			option.text=dato
				tamano.add(option);
			}
			);
		})
}

function ruta(){
	let inicio = origen.options[origen.selectedIndex].text
	let fin = destino.options[destino.selectedIndex].text
	if(inicio != "Seleccionar" && fin != "Seleccionar") {
		convertMyRoute(inicio, fin);
	}
}
function getDisponibilidad(){
	const url ="http://127.0.0.1:5000/json"
	fetch(url).then(response => response.json())
	.then(data => {
		// sucursales = data.ubicaciones
		var opciones = document.querySelectorAll('#Origen option');
		opciones.forEach(o => o.remove());
		let option0 = document.createElement("option");
		option0.text = "Seleccionar";
		origen.add(option0);
		data.ubicaciones.forEach((dato)=>{
			let option = document.createElement("option");
			option.text=dato
				origen.add(option);
			}
			);
		})
}

function selecciones(){
	// let option0 = document.createElement("option");
	// let option = document.createElement("option");
	// let option2 = document.createElement("option");
	// let option3 = document.createElement("option");
	// let opcion = origen.selectedIndex;
	// var opciones = document.querySelectorAll('#Destino option');
	let inicio = origen.options[origen.selectedIndex].text
	const url ="http://127.0.0.1:5000/json/" + inicio;
	fetch(url).then(response => response.json())
	.then(data => {
		// sucursales = data.ubicaciones
		var opciones = document.querySelectorAll('#Destino option');
		opciones.forEach(o => o.remove());
		let option0 = document.createElement("option");
		option0.text = "Seleccionar";
		destino.add(option0);
		data.ubicaciones.forEach((dato)=>{
			let option = document.createElement("option");
				option.text=dato
				destino.add(option);
			}
			);
		})
}
function checkInputs() {
	const nombreValue = nombre.value.trim();
	const emailValue = email.value.trim();
	const telefonoValue = telefono.value.trim();
	const origenValue = origen.value.trim();
	const destinoValue = destino.value.trim();
	const tamanoValue = tamano.value.trim();

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
	//comprobar origen
	let opcion = origen.selectedIndex;
	if(origen.options[opcion].text != "Seleccionar") {
		campos['origen'] = true;
		setSuccessFor(origen);
	}else{
		setErrorFor(origen, "Ingresa tu origen.");
		campos['origen'] = false;
	}
	let opcion1 = destino.selectedIndex;
	if(destino.options[opcion1].text != "Seleccionar") {
		campos['destino'] = true;
		setSuccessFor(destino);
	}else{
		setErrorFor(destino, "Ingresa tu destino.");
		campos['destino'] = false;
	}
	let opcion2 = tamano.selectedIndex;
	if(tamano.options[opcion2].text != "Seleccionar") {
		campos['tamano'] = true;
		setSuccessFor(tamano);
	}else{
		setErrorFor(tamano, "Selecciona el tamaño.");
		campos['tamano'] = false;
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
	if(campos.email == true  && campos.nombre == true  && campos.telefono == true && campos.origen == true && campos.destino == true && campos.tamano == true){
		form.submit();
	}
});
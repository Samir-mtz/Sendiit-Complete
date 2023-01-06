const inputs = document.querySelectorAll("#formulario input");
const selects = document.querySelectorAll("#formulario select");
const tarjeta = document.getElementById("Tarjetas");
const form = document.getElementById("formulario");
const nombre = document.getElementById("Destinatario");
const email = document.getElementById("EmailDestinatario");
const telefono = document.getElementById("TelefonoDestinatario");
const origen = document.getElementById("Origen");
const destino = document.getElementById("Destino");
const tamano = document.getElementById("Tamaño");
const peso = document.getElementById("Peso");
const fragil = document.getElementById("cbox");
const numero = document.getElementById("inputNumero");
const nombretarjeta = document.getElementById("inputNombre");
const cvv = document.getElementById("inputCCV");
const mes = document.getElementById("mes");
const anio = document.getElementById("year");

let sucursales = [];
const campos = {
	nombre: false,
	email: false,
	origen: false,
	destino: false,
	tamano: false,
	peso: false,
	numero: true,
	nombretarjeta: true,
	cvv: true,
	mes: true,
	anio: true,
};

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	if (input.id == "Peso") {
		input.addEventListener("keyup", precio);
	}
	input.addEventListener("blur", checkInputs);
});

selects.forEach((select) => {
	select.addEventListener("change", checkInputs);
	if (select.id == "Origen") {
		select.addEventListener("change", selecciones);
	}
	if (select.id == "Destino") {
		select.addEventListener("change", ruta);
		select.addEventListener("change", tamanos);
	}
	if (select.id == "Tamaño") {
		select.addEventListener("change", precio);
	}
	if (select.id == "cbox") {
		select.addEventListener("change", precio);
	}
	if (select.id == "Mes") {
		select.addEventListener("change", mes);
	}
	if (select.id == "Año") {
		select.addEventListener("change", anio);
	}
});
function precio() {
	let inicio = tamano.options[tamano.selectedIndex].value;
	let extra = fragil.options[fragil.selectedIndex].text;

	let valor = 80.0;
	if (inicio == "Mediano(45cm, 35cm, 50cm)") {
		valor += 25.5;
	} else if (inicio == "Grande(85cm, 35cm, 50cm)") {
		valor += 40.5;
	}
	if (extra == "Si") {
		valor += 25;
	}
	valor += 1.5 * peso.value;
	const precio = document.getElementById("precioTotal");
	const iva = document.getElementById("ivaFinal");
	let precioF = document.getElementById("precioFinal");
	const precio2 = document.getElementById("precioTotal2");
	const iva2 = document.getElementById("ivaFinal2");
	let precioF2 = document.getElementById("precioFinal2");
	let iva1 = valor * 0.16;

	precio.innerHTML = "$" + valor.toFixed(2);
	+"MXN";
	iva.innerHTML = "$" + iva1.toFixed(2);
	+"MXN";
	precio2.innerHTML = "$" + valor.toFixed(2);
	+"MXN";
	iva2.innerHTML = "$" + iva1.toFixed(2);
	+"MXN";
	let total = iva1 + valor;
	precioF.innerHTML = "$" + total.toFixed(2);
	+"MXN";
	precioF2.innerHTML = "$" + total.toFixed(2);
	+"MXN";
	let inputCosto = document.getElementById("inputCosto");
	inputCosto.value = total.toFixed(2);
}

function tamanos() {
	let inicio = origen.options[origen.selectedIndex].text;
	let fin = destino.options[destino.selectedIndex].text;
	const url = "http://127.0.0.1:5000/tamanos/" + inicio + "/" + fin;
	// console.log(url);
	fetch(url)
		.then((response) => response.json())
		.then((data) => {
			// sucursales = data.ubicaciones
			var opciones = document.querySelectorAll("#Tamaño option");
			opciones.forEach((o) => o.remove());
			let option0 = document.createElement("option");
			option0.text = "Seleccionar";
			tamano.add(option0);
			data.tamanos.forEach((dato) => {
				let option = document.createElement("option");
				option.text = dato;
				tamano.add(option);
			});
		});
}

function ruta() {
	let inicio = origen.options[origen.selectedIndex].text;
	let fin = destino.options[destino.selectedIndex].text;
	if (inicio != "Seleccionar" && fin != "Seleccionar") {
		convertMyRoute(inicio, fin);
	}
}
function getDisponibilidad() {
	const url = "http://127.0.0.1:5000/json";
	fetch(url)
		.then((response) => response.json())
		.then((data) => {
			// sucursales = data.ubicaciones
			var opciones = document.querySelectorAll("#Origen option");
			opciones.forEach((o) => o.remove());
			let option0 = document.createElement("option");
			option0.text = "Seleccionar";
			origen.add(option0);
			data.ubicaciones.forEach((dato) => {
				let option = document.createElement("option");
				option.text = dato;
				origen.add(option);
			});
		});
}

function selecciones() {
	let inicio = origen.options[origen.selectedIndex].text;
	const url = "http://127.0.0.1:5000/json/" + inicio;
	fetch(url)
		.then((response) => response.json())
		.then((data) => {
			// sucursales = data.ubicaciones
			var opciones = document.querySelectorAll("#Destino option");
			opciones.forEach((o) => o.remove());
			let option0 = document.createElement("option");
			option0.text = "Seleccionar";
			destino.add(option0);
			data.ubicaciones.forEach((dato) => {
				let option = document.createElement("option");
				option.text = dato;
				destino.add(option);
			});
		});
}

function NewTarjeta() {
	let texto = document.getElementById("leyenda");
	texto.style.display = "None";
	let selecto = document.getElementById("guardadas");
	selecto.style.display = "None";
	let formularioTarjeta = document.getElementById("addTarjeta");
	formularioTarjeta.style.display = "Block";
	checkInputs();
}
function Reset() {
	let texto = document.getElementById("leyenda");
	texto.style.display = "Block";
	let selecto = document.getElementById("guardadas");
	selecto.style.display = "Block";
	let formularioTarjeta = document.getElementById("addTarjeta");
	formularioTarjeta.style.display = "None";
	checkInputs();
}

function checkInputs() {
	const nombreValue = nombre.value.trim();
	const emailValue = email.value.trim();
	const telefonoValue = telefono.value.trim();
	const pesoValue = peso.value.trim();
	const nombreTarjetaValue = nombretarjeta.value.trim();
	const numeroValue = numero.value.trim();
	const cvvValue = cvv.value.trim();
	// Comparacion del nombre
	if (nombreValue === "") {
		setErrorFor(nombre, "No puede dejar el nombre en blanco.");
		campos["nombre"] = false;
	} else if (!comprobarNombre(nombreValue)) {
		setErrorFor(nombre, "El nombre solo puede tener letras mayusculas, minusculas y espacios.");
		campos["nombre"] = false;
	} else {
		setSuccessFor(nombre);
		campos["nombre"] = true;
	}
	
	// Comparacion del email
	if (emailValue === "") {
		setErrorFor(email, "No puede dejar el email en blanco.");
		campos["email"] = false;
	} else if (!comprobarEmail(emailValue)) {
		setErrorFor(email, "No ingreso un un formato de email válido.");
		campos["email"] = false;
	} else {
		setSuccessFor(email);
		campos["email"] = true;
	}
	
	// Comparacion del telefono
	if (telefonoValue === "") {
		setErrorFor(telefono, "No puede dejar el teléfono en blanco.");
		campos["telefono"] = false;
	} else if (!comprobarTelefono(telefonoValue)) {
		setErrorFor(
			telefono,
			"El telefono debe de contener unicamente valores numericos, sin espacios o caracteres entre números."
			);
			campos["telefono"] = false;
		} else {
			setSuccessFor(telefono);
			campos["telefono"] = true;
		}
		
		// Comparacion del peso
		if (pesoValue === "") {
			setErrorFor(peso, "No puede dejar el Peso en blanco.");
			campos["peso"] = false;
		} else if (!comprobarPeso(pesoValue)) {
			setErrorFor(
				peso,
			"El peso debe de contener unicamente valores numericos. Los pesos validos son entre 1 y 30 kg. Use 2 decimales de precisión"
			);
			campos["peso"] = false;
		} else {
			setSuccessFor(peso);
			campos["peso"] = true;
		}
		
		//comprobar origen
		let opcion = origen.selectedIndex;
		if (origen.options[opcion].text != "Seleccionar") {
			campos["origen"] = true;
			setSuccessFor(origen);
		} else {
		setErrorFor(origen, "Ingresa tu origen.");
		campos["origen"] = false;
	}
	//comprobar destino
	let opcion1 = destino.selectedIndex;
	if (destino.options[opcion1].text != "Seleccionar") {
		campos["destino"] = true;
		setSuccessFor(destino);
	} else {
		setErrorFor(destino, "Ingresa tu destino.");
		campos["destino"] = false;
	}
	//comprobar tamaño
	let opcion2 = tamano.selectedIndex;
	if (tamano.options[opcion2].text != "Seleccionar") {
		campos["tamano"] = true;
		setSuccessFor(tamano);
	} else {
		setErrorFor(tamano, "Selecciona el tamaño.");
		campos["tamano"] = false;
	}
	
	let formulario2 = document.getElementById('addTarjeta');
	// console.log("entre");
	console.log(formulario2.style.display);
	//comprobar tarjeta
	let tarjetaSelected = tarjeta.selectedIndex;
	// console.log();
	if (formulario2.style.display == "none" && tarjeta.options[tarjetaSelected].text!="Seleccionar") {
		setSuccessFor(tarjeta);
		campos["nombretarjeta"] = true;
		campos["numero"] = true;
		campos["cvv"] = true;
		campos["mes"] = true;
		campos["year"] = true;
	} else {
		setErrorFor(tarjeta, "Selecciona una tarjeta.");
		// Comparacion del nombre de trajeta
		if (nombreTarjetaValue === "") {
			setErrorFor(nombretarjeta, "No puede dejar el campo de nombre de tarjeta en blanco.");
			campos["nombretarjeta"] = false;
		} else if (nombreTarjetaValue.length < 5) {
			setErrorFor(nombretarjeta, "Debe de tener una longitud mínima de 5 caracteres.");
			campos["nombretarjeta"] = false;
		} else if (nombreTarjetaValue.length > 30) {
			setErrorFor(nombretarjeta, "Debe de tener una longitud máxima de 30 caracteres.");
			campos["nombretarjeta"] = false;
		} else if (!comprobarNombreTarjeta(nombreTarjetaValue)) {
			setErrorFor(
				nombretarjeta,
				"Solo puede tener letras mayusculas, minusculas y espacios."
			);
			campos["nombretarjeta"] = false;
		} else {
			setSuccessFor(nombretarjeta);
			campos["nombretarjeta"] = true;
		}

		// Comparacion del numero de tarjeta
		if (numeroValue === "") {
			setErrorFor(numero, "No puede dejar el campo de número de tarjeta en blanco.");
			campos["numero"] = false;
		} else if (!comprobarNumero(numero.value)) {
			setErrorFor(numero, "El numero de tarjeta solo debe tener numeros.");
			campos["numero"] = false;
		} else {
			setSuccessFor(numero);
			campos["numero"] = true;
		}

		// Comparacion del CVV
		if (cvvValue === "") {
			setErrorFor(cvv, "Capture el CVV.");
			campos["cvv"] = false;
		} else if (!comprobarCVV(cvv.value)) {
			setErrorFor(cvv, "El CVV solo puede tener numeros.");
			campos["cvv"] = false;
		} else {
			setSuccessFor(cvv);
			campos["cvv"] = true;
		}

		//comprobar Mes
		let opcion3 = mes.selectedIndex;
		if (mes.options[opcion3].text != "Mes") {
			campos["mes"] = true;
			setSuccessFor(mes);
		} else {
			setErrorFor(mes, "Selecciona el mes.");
			campos["mes"] = false;
		}

		//comprobar Año
		let opcion4 = year.selectedIndex;
		if (year.options[opcion4].text != "Año") {
			campos["year"] = true;
			setSuccessFor(year);
		} else {
			setErrorFor(year, "Selecciona el año.");
			campos["year"] = false;
		}
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

function comprobarNombreTarjeta(nombre) {
	return /^[a-zA-Záéíóú ]{5,30}$/.test(nombre);
}

function comprobarNumero(numero) {
	return /^[1-9]{2}[0-9]{14}$/.test(numero);
}

function comprobarCVV(cvv) {
	return /^[0-9]{3,4}$/.test(cvv);
}

function comprobarNombre(nombre) {
	return /^[a-zA-Záéíóú ]{3,50}$/.test(nombre);
}

function comprobarEmail(email) {
	return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
		email
	);
}

function comprobarTelefono(telefono) {
	return /^[1-9]{2}[0-9]{8}$/.test(telefono);
}

function comprobarPeso(peso) {
	// console.log(peso);
	return /(^[1-9].?([0-9]{2})?$|^1[1-9].?([0-9]{2})?$|^2[1-9].?([0-9]{2})?$|^30$)/.test(peso);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if (
		campos.email == true &&
		campos.nombre == true &&
		campos.peso == true &&
		campos.origen == true &&
		campos.destino == true &&
		campos.tamano == true &&
		campos.numero == true &&
		campos.nombretarjeta == true &&
		campos.cvv == true &&
		campos.mes == true &&
		campos.anio == true
	) {
		form.submit();
	}
});

const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const buscar = document.getElementById("Buscar");

const campos = {
	busacar: false,
};

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const buscarValue = buscar.value.trim();

	// Comparacion del email
	if (buscarValue === "") {
		setErrorFor(buscar, "No puede dejar el campo en blanco.");
		campos["buscar"] = false;
	} else if (!comprobarBuscar(buscarValue)) {
		setErrorFor(buscar, "Debe de ser solo carácteres numéricos.");
		campos["buscar"] = false;
	} else {
		setSuccessFor(buscar);
		campos["buscar"] = true;
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

function comprobarBuscar(buscar) {
	return /^\d*$/.test(buscar);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if (campos.buscar == true) {
		form.submit();
	}
});

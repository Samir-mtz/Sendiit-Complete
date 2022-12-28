const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const password = document.getElementById("password");
const password2 = document.getElementById("password_confirm");

const campos = {
	password: false,
	password2: false,
};

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const passwordValue = password.value.trim();
	const password2Value = password2.value.trim();

	// Comparacion del password
	if (passwordValue === "") {
		setErrorFor(password, "No puede dejar el campo de contraseña en blanco.");
		campos["password"] = false;
	} else if (passwordValue.length < 8) {
		setErrorFor(password, "La contraseña debe de tener una longitud mínima de 8 caracteres.");
		campos["password"] = false;
	} else if (passwordValue.length > 15) {
		setErrorFor(password, "La contraseña debe de tener una longitud máxima de 15 caracteres.");
		campos["password"] = false;
	} else if (!comprobarPassword(passwordValue)) {
		setErrorFor(
			password,
			"La contraseña debe de contener una minuscula, mayuscula, un numero y un caracter especial."
		);
		campos["password"] = false;
	} else {
		setSuccessFor(password);
		campos["password"] = true;
	}

	// Comparacion del password_confirm
	if (password2Value === "") {
		setErrorFor(password2, "No puede dejar el campo de confirmar contraseña en blanco.");
		campos["password2"] = false;
	} else if (passwordValue !== password2Value) {
		setErrorFor(password2, "Las contraseñas no coinciden.");
		campos["password2"] = false;
	} else {
		setSuccessFor(password2);
		campos["password2"] = true;
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

function comprobarPassword(password) {
	return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&-._+])[A-Za-z\d$@$!%*?&-._+]{8,15}$/.test(
		password
	);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if (campos.password == true && campos.password2 == true) {
		form.submit();
	}
});

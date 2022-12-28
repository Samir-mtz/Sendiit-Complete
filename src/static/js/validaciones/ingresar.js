const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const email = document.getElementById("email");
const password = document.getElementById("password");

const campos = {
	email : false,
	password: false,
}

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const emailValue = email.value.trim();
	const passwordValue = password.value.trim();

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
	} else if (passwordValue.length < 8 ) {
		setErrorFor(password, "Debe de tener una longitud mínima de 8 caracteres.");
		campos['password'] = false;
	}else if (passwordValue.length > 15) {
		setErrorFor(password, "Debe de tener una longitud máxima de 15 caracteres.");
		campos['password'] = false;
	} else if (!comprobarPassword(passwordValue)) {
		setErrorFor(password, "Debe de contener una minuscula, mayuscula, un numero y un caracter especial.");
		campos['password'] = false;
	} else {
		setSuccessFor(password);
		campos['password'] = true;
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

function comprobarEmail(email) {
	return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}

function comprobarPassword(password) {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&-._+])[A-Za-z\d$@$!%*?&-._+]{8,15}$/.test(password);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if(campos.email == true  && campos.password == true){
		form.submit();
	}
});
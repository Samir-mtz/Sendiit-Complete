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
	// } else if (!comprobarPassword(passwordValue)) {
	// 	setErrorFor(password, "No ingreso un password válido. La contraseña debe de contener una minuscula, mayuscula y un numero, con una longitud minima de 8.");
	// 	campos['password'] = false;
	// } else {
	// 	setSuccessFor(password);
	// 	campos['password'] = true;
	// }

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

// function comprobarPassword(password) {
// 	return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,15}$/.test(password);
// }


form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if(campos.email == true  && campos.password == true){
		form.submit();
	}
});
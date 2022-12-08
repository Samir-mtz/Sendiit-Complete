// Metodo para abrir las ventanas
const btnAbrirModal = document.querySelector("#btn-ventana");
// Metodo para cerrar las ventanas
const btnCerrarModal = document.querySelector("#modal-btn-cerrar");
// Ventana a ocupar
const modal = document.querySelector("#modal-btn");

btnAbrirModal.addEventListener("click", () => {
    modal.showModal();
})

btnCerrarModal.addEventListener("click", () => {
    modal.close();
})
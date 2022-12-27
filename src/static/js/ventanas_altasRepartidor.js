// Modal de pregunta ¿Desea dar de alta al repartidor?
const btnAbrirModalAlta = document.querySelector(".btn-ventana-alta");              // Metodo para abrir las ventanas
const btnCerrarModalAlta = document.querySelector(".modal-btn-cerrar-alta");        // Metodo para cerrar las ventanas
const modalAlta = document.querySelector(".modal-btn-alta");                        // Ventana a ocupar
// Modal de pregunta ¿Rechazar solicitud de repartidor?
const btnAbrirModalRechazar = document.querySelector(".btn-ventana-rechazar");           // Metodo para abrir las ventanas
const btnCerrarModalRechazar = document.querySelector(".modal-btn-cerrar-rechazar");     // Metodo para cerrar las ventanas
const modalRechazar = document.querySelector(".modal-btn-rechazar");                     // Ventana a ocupar



function abrirAlta(){
    modalAlta.showModal();
}

function cerrarAlta(){
    modalAlta.close();
}



function abrirRechazar(){
    modalRechazar.showModal();
}

function cerrarRechazar(){
    modalRechazar.close();
}
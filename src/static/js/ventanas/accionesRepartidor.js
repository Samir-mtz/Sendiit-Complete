                    // Ventana a ocupar
// Modal de pregunta ¿Desea cambier el estado del locker?
const btnAbrirModalEstado = document.querySelector(".btn-ventana-estado");              // Metodo para abrir las ventanas
const btnCerrarModalEstado = document.querySelector(".modal-btn-cerrar-estado");        // Metodo para cerrar las ventanas
const modalEstado = document.querySelector(".modal-btn-estado");                        // Ventana a ocupar


function abrirEstado(numId){
    myId = document.querySelector('#estado_id');
    myId.value = numId;
    modalEstado.showModal();
}

function cerrarEstado(){
    modalEstado.close();
}

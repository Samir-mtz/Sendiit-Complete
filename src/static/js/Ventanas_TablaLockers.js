// Modal de pregunta ¿Desea agregar un locker?
const btnAbrirModalAgregar = document.querySelector(".btn-ventana-agregar");            // Metodo para abrir las ventanas
const btnCerrarModalAgregar = document.querySelector(".modal-btn-cerrar-agregar");      // Metodo para cerrar las ventanas
const modalAgregar = document.querySelector(".modal-btn-agregar");                      // Ventana a ocupar
// Modal de pregunta ¿Desea cambier el estado del locker?
const btnAbrirModalEstado = document.querySelector(".btn-ventana-estado");              // Metodo para abrir las ventanas
const btnCerrarModalEstado = document.querySelector(".modal-btn-cerrar-estado");        // Metodo para cerrar las ventanas
const modalEstado = document.querySelector(".modal-btn-estado");                        // Ventana a ocupar
// Modal de pregunta ¿Desea editar el locker?
const btnAbrirModalEditar = document.querySelector(".btn-ventana-editar");              // Metodo para abrir las ventanas
const btnCerrarModalEditar = document.querySelector(".modal-btn-cerrar-editar");        // Metodo para cerrar las ventanas
const modalEditar = document.querySelector(".modal-btn-editar");                        // Ventana a ocupar
// Modal de pregunta ¿Desea eliminar el locker?
const btnAbrirModalEliminar = document.querySelector(".btn-ventana-eliminar");           // Metodo para abrir las ventanas
const btnCerrarModalEliminar = document.querySelector(".modal-btn-cerrar-eliminar");     // Metodo para cerrar las ventanas
const modalEliminar = document.querySelector(".modal-btn-eliminar");                     // Ventana a ocupar

function abrirAgregar(){
    modalAgregar.showModal();
}

function cerrarAgregar(){
    modalAgregar.close()
}

function abrirEstado(numId){
    myId = document.querySelector('#estado_id');
    myId.value = numId;
    modalEstado.showModal();
}

function cerrarEstado(){
    modalEstado.close();
}

function abrirEditar(){
    modalEditar.showModal();
}

function cerrarEditar(){
    modalEditar.close();
}

function abrirEliminar(numId){
    myId = document.querySelector('#num_id');
    myId.value = numId;
    modalEliminar.showModal();
}

function cerrarEliminar(){
    modalEliminar.close();
}
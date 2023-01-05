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
const modalEliminar = document.querySelector(".modal-btn-eliminar"); 

const btnAbrirModalRastrear = document.querySelector(".btn-ventana-rastrear");           // Metodo para abrir las ventanas
const btnCerrarModalRastrear = document.querySelector(".modal-btn-cerrar-rastrear");     // Metodo para cerrar las ventanas
const modalRastrear = document.querySelector(".modal-btn-rastrear"); 
// Ventana a ocupar
// Modal de pregunta ¿Desea visualizar al cliente?
const btnAbrirModalVisualziar = document.querySelector(".btn-ventana-visualizar");           // Metodo para abrir las ventanas
const btnCerrarModalVisualizar = document.querySelector(".modal-btn-cerrar-visualizar");     // Metodo para cerrar las ventanas
const modalVisualizar = document.querySelector(".modal-btn-visualizar");                     // Ventana a ocupar

function abrirAgregar(){
    modalAgregar.showModal();
}

function cerrarAgregar(){
    modalAgregar.close()
}

function abrirEstado(numId, statusId){
    myId = document.querySelector('#estado_id');
    myStatus = document.querySelector('#estado_confirmed');
    myId.value = numId;
    myStatus.value = statusId;
    modalEstado.showModal();
}

function cerrarEstado(){
    modalEstado.close();
}

function abrirEditar(numId){
    myId = document.querySelector('#editar_id');
    myId.value = numId;
    modalEditar.showModal();
}

function cerrarEditar(){
    modalEditar.close();
}

function abrirEliminar(numId){
    myId = document.querySelector('#eliminar_id');
    myId.value = numId;
    modalEliminar.showModal();
}

function cerrarEliminar(){
    modalEliminar.close();
}

function abrirVisualizar(numId){
    myId = document.querySelector('#visualizar_id');
    myId.value = numId;
    modalVisualizar.showModal();
}

function cerrarVisualizar(){
    modalVisualizar.close();
}

function abrirRastrear(numId){
    myId = document.querySelector('#rastrear_id');
    myId.value = numId;
    modalRastrear.showModal();
}

function cerrarRastrear(){
    modalRastrear.close();
}
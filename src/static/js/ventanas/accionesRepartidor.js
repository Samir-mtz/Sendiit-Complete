                    // Ventana a ocupar
// Modal de pregunta ¿Desea cambier el estado del locker?
const btnAbrirModalEstado = document.querySelector(".btn-ventana-estado");              // Metodo para abrir las ventanas
const btnCerrarModalEstado = document.querySelector(".modal-btn-cerrar-estado");        // Metodo para cerrar las ventanas
const modalEstado = document.querySelector(".modal-btn-estado");                        // Ventana a ocupar


function abrirEstado(numId){
    myId = document.querySelector('#estado_id');
    myId.value = numId;
    estadoSiguiente(numId);
    modalEstado.showModal();
}

function cerrarEstado(){
    modalEstado.close();
}

function estadoSiguiente(id){
	const url ="http://127.0.0.1:5000/estado/" + id;
	// console.log(url);
	fetch(url).then(response => response.json())
	.then(data => {
		// sucursales = data.ubicaciones
		
		data.estado.forEach((dato)=>{
			
			let texto = document.getElementById('estadoSig');
			let siguiente = "";
			if(dato=="EN ESPERA DEL REPARTIDOR"){
				siguiente="¿Desea actualizar el estado del paquete a \"EN CAMINO\"?"
			}else if(dato == "EN CAMINO"){
				siguiente="¿Desea actualizar el estado del paquete a \"ENTREGADO EN LOCKER DESTINO\"?"
			}else if(dato == "ALMACEN"){
				siguiente="¿Desea actualizar el estado del paquete a \"ENTREGADO EN ALMACEN\"?"
			}
			texto.innerHTML = siguiente;
			}
			);
		})
}

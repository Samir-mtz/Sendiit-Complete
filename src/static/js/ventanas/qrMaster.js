const fullImgBox = document.getElementById("fullImgBox");
const fullImg = document.getElementById("fullImg");

function abrirImagen(reference) {
    fullImgBox.style.display = "flex";
    fullImg.src = reference;
    
}

function cerrarImagen() {
    fullImgBox.style.display = "none";
}


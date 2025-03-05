function showImage(imgElement) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("largeImage");

    // Set the source of the modal image
    modalImg.src = imgElement.src;

    // Display the modal
    modal.style.display = "flex";
}

function closeImage() {
    document.getElementById("imageModal").style.display = "none";
}


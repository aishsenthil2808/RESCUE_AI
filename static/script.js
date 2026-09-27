const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const detectButton = document.getElementById("detectButton");

imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        previewImage.src = imageURL;
        previewImage.style.display = "block";
    }
});

detectButton.addEventListener("click", function () {

    if (!imageInput.files.length) {
        alert("Please upload an image first.");
        return;
    }

    alert("Image uploaded successfully. YOLO detection will be connected next.");
});
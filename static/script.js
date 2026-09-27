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


detectButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    // Prepare image for Flask
    const formData = new FormData();
    formData.append("image", file);

    detectButton.disabled = true;
    detectButton.textContent = "Detecting...";

    try {

        // Send image to Flask backend
        const response = await fetch("/detect", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Update result counts
        document.getElementById("personCount").textContent =
            data.person_count;

        document.getElementById("highCount").textContent =
            data.high_count;

        document.getElementById("mediumCount").textContent =
            data.medium_count;

        document.getElementById("lowCount").textContent =
            data.low_count;

        // Show YOLO processed image
        previewImage.src =
            "data:image/jpeg;base64," + data.image;

        previewImage.style.display = "block";

    } catch (error) {

        console.error(error);

        alert("Something went wrong while detecting.");

    } finally {

        detectButton.disabled = false;
        detectButton.textContent = "Detect Persons";
    }
});
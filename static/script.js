const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const detectButton = document.getElementById("detectButton");


// ===============================
// IMAGE PREVIEW
// ===============================

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (file) {

        const imageURL = URL.createObjectURL(file);

        previewImage.src = imageURL;
        previewImage.style.display = "block";
    }
});


// ===============================
// DETECT PERSON
// ===============================

detectButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {

        alert("Please upload an image first.");
        return;
    }


    // Create FormData
    const formData = new FormData();

    formData.append("image", file);


    // Button loading
    detectButton.disabled = true;
    detectButton.textContent = "Detecting...";


    try {

        // Send image to Flask
        const response = await fetch(
            "http://127.0.0.1:5000/detect",
            {
                method: "POST",
                body: formData
            }
        );


        // Check server response
        if (!response.ok) {

            throw new Error(
                "Server error: " + response.status
            );
        }


        const data = await response.json();


        // Backend error
        if (data.error) {

            alert(data.error);
            return;
        }


        // ===============================
        // UPDATE COUNTS
        // ===============================

        document.getElementById("personCount").textContent =
            data.person_count;

        document.getElementById("highCount").textContent =
            data.high_count;

        document.getElementById("mediumCount").textContent =
            data.medium_count;

        document.getElementById("lowCount").textContent =
            data.low_count;


        // ===============================
        // SHOW DETECTED IMAGE
        // ===============================

        previewImage.src =
            "data:image/jpeg;base64," + data.image;

        previewImage.style.display = "block";


    } catch (error) {

        console.error(
            "Detection error:",
            error
        );

        alert(
            "Detection error: " +
            error.message
        );


    } finally {

        detectButton.disabled = false;

        detectButton.textContent =
            "Detect Persons";
    }

});
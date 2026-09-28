const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const detectButton = document.getElementById("detectButton");

// ========================================
// IMAGE PREVIEW
// ========================================

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    // Show uploaded image immediately
    const imageURL = URL.createObjectURL(file);

    previewImage.src = imageURL;
    previewImage.style.display = "block";
});


// ========================================
// DETECT PERSONS
// ========================================

detectButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    // Create FormData
    const formData = new FormData();
    formData.append("image", file);

    // Button loading state
    detectButton.disabled = true;
    detectButton.textContent = "Detecting...";

    try {

        console.log("Sending image to Flask...");

        const response = await fetch("/detect", {
            method: "POST",
            body: formData
        });

        console.log("Server status:", response.status);

        // Get response as text first
        const responseText = await response.text();

        console.log("Server response:", responseText);

        // Check server error
        if (!response.ok) {

            alert(
                "Server Error: " +
                response.status +
                "\n\n" +
                responseText
            );

            return;
        }

        // Convert response to JSON
        let data;

        try {
            data = JSON.parse(responseText);
        } catch (jsonError) {

            console.error("JSON Error:", jsonError);

            alert(
                "Flask server JSON response kudukkala.\n\n" +
                "Terminal-la red error irukka nu check pannunga."
            );

            return;
        }

        // Backend error
        if (data.error) {

            alert("Error: " + data.error);

            return;
        }


        // ========================================
        // UPDATE COUNTS
        // ========================================

        document.getElementById("personCount").textContent =
            data.person_count ?? 0;

        document.getElementById("highCount").textContent =
            data.high_count ?? 0;

        document.getElementById("mediumCount").textContent =
            data.medium_count ?? 0;

        document.getElementById("lowCount").textContent =
            data.low_count ?? 0;


        // ========================================
        // SHOW YOLO RESULT IMAGE
        // ========================================

        if (data.image) {

            previewImage.src =
                "data:image/jpeg;base64," + data.image;

            previewImage.style.display = "block";
        }


        // Success message
        if ((data.person_count ?? 0) > 0) {

            alert(
                "Detection complete!\n\n" +
                "Persons detected: " +
                data.person_count
            );

        } else {

            alert(
                "Detection complete.\n\n" +
                "No person detected in this image."
            );
        }

    } catch (error) {

        console.error("Detection error:", error);

        alert(
            "Flask server connect aagala.\n\n" +
            "Terminal-la app.py running ah irukka nu check pannunga."
        );

    } finally {

        // Reset button
        detectButton.disabled = false;
        detectButton.textContent = "Detect Persons";
    }
});
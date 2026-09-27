from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Load YOLO model
model = YOLO("yolo11n.pt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    # Read uploaded image
    image_bytes = file.read()

    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        return jsonify({
            "error": "Invalid image"
        }), 400

    # YOLO detection
    results = model(
        frame,
        conf=0.15,
        classes=[0],
        verbose=False
    )

    person_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    # Process detections
    for result in results:

        for box in result.boxes:

            confidence = float(box.conf[0])

            person_count += 1

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            # Priority
            if confidence >= 0.70:

                priority = "HIGH"
                high_count += 1

            elif confidence >= 0.40:

                priority = "MEDIUM"
                medium_count += 1

            else:

                priority = "LOW"
                low_count += 1

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )

            # Label
            label = (
                f"PERSON | "
                f"{confidence:.2f} | "
                f"{priority}"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # Convert image to JPG
    success, encoded_image = cv2.imencode(
        ".jpg",
        frame
    )

    if not success:
        return jsonify({
            "error": "Could not process image"
        }), 500

    # Convert to Base64
    image_base64 = base64.b64encode(
        encoded_image
    ).decode("utf-8")

    # Send result to JavaScript
    return jsonify({
        "person_count": person_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "image": image_base64
    })


if __name__ == "__main__":
    app.run(debug=True)
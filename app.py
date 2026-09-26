import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

# Load YOLO model
model = YOLO("yolo11n.pt")

# Page settings
st.set_page_config(
    page_title="Rescue AI",
    page_icon="🚨",
    layout="wide"
)

# Title
st.title("🚨 RESCUE AI")
st.subheader("Advanced Human Detection in Collapsed Structures")

st.write(
    "Upload a disaster or collapsed-structure image "
    "to detect possible human presence."
)

# Upload image
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file)
    frame = np.array(image)

    # Run YOLO
    results = model(frame, verbose=False)

    person_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    # Process detections
    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Person only
            if class_id == 0:

                person_count += 1

                # Bounding box
                x1, y1, x2, y2 = map(
                    int, box.xyxy[0].tolist()
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
                    2
                )

                # Label
                label = f"Person {person_count} | {confidence:.2f} | {priority}"

                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    # Display result
    st.image(
        frame,
        caption="Detection Result",
        use_container_width=True
    )

    # Results
    st.subheader("📊 Detection Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Persons Detected", person_count)
    col2.metric("High Confidence", high_count)
    col3.metric("Medium Confidence", medium_count)
    col4.metric("Low Confidence", low_count)

    if person_count > 0:
        st.success("Possible human presence detected.")
    else:
        st.warning("No person detected in this image.")
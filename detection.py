from ultralytics import YOLO
import os
import cv2

# Load YOLO model
model = YOLO("yolo11n.pt")

# Test categories
folders = ["normal", "occluded", "disaster"]

# Create output folder
os.makedirs("output_images", exist_ok=True)


# Function to identify zone
def get_zone(center_x, image_width):

    if center_x < image_width / 3:
        return "ZONE A - LEFT"

    elif center_x < (2 * image_width) / 3:
        return "ZONE B - CENTER"

    else:
        return "ZONE C - RIGHT"


for folder in folders:

    folder_path = os.path.join("test_images", folder)

    print("\n================================")
    print("CATEGORY:", folder.upper())
    print("================================")

    for image in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image)

        # Read image
        frame = cv2.imread(image_path)

        if frame is None:
            print("Could not read:", image)
            continue

        image_height, image_width = frame.shape[:2]

        # Run YOLO
        results = model(image_path, verbose=False)

        person_count = 0

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

                    # Center point
                    center_x = (x1 + x2) / 2

                    # Zone
                    zone = get_zone(center_x, image_width)

                    # Priority
                    if confidence >= 0.70:
                        priority = "HIGH"

                    elif confidence >= 0.40:
                        priority = "MEDIUM"

                    else:
                        priority = "LOW"

                    # Draw bounding box
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    # Label
                    label = (
                        f"Person {person_count} | "
                        f"{confidence:.2f} | "
                        f"{priority}"
                    )

                    cv2.putText(
                        frame,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

                    # Zone label
                    cv2.putText(
                        frame,
                        zone,
                        (x1, y2 + 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2
                    )

        # Output filename
        output_name = f"{folder}_{image}"

        output_path = os.path.join(
            "output_images",
            output_name
        )

        # Save processed image
        cv2.imwrite(output_path, frame)

        print(
            f"{image} → "
            f"{person_count} person(s) detected"
        )

print("\n================================")
print("DONE!")
print("Check the 'output_images' folder.")
print("================================")
import cv2
from ultralytics import YOLO
from aircraft_classifier import classify_aircraft

model = YOLO("C:/Users/ASAF/Desktop/project_codes/project/uses_modles/v8m_10epoch.pt")
names = model.names

def process_image(img):
    results = model(img)
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, score, cls_id = box.tolist()
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cls_name = names[int(cls_id)]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{cls_name} ({score:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if cls_name == "plane":
                crop = img[y1:y2, x1:x2]
                aircraft_type = classify_aircraft(crop)
                cv2.putText(img, f"{aircraft_type}", (x1, y2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    return img

def detect_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("[!] Görsel yüklenemedi.")
        return
    annotated = process_image(img)
    cv2.imshow("Tespit Sonucu", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

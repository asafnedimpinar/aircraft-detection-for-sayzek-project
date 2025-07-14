import cv2
from model_loader import get_model_and_names  # Dinamik model erişimi
from aircraft_classifier import classify_aircraft

def resize_to_screen(img, screen_res=(1280, 720)):
    h, w = img.shape[:2]
    scale_w = screen_res[0] / w
    scale_h = screen_res[1] / h
    scale = min(scale_w, scale_h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h))

def process_image(img, conf_thresh=0.35, iou_thresh=0.35):
    model, names = get_model_and_names()  # Güncel modeli buradan al

    results = model(img, conf=conf_thresh, iou=iou_thresh)
    drawn_boxes = []

    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, score, cls_id = box.tolist()
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cls_name = names[int(cls_id)]
            box_coords = (x1, y1, x2, y2)

            drawn_boxes.append((x1, y1, x2, y2, score, cls_name))

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{cls_name} ({score:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if cls_name == "airplane":
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

    img = resize_to_screen(img, screen_res=(720, 720))
    try:
        annotated = process_image(img)
    except Exception as e:
        print(f"[!] İşleme hatası: {e}")
        return

    cv2.imshow("🖼️ Tespit Sonucu", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

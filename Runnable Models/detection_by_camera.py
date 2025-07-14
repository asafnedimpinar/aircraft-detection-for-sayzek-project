import cv2
import time
from model_loader import get_model_and_names
from aircraft_classifier import classify_aircraft

# 🎯 Ayarlar
CONFIDENCE_THRESHOLD = 0.35
MIN_BOX_AREA = 500
SCREEN_RES = (1280, 720)

def resize_to_screen(img, screen_res=SCREEN_RES):
    h, w = img.shape[:2]
    scale = min(screen_res[0] / w, screen_res[1] / h)
    return cv2.resize(img, (int(w * scale), int(h * scale)))

def detect_from_camera():
    try:
        model, names = get_model_and_names()
    except Exception as e:
        print(f"[!] Model yüklenemedi: {e}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Kameraya erişilemiyor.")
        return

    print("[INFO] Kamera başlatıldı. Çıkmak için 'q' tuşuna basın.")
    frame_fail_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[!] Kare alınamadı, yeniden deneniyor...")
            frame_fail_count += 1
            if frame_fail_count > 5:
                print("[!] Art arda 5 kare alınamadı, kamera sonlandırılıyor.")
                break
            continue
        frame_fail_count = 0

        frame = resize_to_screen(frame)
        start_time = time.time()

        try:
            results = model(frame, conf=CONFIDENCE_THRESHOLD)[0]
        except Exception as e:
            print(f"[!] Model tahmin hatası: {e}")
            continue

        print(f"[INFO] Inference süresi: {time.time() - start_time:.2f} saniye")

        for box in results.boxes.data:
            x1, y1, x2, y2, score, cls_id = box.tolist()
            if score < CONFIDENCE_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            if (x2 - x1) * (y2 - y1) < MIN_BOX_AREA:
                continue

            cls_index = int(cls_id)
            cls_name = names.get(cls_index, "Bilinmeyen")
            print(f"[DETECTED] {cls_name} - Güven: {score:.2f}")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{cls_name} ({score:.2f})"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # ✈️ Uçak tipi sınıflandırması
            if cls_name.lower() == "airplane":
                crop = frame[y1:y2, x1:x2]
                if crop.shape[0] > 64 and crop.shape[1] > 64:
                    aircraft_type = classify_aircraft(crop)
                else:
                    aircraft_type = "Tespit Güvensiz"
                print(f"🛫 Uçak Tipi: {aircraft_type}")
                cv2.putText(frame, aircraft_type, (x1, y2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        try:
            cv2.imshow("📷 Canlı Kamera Tespiti", frame)
        except cv2.error as e:
            print(f"[!] Görüntü gösterilemiyor: {e}")
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Kamera tespiti sonlandırıldı.")

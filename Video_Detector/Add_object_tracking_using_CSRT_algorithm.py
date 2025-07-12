import cv2
from ultralytics import YOLO
from aircraft_classifier import classify_aircraft

# YOLO modelini yükle
model = YOLO("C:/Users/ASAF/Desktop/project_codes/project/uses_modles/v8m_10epoch.pt")
names = model.names

# Global değişkenler
active_trackers = {}
object_counts = {}
CONFIDENCE_THRESHOLD = 0.5
MIN_BOX_AREA = 500
TRACKER_FAILURE_LIMIT = 10  # CSRT için başarısızlık eşiği

def create_tracker():
    return cv2.TrackerCSRT_create()

def calculate_iou(box1, box2):
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0.0
    box1Area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2Area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    return interArea / float(box1Area + box2Area - interArea + 1e-5)

def detect_and_track(frame, frame_index):
    global active_trackers, object_counts

    if frame_index % 30 == 0:
        results = model(frame)[0]
        for i, box in enumerate(results.boxes.data):
            x1, y1, x2, y2, score, cls_id = box.tolist()
            if score < CONFIDENCE_THRESHOLD:
                continue
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            area = (x2 - x1) * (y2 - y1)
            if area < MIN_BOX_AREA:
                continue

            cls_name = names[int(cls_id)]
            new_box = (x1, y1, x2, y2)

            matched = False
            for obj in active_trackers.values():
                tx, ty, tw, th = obj["last_box"]
                tracked_box = (tx, ty, tx + tw, ty + th)
                if calculate_iou(tracked_box, new_box) > 0.5:
                    matched = True
                    break

            if not matched:
                tracker = create_tracker()
                tracker.init(frame, (x1, y1, x2 - x1, y2 - y1))
                obj_id = f"{cls_name}_{frame_index}_{i}"
                active_trackers[obj_id] = {
                    "tracker": tracker,
                    "label": cls_name,
                    "counted": False,
                    "fail_count": 0,
                    "last_box": (x1, y1, x2 - x1, y2 - y1)
                }

    for obj_id in list(active_trackers.keys()):
        obj = active_trackers[obj_id]
        tracker = obj["tracker"]
        label = obj["label"]

        success, bbox = tracker.update(frame)
        x, y, w, h = map(int, bbox)
        obj["last_box"] = (x, y, w, h)

        if success:
            obj["fail_count"] = 0
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if label == "plane" and not obj["counted"]:
                crop = frame[y:y + h, x:x + w]
                if crop.shape[0] > 64 and crop.shape[1] > 64:
                    aircraft_type = classify_aircraft(crop)
                else:
                    aircraft_type = "Tespit Güvensiz"

                cv2.putText(frame, aircraft_type, (x, y + h + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                obj["counted"] = True
                object_counts[aircraft_type] = object_counts.get(aircraft_type, 0) + 1
        else:
            obj["fail_count"] += 1
            if obj["fail_count"] > TRACKER_FAILURE_LIMIT:
                del active_trackers[obj_id]

    return frame

def detect_from_video(video_path):
    global active_trackers, object_counts
    active_trackers = {}
    object_counts = {}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("[!] Video açılamadı.")
        return

    screen_res = (1280, 720)
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        scale = min(screen_res[0] / width, screen_res[1] / height)
        frame = cv2.resize(frame, (int(width * scale), int(height * scale)))

        annotated = detect_and_track(frame, frame_index)
        cv2.imshow("Video Tespiti", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or cv2.getWindowProperty("Video Tespiti", cv2.WND_PROP_VISIBLE) < 1:
            break

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

    print("\n📊 Video Özeti:")
    if object_counts:
        for obj, count in object_counts.items():
            print(f"🔸 {obj}: {count} adet tespit edildi.")
    else:
        print("Hiç nesne tespit edilemedi.")

import cv2
import numpy as np
import json
from model_loader import get_aircraft_model  # 🔄 model_loader'dan doğru fonksiyon

# ✨ Modeli dinamik olarak yükle
model = get_aircraft_model("resnet50")

# ✨ Sınıf isimlerini yükle
with open("C:/Users/ASAF/Desktop/project_codes/project/uses_models/classfier/class_names.json", "r") as f:
    class_names = json.load(f)

IMG_SIZE = (224, 224)

def preprocess(img):
    """Resmi modele uygun şekilde hazırla (224x224, RGB, normalize)"""
    img = cv2.resize(img, IMG_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)

def classify_aircraft(image, use_tta=True):
    """Uçak resmini sınıflandırır. TTA ile flipli tahmin yapar."""
    try:
        preds = []

        if use_tta:
            for flip in [False, True]:
                aug_img = cv2.flip(image, 1) if flip else image
                input_img = preprocess(aug_img)
                pred = model.predict(input_img, verbose=0)
                preds.append(pred)
            final_pred = np.mean(preds, axis=0)[0]
        else:
            input_img = preprocess(image)
            final_pred = model.predict(input_img, verbose=0)[0]

        max_idx = int(np.argmax(final_pred))
        confidence = float(final_pred[max_idx])
        predicted_label = class_names[max_idx] if max_idx < len(class_names) else "Bilinmeyen"

        print(f"[✓] Tahmin: {predicted_label}")
        print(f"[✓] Güven: {confidence:.2f}")
        print(f"[✓] Vektör: {np.round(final_pred, 3).tolist()}")

        return f"{predicted_label} ({confidence:.2f})"

    except Exception as e:
        print(f"[!] Tahmin hatası: {e}")
        return "Tespit Edilemedi (0.00)"

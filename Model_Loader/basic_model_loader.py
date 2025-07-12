from ultralytics import YOLO

# Model nesnesi ve sınıf isimleri
model = None
names = []

def load_model_by_type(model_type):
    """
    'kara' veya 'hava' tipine göre modeli ve sınıf isimlerini yükler.
    """
    global model, names

    if model_type == "kara":
        model_path = "C:/Users/ASAF/Desktop/project_codes/project/uses_modles/onland/v8m_50epoch.pt"
    elif model_type == "hava":
        model_path = "C:/Users/ASAF/Desktop/project_codes/project/uses_modles/airborne/v8m_50epoch.pt"
    else:
        raise ValueError("Model tipi 'kara' veya 'hava' olmalıdır.")

    model = YOLO(model_path)
    names = model.names
    print(f"[✓] {model_type.upper()} modeli yüklendi.")

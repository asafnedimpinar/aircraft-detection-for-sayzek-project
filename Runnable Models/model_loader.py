from ultralytics import YOLO
from keras.models import load_model

# Model nesnesi ve sınıf isimleri
model = None
names = []

def load_model_by_type(model_type):
    """
    'kara' veya 'hava' tipine göre modeli ve sınıf isimlerini yükler.
    """
    global model, names

    if model_type == "kara":
        model_path = "C:/Users/ASAF/Desktop/project_codes/project/uses_models/onland/v8m_50epoch.pt" # karadaki nesnler  model yolonu giriniz 
    elif model_type == "hava":
        model_path = "C:/Users/ASAF/Desktop/project_codes/project/uses_models/airborne/best (3).pt" # havaadaki nesneler model dosyası yolunu giriniz
    else:
        raise ValueError("Model tipi 'kara' veya 'hava' olmalıdır.")

    model = YOLO(model_path)
    names = model.names
    print(f"[✓] {model_type.upper()} modeli yüklendi.")

def get_model_and_names():
    """
    Yüklü modeli ve sınıf isimlerini döndürür. Eğer model henüz yüklenmediyse hata verir.
    """
    if model is None:
        raise ValueError("Model henüz yüklenmedi. Lütfen önce load_model_by_type() çağırın.")
    
    return model, names

def get_aircraft_model(model_name):
    model_paths = {
        "resnet50": "C:/Users/ASAF/Desktop/project_codes/project/uses_models/classfier/resnet50.h5",
        
    }
    if model_name not in model_paths:
        raise ValueError(f"Model '{model_name}' bulunamadı.")
    return load_model(model_paths[model_name])
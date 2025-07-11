
import os
import shutil

# Mevcut klasör yolu (veri setinin bulunduğu klasör)
data_dir = "C:/Users/ASAF/Desktop/skymonioring"# burayı kendi klasör yolunla değiştir

# Hedef klasör yolları
labels_dir = os.path.join(data_dir, "labels")
images_dir = os.path.join(data_dir, "images")

# Klasörler yoksa oluştur
os.makedirs(labels_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

# Dosyaları ayır
for file_name in os.listdir(data_dir):
    full_path = os.path.join(data_dir, file_name)
    if os.path.isfile(full_path):
        if file_name.endswith(".txt"):
            shutil.move(full_path, os.path.join(labels_dir, file_name))
        elif file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            shutil.move(full_path, os.path.join(images_dir, file_name))

print("Dosyalar başarıyla ayrıldı.")

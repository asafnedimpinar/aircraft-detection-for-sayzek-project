import os

# 📁 Görsel ve etiket klasör yolları
images_dir = r"C:/Users/ASAF/Desktop/airborne/images"
labels_dir = r"C:/Users/ASAF/Desktop/airborne/labels"

# 🏷️ Etiket dosya adları (uzantısız)
label_files = set(os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith(".txt"))

# 📸 Görselleri kontrol et
for image_file in os.listdir(images_dir):
    if image_file.lower().endswith((".jpg", ".jpeg", ".png")):
        image_name = os.path.splitext(image_file)[0]
        if image_name not in label_files:
            image_path = os.path.join(images_dir, image_file)
            os.remove(image_path)
            print(f"[🗑️] Etiket yok, görsel silindi: {image_path}")
        else:
            print(f"[✔️] Eşleşti: {image_file}")

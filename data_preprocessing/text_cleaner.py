import os

# Görsel ve etiket klasör yolları
images_dir = r"C:/Users/ASAF/Desktop/veri_işlemleri/images"
labels_dir = r"C:/Users/ASAF/Desktop/veri_işlemleri/labels"

# Görsel dosyalarının isimlerini al (uzantısız)
image_files = set(os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".jpeg", ".png")))

# Label dosyalarını kontrol et
for label_file in os.listdir(labels_dir):
    if label_file.endswith(".txt"):
        label_name = os.path.splitext(label_file)[0]
        if label_name not in image_files:
            label_path = os.path.join(labels_dir, label_file)
            os.remove(label_path)
            print(f"[🗑️] Silindi: {label_path}")
        else:
            print(f"[✔️] Eşleşti: {label_file}")

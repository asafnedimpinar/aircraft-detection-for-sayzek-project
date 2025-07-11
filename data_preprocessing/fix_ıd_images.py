import os

# Etiket dosyalarının bulunduğu klasör
labels_path = r"C:/Users/ASAF/Desktop/airborne/labels"

# Tüm .txt dosyalarını kontrol et
for filename in os.listdir(labels_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(labels_path, filename)
        with open(file_path, "r") as f:
            lines = f.readlines()

        # En az bir satırda etiket id'si 3 var mı?
        has_id_3 = any(line.strip().startswith("3") for line in lines)

        # Eğer yoksa dosyayı sil
        if not has_id_3:
            print(f"Siliniyor: {filename}")  # Önizleme
            os.remove(file_path)

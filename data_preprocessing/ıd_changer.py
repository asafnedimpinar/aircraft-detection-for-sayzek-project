import os

# Etiket klasörlerinin yolları
label_dirs = [
    r"C:/Users/ASAF/Desktop/plane_faraway/test/labels",
    r"C:/Users/ASAF/Desktop/plane_faraway/train/labels",
    r"C:/Users/ASAF/Desktop/plane_faraway/val/labels",
]
def convert_class_ids(folder_path, from_id='0', to_id='2'):
    print(f"\nİşleniyor: {folder_path}")
    for file_name in os.listdir(folder_path):
        if not file_name.endswith('.txt'):
            continue  # Sadece .txt dosyalarını işle

        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"HATA (okuma): {file_path} - {e}")
            continue

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts and parts[0] == from_id:
                parts[0] = to_id
            new_lines.append(' '.join(parts) + '\n')

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"HATA (yazma): {file_path} - {e}")

# Her klasördeki etiket dosyalarını dönüştür
for directory in label_dirs:
    convert_class_ids(directory)

print("\n✅ Tüm class_id: 0 → 2 olarak değiştirildi.")

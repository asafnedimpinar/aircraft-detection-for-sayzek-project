
import os
from collections import Counter
"""
# root klasör (örneğin: veri setinin bulunduğu ana klasör)
dataset_root = r"C:/Users/ASAF/Desktop/main_detect_dataset"

# alt klasörler (her biri içinde labels klasörü var)
subdirs = ["train", "test", "val"]

# Class ID sayacı
class_counter = Counter()

# Her alt klasördeki labels içindeki txt dosyalarını işle
for subdir in subdirs:
    labels_path = os.path.join(dataset_root, subdir, "labels")
    if not os.path.exists(labels_path):
        print(f"❗ Uyarı: {labels_path} klasörü bulunamadı, atlanıyor.")
        continue

    print(f"\n🔍 Tarama: {labels_path}")
    for file_name in os.listdir(labels_path):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(labels_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if parts:
                        class_id = parts[0]
                        class_counter[class_id] += 1
        except Exception as e:
            print(f"HATA: {file_path} - {e}")

# Sonuçları yazdır
print("\n📊 Class ID Sayımları:")
for class_id in sorted(class_counter.keys(), key=int):
    print(f"Class {class_id}: {class_counter[class_id]} adet")

"""
"""


import os
from collections import Counter

# Ana klasör yolu
dataset_root = r"C:/Users/ASAF/Desktop/main_detect_dataset"
# Alt klasörler
subdirs = ["train", "test", "valid"]

# Her alt klasör için ayrı class_id sayacı
all_counts = {}

for subdir in subdirs:
    labels_path = os.path.join(dataset_root, subdir, "labels")
    if not os.path.exists(labels_path):
        print(f"❗ Uyarı: {labels_path} klasörü bulunamadı, atlanıyor.")
        continue

    print(f"\n🔍 Tarama: {labels_path}")
    class_counter = Counter()

    for file_name in os.listdir(labels_path):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(labels_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if parts:
                        class_id = parts[0]
                        class_counter[class_id] += 1
        except Exception as e:
            print(f"HATA: {file_path} - {e}")

    all_counts[subdir] = class_counter

# Her alt klasör için sonuçları yazdır
print("\n📊 Her klasör için Class ID Sayımları:")
for subdir in subdirs:
    print(f"\n📁 {subdir.upper()} klasörü:")
    counter = all_counts.get(subdir, {})
    if not counter:
        print("  Veri bulunamadı.")
        continue
    for class_id in sorted(counter.keys(), key=int):
        print(f"  Class {class_id}: {counter[class_id]} adet")

"""
import os
import os
import shutil
import optuna
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import numpy as np

# 🔧 Dosya yolları
base_path = r"C:/Users/ASAF/Desktop/veri_işlemleri"
images_dir = os.path.join(base_path, "images")
labels_dir = os.path.join(base_path, "labels")

# 📥 Tüm verileri topla
image_paths = glob(os.path.join(images_dir, "*.jpg")) + glob(os.path.join(images_dir, "*.png"))
all_labels = []

# 📤 Her görüntü için sınıf etiketini label dosyasından al
for img_path in image_paths:
    label_path = img_path.replace("\\images\\", "\\labels\\").replace(".jpg", ".txt").replace(".png", ".txt")
    try:
        with open(label_path, "r") as f:
            lines = f.readlines()
            if lines:
                class_id = int(lines[0].split()[0])  # YOLO: class x y w h
            else:
                class_id = -1  # boş dosya varsa
    except FileNotFoundError:
        class_id = -1
    all_labels.append(class_id)

# ❌ Etiketsiz verileri çıkar
filtered = [(img, lbl) for img, lbl in zip(image_paths, all_labels) if lbl >= 0]
image_paths, all_labels = zip(*filtered)

# 💡 Basit görsel özellik (dosya boyutu gibi) çıkar – burada basit bir şey kullanıyoruz
def get_features(img_paths):
    return np.array([[os.path.getsize(p)] for p in img_paths])

features = get_features(image_paths)

# 🔍 Optuna ile en iyi train oranını bul
def objective(trial):
    train_ratio = trial.suggest_float('train_ratio', 0.6, 0.9)
    X_train, X_test, y_train, y_test = train_test_split(
        features, all_labels, train_size=train_ratio, stratify=all_labels, random_state=42
    )
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    return acc

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)
best_ratio = study.best_params['train_ratio']
print(f"✅ En iyi train oranı: {best_ratio:.2f}")

# 🔁 Train/val/test ayır
X_temp, X_test, y_temp, y_test, img_temp, img_test = train_test_split(
    features, all_labels, image_paths, test_size=0.15, stratify=all_labels, random_state=42
)
X_train, X_val, y_train, y_val, img_train, img_val = train_test_split(
    X_temp, y_temp, img_temp, test_size=(1 - best_ratio - 0.15) / (best_ratio), stratify=y_temp, random_state=42
)

# 📁 Klasörlere kopyalama fonksiyonu
def copy_set(img_list, split_name):
    for img_path in tqdm(img_list, desc=f"Kopyalanıyor → {split_name}"):
        file = os.path.basename(img_path)
        label_file = file.replace('.jpg', '.txt').replace('.png', '.txt')
        label_path = os.path.join(labels_dir, label_file)

        dest_img = os.path.join(base_path, split_name, "images", file)
        dest_lbl = os.path.join(base_path, split_name, "labels", label_file)

        os.makedirs(os.path.dirname(dest_img), exist_ok=True)
        os.makedirs(os.path.dirname(dest_lbl), exist_ok=True)

        shutil.copy(img_path, dest_img)
        if os.path.exists(label_path):
            shutil.copy(label_path, dest_lbl)

# 🚚 Verileri yeni klasör yapısına taşı
copy_set(img_train, "train")
copy_set(img_val, "val")
copy_set(img_test, "test")

print("🎉 Veri başarıyla ayrıldı ve kopyalandı.")

# 🚀 AI Destekli Hava ve Kara Hedef Tespit ve Sınıflandırma Sistemi

Bu proje, kamera görüntülerinden **hava ve kara hedeflerini gerçek zamanlı olarak tespit etmek** ve **hava araçlarının tipini sınıflandırmak** amacıyla geliştirilmiştir. Proje, Ultralytics YOLOv8 nesne tespiti modeli ile birlikte özel eğitimli bir resne50  uçak sınıflandırma modülünü kullanır.

---
## Kullanım 

 - model_loader sınıfından kara ve hava mdeol dosya yollarını giriniz
 - aircraft_classifier da yer alan h5 model dosyasını ve etıket ısımlerı bulunan json dosya yolunu ayarlayınız
 - main sınıfından çalıştırıp istediğiniz modeli seçerek kullanmaya başlayabilirsiniz 
---


## 🔍 Özellikler

- Gerçek zamanlı kamera ile hedef tespiti
- Tespit edilen uçaklar için tür sınıflandırması 
- Hava ve kara modellerini ayrı ayrı destekler
- Görüntü , Video ve canlı kamera seçim olanaıgı sağlar
- YOLOv8 tabanlı hızlı ve hassas nesne tespiti
- Modüler Python yapısı (model ayırma, sınıflandırıcılar ayrı dosyalarda)

---


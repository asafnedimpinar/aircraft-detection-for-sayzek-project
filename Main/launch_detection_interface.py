from image_detector import detect_from_image
from video_detector import detect_from_video

def main():
    while True:
        secim = input("\n Tespitin yapılacagı formatın seçim yapın: resim yüklemek için r | video yüklemek  için v | çıkış yapmak için için e: ").strip().lower()

        if secim == 'r':
            path = input("🖼️  Lütfen resim dosyasının yolunu girin: ").strip()
            detect_from_image(path)

        elif secim == 'v':
            path = input("🎥  Lütfen video dosyasının yolunu girin: ").strip()
            detect_from_video(path)

        elif secim == 'e':
            print("🚪 Çıkılıyor...")
            break

        else:
            print("⚠️  Geçersiz seçim. Lütfen 'r', 'v' ya da 'e' girin.")

if __name__ == "__main__":
    main()

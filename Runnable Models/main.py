import tkinter as tk
from tkinter import messagebox, filedialog
from image_detector import detect_from_image
from video_detector import detect_from_video
from detection_by_camera import detect_from_camera
from model_loader import load_model_by_type

model_tip = None  # Kullanıcının seçtiği model tipi: 'kara' veya 'hava'

def baslangic_ekrani():
    def sec_kategori(tip):
        nonlocal kategori_pencere
        global model_tip
        model_tip = tip

        try:
            load_model_by_type(tip)
        except Exception as e:
            messagebox.showerror("Model Yükleme Hatası", str(e))
            return

        kategori_pencere.destroy()
        ana_menu()

    kategori_pencere = tk.Tk()
    kategori_pencere.title("Tespit Alanı Seç")
    kategori_pencere.geometry("400x250")
    kategori_pencere.configure(bg="#1e1e1e")

    label = tk.Label(kategori_pencere, text="Tespit Alanı Seçin", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e")
    label.pack(pady=30)

    btn_kara = tk.Button(kategori_pencere, text="🚗 Karadaki Nesneler", command=lambda: sec_kategori("kara"),
                         width=25, height=2, bg="#0078D7", fg="white")
    btn_kara.pack(pady=10)

    btn_hava = tk.Button(kategori_pencere, text="✈️Havadaki Nesneler", command=lambda: sec_kategori("hava"),
                         width=25, height=2, bg="#107c10", fg="white")
    btn_hava.pack(pady=10)

    kategori_pencere.mainloop()

def ana_menu():
    global root
    root = tk.Tk()
    root.title("Hava Aracı Tespit Sistemi")
    root.geometry("400x400")
    root.configure(bg="#1e1e1e")

    secilen_model = "Karadaki Nesneler" if model_tip == "kara" else "Havadaki Nesneler"

    label = tk.Label(root, text=f"🧠 Seçilen Model: {secilen_model}", font=("Helvetica", 14, "bold"), fg="white", bg="#1e1e1e")
    label.pack(pady=20)

    btn_resim = tk.Button(root, text="🖼️ Görüntü ile Tespit", command=sec_resim, width=25, height=2, bg="#2d89ef", fg="white")
    btn_resim.pack(pady=10)

    btn_video = tk.Button(root, text="🎥 Video ile Tespit", command=sec_video, width=25, height=2, bg="#2d89ef", fg="white")
    btn_video.pack(pady=10)

    btn_camera = tk.Button(root, text="🎦 Canlı Kamera ile Tespit", command=sec_kamera, width=25, height=2, bg="#107c10", fg="white")
    btn_camera.pack(pady=10)

    btn_model_degistir = tk.Button(root, text="🔄 Modeli Değiştir", command=geri_git_kategoriye, width=25, height=2, bg="#ffb900", fg="black")
    btn_model_degistir.pack(pady=10)

    btn_exit = tk.Button(root, text="🚪 Çıkış", command=cikis, width=25, height=2, bg="#e81123", fg="white")
    btn_exit.pack(pady=20)

    root.mainloop()

# Yardımcı Fonksiyonlar         

def sec_resim():
    path = filedialog.askopenfilename(title="🖼️ Resim Dosyası Seç", filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png")])
    if path:
        try:
            detect_from_image(path)
        except Exception as e:
            messagebox.showerror("Hata", f"Resim tespiti başarısız:\n{str(e)}")

def sec_video():
    path = filedialog.askopenfilename(title="🎥 Video Dosyası Seç", filetypes=[("Video Dosyaları", "*.mp4 *.avi *.mov")])
    if path:
        try:
            detect_from_video(path)
        except Exception as e:
            messagebox.showerror("Hata", f"Video tespiti başarısız:\n{str(e)}")

def sec_kamera():
    try:
        detect_from_camera()
    except Exception as e:
        messagebox.showerror("Hata", f"Kamera tespiti başarısız:\n{str(e)}")

def cikis():
    root.destroy()

def geri_git_kategoriye():
    root.destroy()
    baslangic_ekrani()

# Program Giriş Noktası         

if __name__ == "__main__":
    baslangic_ekrani()

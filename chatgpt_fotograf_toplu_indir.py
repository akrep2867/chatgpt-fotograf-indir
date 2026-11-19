import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import PurePosixPath

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff",
    ".heic", ".heif", ".avif", ".ico", ".jfif", ".svg"
}

class ImageExportTool:
    def __init__(self, root):
        self.root = root
        root.title("ChatGPT Fotoğraf Toplu İndirme")
        root.geometry("620x390")
        root.minsize(560, 350)

        tk.Label(root, text="ChatGPT Fotoğraflarını Toplu Çıkar", font=("Segoe UI", 16, "bold")).pack(pady=(18, 6))
        tk.Label(root, text="ChatGPT veri dışa aktarma ZIP dosyanızdaki görselleri tek klasöre çıkarır.\nChatGPT şifrenizi istemez ve internete bağlanmaz.",
                 font=("Segoe UI", 10), justify="center").pack(pady=(0, 16))

        self.zip_path = tk.StringVar()
        self.dest_path = tk.StringVar()

        self._path_row("Veri dışa aktarma ZIP dosyası:", self.zip_path, self.choose_zip)
        self._path_row("Fotoğrafların kaydedileceği klasör:", self.dest_path, self.choose_dest)

        self.progress = ttk.Progressbar(root, mode="determinate", length=540)
        self.progress.pack(pady=(18, 8))
        self.status = tk.StringVar(value="Başlamak için ZIP dosyanızı ve hedef klasörü seçin.")
        tk.Label(root, textvariable=self.status, wraplength=560, justify="center").pack(pady=4)

        self.start_btn = tk.Button(root, text="FOTOĞRAFLARI ÇIKAR", command=self.extract,
                                   bg="#1769aa", fg="white", activebackground="#0d4f85",
                                   font=("Segoe UI", 11, "bold"), padx=18, pady=9)
        self.start_btn.pack(pady=14)

        tk.Label(root, text="Not: Yalnızca dışa aktarma ZIP dosyasında bulunan görseller çıkarılır.\nKütüphanedeki her görselin dışa aktarma dosyasına dahil olması garanti değildir.",
                 font=("Segoe UI", 8), fg="#555", justify="center").pack(side="bottom", pady=12)

    def _path_row(self, label, variable, command):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=28, pady=6)
        tk.Label(frame, text=label, anchor="w").pack(fill="x")
        line = tk.Frame(frame)
        line.pack(fill="x", pady=3)
        tk.Entry(line, textvariable=variable).pack(side="left", fill="x", expand=True)
        tk.Button(line, text="Gözat...", command=command, width=10).pack(side="left", padx=(8, 0))

    def choose_zip(self):
        path = filedialog.askopenfilename(title="ChatGPT veri ZIP dosyasını seçin",
                                          filetypes=[("ZIP dosyaları", "*.zip"), ("Tüm dosyalar", "*.*")])
        if path:
            self.zip_path.set(path)
            if not self.dest_path.get():
                self.dest_path.set(os.path.join(os.path.dirname(path), "ChatGPT_Fotograflar"))

    def choose_dest(self):
        path = filedialog.askdirectory(title="Fotoğrafların kaydedileceği klasörü seçin")
        if path:
            self.dest_path.set(path)

    def extract(self):
        archive = self.zip_path.get().strip()
        destination = self.dest_path.get().strip()
        if not archive or not os.path.isfile(archive):
            messagebox.showwarning("ZIP seçilmedi", "Lütfen ChatGPT veri dışa aktarma ZIP dosyasını seçin.")
            return
        if not destination:
            messagebox.showwarning("Klasör seçilmedi", "Lütfen fotoğrafların kaydedileceği klasörü seçin.")
            return

        os.makedirs(destination, exist_ok=True)
        self.start_btn.config(state="disabled")
        count = 0
        skipped = 0
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                candidates = [i for i in zf.infolist()
                              if not i.is_dir()
                              and PurePosixPath(i.filename).suffix.lower() in IMAGE_EXTENSIONS
                              and "__MACOSX" not in i.filename]
                self.progress["maximum"] = max(len(candidates), 1)
                for index, info in enumerate(candidates, 1):
                    # Flatten into one folder; preserve duplicate names safely.
                    name = PurePosixPath(info.filename).name
                    if not name:
                        skipped += 1
                        continue
                    target = os.path.join(destination, name)
                    stem, ext = os.path.splitext(name)
                    n = 1
                    while os.path.exists(target):
                        target = os.path.join(destination, f"{stem}_{n}{ext}")
                        n += 1
                    with zf.open(info, "r") as source, open(target, "wb") as output:
                        while True:
                            chunk = source.read(1024 * 1024)
                            if not chunk:
                                break
                            output.write(chunk)
                    count += 1
                    self.progress["value"] = index
                    self.status.set(f"Taranıyor... {index}/{len(candidates)}")
                    self.root.update_idletasks()

            self.status.set(f"Tamamlandı: {count} görsel çıkarıldı.")
            messagebox.showinfo("İşlem tamamlandı",
                                f"{count} görsel şu klasöre çıkarıldı:\n{destination}\n\n"
                                "ZIP içinde uygun uzantılı görsel bulunamadıysa sayı 0 olabilir.")
        except zipfile.BadZipFile:
            messagebox.showerror("Geçersiz ZIP", "Seçtiğiniz dosya geçerli bir ZIP arşivi değil.")
        except Exception as exc:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu:\n{exc}")
        finally:
            self.start_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageExportTool(root)
    root.mainloop()

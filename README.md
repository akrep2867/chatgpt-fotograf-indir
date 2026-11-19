# ChatGPT Fotoğraf Toplu İndirme (Windows)

Bu araç, ChatGPT hesabınızdan **kendinizin indirdiği veri dışa aktarma ZIP dosyasının** içindeki görsel dosyalarını tek klasöre çıkarır.

## Kullanım

1. ChatGPT'de **Ayarlar → Veri Denetimleri → Verileri dışa aktar** bölümünden dışa aktarma isteyin.
2. E-posta ile gelen indirme bağlantısından ZIP dosyasını bilgisayarınıza indirin.
3. Bu depodaki **Actions** sekmesini açın.
4. **Windows EXE oluştur** iş akışını seçip **Run workflow** düğmesine basın. (İlk dosya yüklemelerinden sonra otomatik bir derleme de başlamış olabilir.)
5. İşlem tamamlandığında çalıştırma kaydına girin; **Artifacts** bölümünden `ChatGPT-Fotograf-Toplu-Indir-Windows` dosyasını indirin.
6. İndirdiğiniz ZIP içindeki EXE'yi çıkarıp `ChatGPT_Fotograf_Toplu_Indir.exe` dosyasını çalıştırın.
7. ChatGPT veri ZIP dosyanızı ve fotoğrafların kaydedileceği klasörü seçin.

## Önemli sınırlar ve gizlilik

- Program ChatGPT hesabınıza giriş yapmaz, şifrenizi istemez ve dosyaları herhangi bir sunucuya göndermez.
- Yalnızca seçtiğiniz dışa aktarma ZIP dosyasının içinde bulunan görselleri çıkarır. ChatGPT Kütüphanesindeki her görselin dışa aktarma paketine dahil olması garanti değildir.
- ZIP arşivindeki görselleri tek klasöre çıkarır; aynı adlı dosyaların üzerine yazmaz, dosya adlarına sıra numarası ekler.
- Windows EXE'si GitHub Actions tarafından oluşturulur; bilgisayarınızda Python kurulu olması gerekmez.

## Kaynak kod

`chatgpt_fotograf_toplu_indir.py` Python kaynak kodudur. EXE, GitHub Actions üzerinde PyInstaller ile oluşturulur.

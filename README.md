# IronTrack AI 3.0 | iPhone PWA

Bu sürüm **Streamlit değil**. iPhone Safari'de çalışan, ana ekrana eklenebilen çevrimdışı-öncelikli web uygulamasıdır. Windows EXE, Python sunucusu, ücretli API, bulut veritabanı veya hesap gerektirmez. Yalnızca ilk kez yüklemek ve güncellemek için internete ihtiyaç vardır.

## Özellikler

- Pazartesi ve Salı antrenmanları; ilk kurulumda 8'er hareket
- Hareket ekleme, ad değiştirme, gün listesinden kaldırma
- Her hareket için 1–3 set; ayrı kg, tekrar, RIR ve tek tekrar hedefi
- Değerler taslak olarak yerel cihazda tutulur; kaydedilen antrenmanlar sonraki antrenmana otomatik gelir
- Gelişim: önceki seansa göre kg/tekrar, set hedefi, son 8 antrenmanın basit grafiği
- JSON yedek indir, JSON'dan geri yükle; onaylı geçmiş sıfırlama
- Veri IndexedDB'de **yalnızca kullanılan iPhone ve tarayıcı profilinde** tutulur

## iPhone'a kurulum (HTTPS gerekli)

1. Bu klasörün içindeki **index.html, app.js, style.css, sw.js, manifest.webmanifest ve icons/** dosyalarını bir GitHub deposunun kök dizinine yükle. **irontrack.db, özel antrenman kayıtların veya JSON yedeğin depoya yüklenmemeli.** Depo herkese açıksa kod herkes tarafından görülebilir.
2. GitHub deposunda Settings > Pages > Build and deployment > Deploy from a branch > main / (root) seç. Yayınlanan `https://KULLANICI.github.io/DEPO/` adresini bekle. GitHub Pages erişimi ve menüler değişebilir; yayınlanan URL'yi depo Pages ekranından doğrula.
3. Bu adresi **iPhone Safari** ile aç. Safari'nin Paylaş menüsünden **Ana Ekrana Ekle** seçeneğini kullan. Sonrasında IronTrack simgesinden başlat.
4. İlk başarılı yükleme ve önbelleğe alma tamamlandıktan sonra uygulama çevrimdışı çalışabilir. Önce uçak modunda test et. Safari/telefon depolaması temizlenirse yerel veriler kaybolabilir.

**Önemli:** `index.html` dosyasını iPhone'da Dosyalar'dan doğrudan açmak veya bilgisayarda çift tıklamak PWA kurulumu sağlamaz. HTTPS sunucusu gereklidir. GitHub Pages yalnızca statik uygulama dosyalarını sunar; kullanıcı antrenmanları otomatik GitHub'a yüklenmez.

## Eski Windows SQLite kayıtlarını taşıma (isteğe bağlı)

Eski verileri aktarmak istemiyorsan yeni uygulama boş geçmişle başlar. Aktarmak istersen bilgisayarda:

```cmd
py sqlite_to_json.py "C:\\...\\irontrack.db"
```

Oluşan `irontrack-eski-kayitlar.json` dosyasını AirDrop veya Dosyalar ile iPhone'a gönder. IronTrack > **Veriler > Yedekten geri yükle** bölümünden seç. İçe aktarma mevcut mobil verilerin yerini alır. SQLite dosyan okunur ama **değiştirilmez**.

## Günlük kullanım / veri güvenliği

- Kg, tekrar, RIR ve hedef değişiklikleri otomatik yerel taslağa yazılır. Antrenman geçmişine yeni kayıt oluşturmak için **Antrenmanı Kaydet** tuşuna bas.
- Aynı antrenmanı iki kez kaydetmek iki ayrı kayıt oluşturur. Hatalı kayıt silme/düzenleme bu sürümde yoktur.
- **Veriler > Yedeği indir** ile düzenli yedek al, dosyayı iCloud Drive gibi güvenli bir yerde sakla. JSON yedeği hassas kişisel antrenman verilerini içerir.
- Uygulama hesap/senkronizasyon sağlamaz. Başka iPhone'da devam etmek için JSON yedeğini aktar.
- iOS uygulama önbelleğini ve IndexedDB'yi korumayı garanti etmez; özellikle az depolama, site verilerini temizleme veya uygulamayı kaldırma durumlarında veri kaybı olabilir.
- Apple App Store'a gönderilen yerel IPA değildir. Ana ekrandan bağımsız açılan PWA'dır.

## Yerel bilgisayar testi

```cmd
py -m http.server 8000
```

Bilgisayarda `http://localhost:8000` aç. Gerçek iPhone kurulumu için HTTPS adresi gerekir.

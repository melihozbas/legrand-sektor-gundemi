# Legrand Sektör Gündemi — ücretsiz pilot

Bu proje, V5'in tek sütunlu haber tasarımını koruyan **gerçek RSS toplama + GitHub Pages yayını** prototipidir.

## Kurulum (GitHub hesabı gerekli)

1. GitHub'da yeni **public** repository oluşturun (ör. `legrand-sektor-gundemi`). Şirket içi gizli dosya koymayın.
2. Bu ZIP içindeki **tüm dosyaları**, `.github/workflows/scan.yml` dahil, repository köküne yükleyin. GitHub web arayüzünde gizli `.github` klasörünün doğru yüklendiğini kontrol edin.
3. **Settings → Pages → Build and deployment → Deploy from a branch** bölümünde `main` ve `/ (root)` seçip kaydedin.
4. **Actions → Kaynaklari tara → Run workflow** ile ilk taramayı başlatın. Gerekirse Actions izinleri ve repository için `Read and write permissions` ayarı etkinleştirilmelidir.
5. Tarama tamamlanıp `data/news.json` commit edildikten ve Pages yayımlandıktan sonra site `https://KULLANICI.github.io/REPO/` adresinde açılır.

## Otomasyon

- GitHub Actions her gün **05:00 UTC = 08:00 Türkiye** için planlanır. GitHub yoğunluğunda gecikme olabilir; cron çalıştırması garanti edilen bir saat değildir.
- **Actions → Kaynaklari tara → Run workflow** manuel tarama başlatır.
- Sitedeki **Son verileri yükle** düğmesi araştırma yapmaz; yayımlanmış `data/news.json` dosyasını yeniden okur. Bu ayrım bilinçli ve açıktır.
- Tarama Google News RSS sorgularını kullanır; bunlar resmî mevzuat kaynaklarının tam metinlerini taramaz. RSS kullanılabilirliği ve kaynak kapsamı garanti değildir.
- Ücretsiz GitHub Pages yayını public repo gerektirir; GitHub hizmet limitleri ve kullanım şartları geçerlidir.

## Doğruluk sınırları

- Her otomatik kayıt **doğrulanmamış haber** statüsündedir.
- Ürün önerileri basit anahtar kelime eşleştirmesidir; gerçek Legrand teknik katalog doğrulaması, madde karşılaştırması veya üretken yapay zekâ analizi **yoktur**.
- Haberlerde 'zorunlu' iddiası otomatik olarak üretilmez.
- Resmî Legrand logosu dahil edilmedi; yalnızca şirketçe onaylanmış logo kullanıcı tarafından eklenebilir.
- Bu proje resmî Legrand yayını değildir.

## Geliştirme yol haritası

1. Resmî kaynaklardan mevzuat metni alma ve sürüm karşılaştırma.
2. Legrand Türkiye resmî ürün kataloglarıyla doğrulanmış ürün eşleştirme.
3. Uzman onay kuyruğu ve editoryal inceleme.
4. Gerçek yapay zekâ destekli gerekçeli analiz (ayrı model/servis ve kullanım maliyeti değerlendirilerek).
5. Günlük e-posta raporları.

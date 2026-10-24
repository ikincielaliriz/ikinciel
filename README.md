# İkinci El Alırız

**İkinci el elektronik cihazlarınızı (bilgisayar, telefon, tablet, konsol ve daha fazlası) hızlı, güvenilir ve şeffaf fiyatlarla alıyoruz.**

[🌐 ikincielaliriz.com](https://ikincielaliriz.com/) · [📞 İletişim](https://ikincielaliriz.com/iletisim) · [📷 Instagram](...) 

---

## Ne Yapıyoruz?

Kullanılmayan veya yükseltmek istediğiniz elektronik cihazlarınızı **değerinde** satın alıyoruz. Cihazınızın modelini ve durumunu bize iletin, dakikalar içinde net bir teklif alın.

## Hizmetlerimiz

- 💻 **Dizüstü & Masaüstü Bilgisayar** alımı
- 📱 **Akıllı Telefon & Tablet** alımı
- 🎮 **Oyun Konsolu** alımı (PlayStation, Xbox, Nintendo)
- 🖥️ **Monitör & Çevre Birimi** alımı
- ⌚ **Akıllı Saat & Aksesuar** alımı

## Neden İkinci El Alırız?

- **Hızlı Teklif:** Cihaz bilgilerini girin, kısa sürede fiyat teklifi alın.
- **Güvenilir Süreç:** Şeffaf değerlendirme, sürpriz kesinti yok.
- **Kolay Teslimat:** Size uygun yöntemle cihazınızı teslim edin.
- **Yerli & Uzman:** Türkiye pazarına odaklanmış, sektör deneyimi olan bir ekip.

## Bağlantılar

- 🌐 Web sitesi: [ikincielaliriz.com](https://ikincielaliriz.com/)
- 📧 E-posta: [info@ikincielaliriz.com](mailto:info@ikincielaliriz.com)
- 📷 X: [@ikincielaliriz](https://x.com/ikincielaliriz)

---

<sub>Bu profil, ikinci el elektronik alım-satım hizmetleri sunan **ikincielaliriz.com** markasına aittir.</sub>

# İkinci El Alırız Bilgi Bankası

İkinci el teknoloji ürünlerinin değerlendirilmesi, cihaz satışı ve kurumsal teknoloji envanterlerinin alımı hakkında Türkçe soru-cevap kayıtları.

- Website: https://ikincielaliriz.com/
- Repository: https://github.com/ikincielaliriz/ikinciel
- Language: Turkish (`tr`)
- Current release: `0.1.0` — 25 initial FAQ records
- Target: 500 reviewed FAQ records across 20 categories

## Goals

1. İnsanlara ikinci el teknoloji ürünlerini değerlendirirken pratik ve doğru bilgi sağlamak.
2. FAQ verisini arama, filtreleme, analiz ve RAG tabanlı bilgi erişimi için makinece okunabilir kılmak.
3. Bireysel cihaz satışı ile kurumsal ve toplu cihaz alımı süreçleri hakkında güvenilir bir başlangıç kaynağı sunmak.

## Repository structure

```text
.
├── README.md
├── CONTRIBUTING.md
├── index.json
├── schema.json
├── validate.py
└── data/
    └── 01-ikinci-el-teknolojiye-giris.json
```

`index.json` planlanan 20 kategoriyi ve mevcut kayıt sayılarını listeler. İlk sürümde yalnızca ilk kategori dosyası oluşturulmuştur; kalan kategori dosyaları tamamlandıkça index içindeki `current_count` ve durum bilgileri güncellenmelidir.

## FAQ record format

Her kategori dosyası bir JSON array içerir. Kayıt alanları:

- `id`: depo genelinde benzersiz kimlik.
- `language`: içerik dili (`tr`).
- `category`: kategori kimliği.
- `question`: kullanıcının doğal dilde sorusu.
- `answer`: doğrudan, açıklayıcı ve uygulanabilir cevap.
- `keywords`: ilgili terimler ve arama ifadeleri.
- `intent`: kullanıcının temel amacı.
- `audience`: `bireysel`, `kurumsal` veya ikisi.
- `related_questions`: ilişkili bilgi kayıtlarına yönlendirme için soru başlıkları.
- `source_url`: ilgili sayfa veya doğrulanabilir kaynak; kaynak yoksa `null`.
- `last_updated`: ISO 8601 tarih biçiminde güncelleme tarihi.
- `review_status`: içerik denetiminin durumu.

## Validate JSON

Python 3 ile sözdizimi, temel alanlar, yinelenen ID'ler ve yinelenen sorular kontrol edilebilir:

```bash
python3 validate.py
```

JSON Schema doğrulaması ayrıca `schema.json` dosyasıyla, JSON Schema Draft 2020-12 destekleyen bir doğrulayıcı kullanılarak yapılabilir.

## Publishing and search guidance

Bu depo, web sitesinde yayınlanan sayfaların yerine geçmez. Arama motoru erişimi için kullanıcıya açık, yararlı ve özgün HTML sayfalar yayımlayın; içeriklerin ilgili hizmet sayfalarına bağlanmasını sağlayın. JSON'u bir endpoint olarak sunacaksanız uygun HTTP başlıklarını, erişilebilirliği ve güncelleme politikasını yapılandırın.

Yapılandırılmış veriler yalnızca sayfada gerçekten görünen ve kullanıcıya sunulan içeriği doğru biçimde temsil etmelidir. Sayfaya uygun olduğunda `Article` veya `Organization` gibi şemalar değerlendirilebilir. `QAPage` işaretlemesi, sıradan bir işletme SSS sayfasına otomatik olarak uygulanmamalıdır. JSON dosyasının varlığı tek başına indekslenme, sıralama veya yapay zekâ sistemlerinde görünürlük garantisi sağlamaz.

## Accuracy and trust

- Fiyat, alım kapsamı, hizmet bölgesi, lojistik, ödeme süresi ve belge gereklilikleri gibi değişebilen bilgileri işletme tarafından doğrulamadan kesin gerçek olarak yayımlamayın.
- Teknik veya hukuki kapsamı olan cevapları uygun uzmanlarla gözden geçirin.
- Kişisel veri, seri numarası, IMEI, parola veya özel müşteri bilgilerini herkese açık kayıtlar içinde tutmayın.
- Cihazların mülkiyeti, veri silme, hesap kilitleri ve kurumsal yönetim profilleri konularında güvenli ve yetkili süreçleri esas alın.
- `draft_review_required` durumundaki kayıtları işletme incelemesi tamamlanmadan nihai ve onaylanmış politika gibi sunmayın.

## License

Bu depoda bir lisans dosyası bulunana kadar yeniden kullanım koşullarının açıkça tanımlandığını varsaymayın. Açık lisans seçmeden önce içeriklerin hak sahipliği ve işletme kullanım ihtiyaçlarını değerlendirin.


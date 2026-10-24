# Katkı ve içerik kalite kuralları

Yeni soru-cevap eklerken aşağıdaki kuralları izleyin.

## İçerik kuralları

1. Her kayıt tek bir gerçek kullanıcı sorusuna cevap vermeli.
2. Soru başlıklarını yalnızca anahtar kelime değiştirerek çoğaltmayın.
3. Cevap doğrudan soruyu yanıtlamalı; gerektiğinde adımlar, örnekler ve önemli istisnalar içermeli.
4. Fiyat, ödeme, alım kapsamı, teslimat, hizmet bölgesi veya hukuki yükümlülükler hakkında doğrulanmamış taahhüt vermeyin.
5. Marka veya hizmetle ilgili iddialar ilgili işletme sayfası ya da yetkili kişi tarafından doğrulanmalı.
6. Başka kaynaklardan kopyalanmış metin yerine özgün anlatım kullanın ve gerektiğinde kaynağı belirtin.
7. Kişisel veri, müşteri verisi, parola, seri numarası veya IMEI gibi bilgileri örnek kayıtların içine koymayın.
8. İçerik dili Türkçe ve anlatım açık, doğal, tarafsız olmalı.

## Teknik kurallar

1. Her kayıt benzersiz bir `id` almalı; yayımlanmış kimlikler sonradan değiştirilmemeli.
2. Kayıt alanları `schema.json` ile uyumlu olmalı.
3. `last_updated` alanı `YYYY-MM-DD` biçiminde olmalı.
4. `source_url` yalnızca gerçek ve ilgili bir URL olmalı; kaynak yoksa `null` kullanılmalı.
5. `review_status`, inceleme durumunu doğru göstermeli. Yeni kayıtlar `draft_review_required` ile başlamalı.
6. İlgili kategori dosyası ve `index.json` sayaçları birlikte güncellenmeli.
7. Değişiklik öncesinde `python3 validate.py` çalıştırılmalı.

## İnceleme akışı

- `draft_review_required`: taslak, doğrulama bekliyor.
- `reviewed`: içerik ve teknik biçim gözden geçirildi.
- `approved`: işletme tarafından yayımlanmaya uygun bulundu.
- `archived`: artık kullanılmıyor; silmek yerine gerektiğinde arşivlenebilir.

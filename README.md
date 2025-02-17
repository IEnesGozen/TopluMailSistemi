Mail Gönderme Sistemi:
Bu Python projesi, kullanıcıların veritabanına kişileri ekleyebileceği ve ardından tüm kişilere toplu e-posta gönderebileceği bir uygulama sağlar. Proje, Tkinter kullanarak GUI (grafiksel kullanıcı arayüzü) oluşturur ve SQLite veritabanı ile kişileri yönetir. Gmail üzerinden e-posta göndermek için SMTP protokolü kullanılır.

Özellikler:
Kişi Ekleme: Kullanıcılar, isim ve e-posta adresi girerek veritabanına yeni kişiler ekleyebilir.
Kişi Listesi: Kullanıcılar, veritabanındaki kişileri listeleyebilir, silme işlemi yapabilirler.
Mail Gönderme: Kullanıcılar, Gmail hesapları aracılığıyla tüm kişilere toplu e-posta gönderebilir.
İlerleme Çubuğu: Mail gönderme işlemi sırasında bir ilerleme çubuğu görüntülenir.

Kullanılan Teknolojiler:
Python 3: Proje Python 3 ile geliştirilmiştir.
Tkinter: Grafiksel kullanıcı arayüzü için kullanılmıştır.
SQLite: Kişi verilerini saklamak için kullanılmıştır.
SMTP: Gmail üzerinden e-posta göndermek için kullanılmıştır.

Gereksinimler:
Python 3.x yüklü olmalıdır.
Gmail hesabı ile SMTP üzerinden e-posta gönderebilmek için Gmail Güvenlik Ayarları'nda "Daha az güvenli uygulamalara izin ver" seçeneğini açmanız gerekebilir.

Python'da gerekli kütüphanelerin yüklü olduğundan emin olun:
pip install tkinter sqlite3 smtplib

Projenin Çalıştırılması:
Bu projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz:
mail_system.py dosyasını çalıştırın.
GUI arayüzü açılacak ve veritabanına kişi eklemeye başlayabilirsiniz.

Kişi Ekleme:
İsim ve e-posta adresini girerek kişi ekleyebilirsiniz.

Kişi Silme:
Kişi listesinde bir kişi seçerek "Seçili Kişiyi Sil" butonunu kullanarak kişiyi silebilirsiniz.

Mail Gönderme:
E-posta göndermek için Gmail hesabınızı ve uygulama şifrenizi girin, ardından e-posta konusu ve içeriğini belirleyin.
"Tüm Kişilere Gönder" butonunu kullanarak mailleri gönderebilirsiniz.

Bilinen Hatalar
Gmail güvenlik ayarları nedeniyle, bazı kullanıcıların "Daha Az Güvenli Uygulama" erişimi açık olmadan mail göndermesi engellenebilir.
Gmail'den toplu mail gönderirken, belirli sayıda e-posta gönderiminden sonra engellemeler yaşanabilir (özellikle büyük miktarda mail gönderiliyorsa).

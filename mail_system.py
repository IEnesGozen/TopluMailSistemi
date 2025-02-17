import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random
import os

class MailSystem:
    def __init__(self):
        # Ana pencereyi oluştur
        self.root = tk.Tk()
        self.root.title("Mail Gönderme Sistemi")
        self.root.geometry("800x600")
        
        # Veritabanı bağlantısı
        self.create_database()
        
        # Arayüz bileşenlerini oluştur
        self.create_gui()
        
        # Pencereyi görüntüle
        self.root.mainloop()
    
    def create_database(self):
        """Veritabanını oluştur ve bağlantıyı kur"""
        try:
            # Veritabanı dosyası yoksa oluştur
            self.conn = sqlite3.connect('mail_database.db')
            self.cursor = self.conn.cursor()
            
            # Contacts tablosunu oluştur
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Veritabanı Hatası", f"Veritabanı oluşturulurken hata: {str(e)}")
    
    def create_gui(self):
        """Kullanıcı arayüzünü oluştur"""
        # Ana frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Grid yapılandırması
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Bölümleri oluştur
        self.create_contact_section()
        self.create_contact_list()
        self.create_mail_section()
    
    def create_contact_section(self):
        """Kişi ekleme bölümünü oluştur"""
        contact_frame = ttk.LabelFrame(self.main_frame, text="Kişi Ekle", padding="5")
        contact_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # İsim alanı
        ttk.Label(contact_frame, text="İsim:").grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(contact_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        # Email alanı
        ttk.Label(contact_frame, text="Email:").grid(row=0, column=2, padx=5)
        self.email_entry = ttk.Entry(contact_frame, width=30)
        self.email_entry.grid(row=0, column=3, padx=5)
        
        # Ekle butonu
        ttk.Button(contact_frame, text="Kişi Ekle", command=self.add_contact).grid(row=0, column=4, padx=5)
    
    def create_contact_list(self):
        """Kişi listesi bölümünü oluştur"""
        list_frame = ttk.LabelFrame(self.main_frame, text="Kişi Listesi", padding="5")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Treeview oluştur
        columns = ("ID", "İsim", "Email")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Sütunları yapılandır
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar ekle
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Yerleştir
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Sil butonu
        ttk.Button(list_frame, text="Seçili Kişiyi Sil", command=self.delete_contact).grid(row=1, column=0, pady=5)
        
        # Liste frame'ini genişletilebilir yap
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Kişi listesini güncelle
        self.update_contact_list()
    
    def create_mail_section(self):
        """Mail gönderme bölümünü oluştur"""
        mail_frame = ttk.LabelFrame(self.main_frame, text="Mail Gönder", padding="5")
        mail_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Gmail bilgileri
        creds_frame = ttk.Frame(mail_frame)
        creds_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Label(creds_frame, text="Gmail:").grid(row=0, column=0, padx=5)
        self.gmail_entry = ttk.Entry(creds_frame, width=30)
        self.gmail_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(creds_frame, text="Uygulama Şifresi:").grid(row=0, column=2, padx=5)
        self.password_entry = ttk.Entry(creds_frame, width=30, show="*")
        self.password_entry.grid(row=0, column=3, padx=5)
        
        # Mail içeriği
        ttk.Label(mail_frame, text="Konu:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.subject_entry = ttk.Entry(mail_frame, width=80)
        self.subject_entry.grid(row=1, column=1, sticky="ew", padx=5)
        
        ttk.Label(mail_frame, text="Mesaj:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.message_text = tk.Text(mail_frame, height=10, width=80)
        self.message_text.grid(row=2, column=1, sticky="ew", padx=5)
        
        # Gönder butonu
        ttk.Button(mail_frame, text="Tüm Kişilere Gönder", command=self.send_mail).grid(row=3, column=1, pady=10)
    
    def add_contact(self):
        """Yeni kişi ekle"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not name or not email:
            messagebox.showerror("Hata", "İsim ve email alanları boş bırakılamaz!")
            return
        
        try:
            self.cursor.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            self.update_contact_list()
            
            # Alanları temizle
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            
            messagebox.showinfo("Başarılı", "Kişi başarıyla eklendi!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu email adresi zaten kayıtlı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kişi eklenirken bir hata oluştu: {str(e)}")
    
    def delete_contact(self):
        """Seçili kişiyi sil"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen silinecek kişiyi seçin!")
            return
        
        try:
            contact_id = self.tree.item(selected_item)['values'][0]
            self.cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            self.conn.commit()
            self.update_contact_list()
            messagebox.showinfo("Başarılı", "Kişi başarıyla silindi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kişi silinirken bir hata oluştu: {str(e)}")
    
    def update_contact_list(self):
        """Kişi listesini güncelle"""
        # Mevcut listeyi temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Veritabanından kişileri al
            self.cursor.execute("SELECT * FROM contacts ORDER BY name")
            contacts = self.cursor.fetchall()
            
            # Listeye ekle
            for contact in contacts:
                self.tree.insert("", tk.END, values=contact)
        except Exception as e:
            messagebox.showerror("Hata", f"Kişi listesi güncellenirken hata: {str(e)}")
    
    def send_mail(self):
        """Tüm kişilere mail gönder"""
        # Mail bilgilerini al
        gmail = self.gmail_entry.get().strip()
        password = self.password_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()
        
        # Bilgileri kontrol et
        if not all([gmail, password, subject, message]):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return
        
        try:
            # SMTP sunucusuna bağlan
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail, password)
            
            # Kişileri al
            self.cursor.execute("SELECT name, email FROM contacts")
            recipients = self.cursor.fetchall()
            
            if not recipients:
                messagebox.showerror("Hata", "Kayıtlı kişi bulunamadı!")
                return
            
            # İlerleme penceresi
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Mail Gönderiliyor")
            progress_window.geometry("300x150")
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=len(recipients))
            progress_bar.pack(pady=20, padx=10, fill="x")
            
            progress_label = ttk.Label(progress_window, text="Mailler gönderiliyor...")
            progress_label.pack(pady=10)
            
            # Mailleri gönder
            for index, (name, email) in enumerate(recipients, 1):
                # Kişiselleştirilmiş mesaj
                personalized_message = f"Sayın {name},\n\n{message}"
                
                # Mail oluştur
                msg = MIMEMultipart()
                msg['From'] = gmail
                msg['To'] = email
                msg['Subject'] = subject
                
                # HTML içerik
                html_content = f"""
                <html>
                    <body>
                        <p>{personalized_message.replace(chr(10), '<br>')}</p>
                        <br>
                        <p>Saygılarımızla,</p>
                        <p>{gmail.split('@')[0]}</p>
                    </body>
                </html>
                """
                
                msg.attach(MIMEText(html_content, 'html'))
                
                # Gönder
                server.send_message(msg)
                
                # İlerleme çubuğunu güncelle
                progress_var.set(index)
                progress_label.config(text=f"Gönderilen: {index}/{len(recipients)}")
                progress_window.update()
                
                # Spam önlemek için bekle
                time.sleep(random.uniform(2, 5))
            
            server.quit()
            progress_window.destroy()
            
            # Başarı mesajı
            messagebox.showinfo("Başarılı", "Tüm mailler başarıyla gönderildi!")
            
            # Mail alanlarını temizle
            self.subject_entry.delete(0, tk.END)
            self.message_text.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Mail gönderirken bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    app = MailSystem()

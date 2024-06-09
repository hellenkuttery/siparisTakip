from tkinter import *
from tkinter import messagebox
import sqlite3

ekran=Tk()
ekran.geometry("500x300+800+200")
ekran.title("KİTAP TAKİP UYGULAMASI")


listeKutusu=""
listelePenceresi=""
# ---------------------------------------------------------------------------- #
#                          VERITABANININ OLUŞTURULMASI                         #
# ---------------------------------------------------------------------------- #
# Veritabanı dosyamızın oluşturulması (Bağlantı oluşturulması)

kitapVeritabani=sqlite3.connect("kitapKaydi.db")
curr=kitapVeritabani.cursor()
# ---------------------------------------------------------------------------- #
# Kitap Kaydı Tablosunun Oluşturulması
#IF NOT EXISTS  ekleyerek defalarca aynı tablos oluşuturulmasını istek yapmıyoruz.Bu da hata almamızı engelliyor
curr.execute(''' CREATE TABLE IF NOT EXISTS kitapKaydi (
  uyeID INT PRIMARY KEY,
  uyeAdi VARCHAR(50),
  kitapISBN VARCHAR(15),
  tarih VARCHAR(15)
  )   ''')

kitapVeritabani.commit()
kitapVeritabani.close()

# ---------------------------------------------------------------------------- #
# YENİ ELEMAN KAYIT İŞLEME
def Kaydet():
    uyeNo=uyeID.get()
    uye=uyeAdi.get()
    ISBNNumber=ISBN.get()
    tarih=AlınısTarihi.get()
    
    # Veritabanı bağlantısı
    kitapVeritabani=sqlite3.connect("kitapKaydi.db")
    curr=kitapVeritabani.cursor()
    curr.execute(''' INSERT INTO kitapKaydi (uyeID,uyeAdi,kitapISBN,tarih) VALUES 
    (?,?,?,?)''',(uyeNo,uye,ISBNNumber,tarih))
    kitapVeritabani.commit()
    kitapVeritabani.close()

# ---------------------------------------------------------------------------- #
def duzenle():
      secilen=listeKutusu.curselection()
      secilmis=secilen[0]
    
      bilgi=listeKutusu.get(secilen)
      print(bilgi[0])
      
      guncellePenceresi=Toplevel(listelePenceresi)
      guncellePenceresi.geometry("250x250")
      guncellePenceresi.title("GÜNCELLE")
      
      Label(guncellePenceresi, text="Üye Adı:").place(x=20, y=10)
      uyeAdi = Entry(guncellePenceresi)
      uyeAdi.place(x=80, y=10)

      Label(guncellePenceresi, text="ISBN:").place(x=20, y=40)
      ISBN = Entry(guncellePenceresi)
      ISBN.place(x=80, y=40)

      Label(guncellePenceresi, text="Alınış Tarihi:").place(x=20, y=80)
      AlınısTarihi = Entry(guncellePenceresi)
      AlınısTarihi.place(x=80, y=80)
      
      
      def guncelleme():
              yeniuye=uyeAdi.get()
              yeniISBNNumber=ISBN.get()
              yenitarih=AlınısTarihi.get()
              
              #veritabanı bağlantısını oluşutrduk
              kitapVeritabani=sqlite3.connect("kitapKaydi.db")
              curr=kitapVeritabani.cursor()
              curr.execute('''UPDATE KitapKaydi SET uyeAdi=?,  kitapISBN=? , tarih=? 
                           WHERE uyeID=?  ''', (yeniuye,yeniISBNNumber,yenitarih,bilgi[0])  )
              kitapVeritabani.commit()
              kitapVeritabani.close() 
                
              Listele()   

      guncelleButon=Button(guncellePenceresi,text="GUNCELLE",command=guncelleme)
      guncelleButon.place(x=120,y=120)
      
     
      
def sil():
      
      cevap=messagebox.askokcancel("Onay Kutusu","Silmek istediğinize emin misiniz?:")
      
      if cevap:          
          secilen=listeKutusu.curselection()
          secilmis=secilen[0]        
          bilgi=listeKutusu.get(secilen)
          print(bilgi[0])
          #veritabanı bağlantısını oluşutrduk
          kitapVeritabani=sqlite3.connect("kitapKaydi.db")
          curr=kitapVeritabani.cursor()
          curr.execute(''' DELETE FROM kitapKaydi WHERE uyeId=?''',(bilgi[0],)  )
          kitapVeritabani.commit()
          kitapVeritabani.close() 
          Listele()





def Listele():
      global listeKutusu
      global listelePenceresi
      listelePenceresi=Toplevel(ekran)
      listelePenceresi.geometry("350x500+500+300")
      listelePenceresi.title("Listeleme Ekranı")
      
      duzenleButton=Button(listelePenceresi,text="DÜZENLE",command=duzenle)
      duzenleButton.place(x=280,y=50)
      
      silButton=Button(listelePenceresi,text="KAYIT SİL",command=sil)
      silButton.place(x=280,y=90)
      
      
      # Veritabanı bağlantısı
      kitapVeritabani=sqlite3.connect("kitapKaydi.db")
      curr=kitapVeritabani.cursor()
      # Yapılacak işlemler bu arada yapılıyor. Sadece bu kısım değişiyor
      curr.execute(''' SELECT * FROM  kitapKaydi''')
      # fetch işlemi bir şeyi al getir anlamında. Burdada verileri çekmek için kullanılır.
      bilgiler=curr.fetchall()
  
      kitapVeritabani.close()
      listeKutusu=Listbox(listelePenceresi,height=20,width=40)
      listeKutusu.place(x=20,y=10)
      
      for bilgi in bilgiler:
            listeKutusu.insert(END,bilgi)
      







# # Resim Ekleme
# resim = Image.open("images\kitapKurdu.png")  # Resmi aç
# resim = resim.resize((200, 200), Image.ANTIALIAS)  # Resmi boyutlandır
# resim = ImageTk.PhotoImage(resim)  # Resmi Tkinter PhotoImage nesnesine dönüştür
# etiket = Label(ekran, image=resim)  # Etiket oluştur
# etiket.place(x=500, y=30)  # Sağ üst köşeye yerleştir

# ---------------------------------------------------------------------------- #
# Girişler ve Etiketler
Label(ekran, text="Üye ID:").place(x=100, y=20)
uyeID = Entry(ekran)
uyeID.place(x=200, y=20)

Label(ekran, text="Üye Adı:").place(x=100, y=50)
uyeAdi = Entry(ekran)
uyeAdi.place(x=200, y=50)

Label(ekran, text="ISBN:").place(x=100, y=80)
ISBN = Entry(ekran)
ISBN.place(x=200, y=80)

Label(ekran, text="Alınış Tarihi:").place(x=100, y=110)
AlınısTarihi = Entry(ekran)
AlınısTarihi.place(x=200, y=110)

# ---------------------------------------------------------------------------- #
# Kaydet Butonu
kaydetButon = Button(ekran, text="KAYDET", command=Kaydet)
kaydetButon.place(x=150, y=140) 

listeleButton=Button(ekran,text="LİSTELE",command=Listele)
listeleButton.place(x=210,y=140)



ekran.mainloop()

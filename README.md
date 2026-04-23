# 🧨 Minesweeper (PyQt5)

Modern arayüze sahip, geliştirilmiş özellikler içeren klasik **Minesweeper (Mayın Tarlası)** oyunu.

---

## 📌 İçindekiler

* [Proje Amacı](#-proje-amacı)
* [Özellikler](#-özellikler)
* [Kullanılan Teknolojiler](#-kullanılan-teknolojiler)
* [Kurulum (Windows)](#-kurulum-windows)
* [Çalıştırma](#-çalıştırma)
* [Oyun Nasıl Oynanır](#-oyun-nasıl-oynanır)
* [Proje Yapısı](#-proje-yapısı)
* [Geliştirilecek Özellikler](#-geliştirilecek-özellikler)

---

## 🎯 Proje Amacı

Bu proje, klasik Minesweeper oyununu:

* modern bir arayüzle yeniden tasarlamak
* kullanıcı deneyimini iyileştirmek
* PyQt5 ile masaüstü uygulama geliştirmeyi öğrenmek

amacıyla geliştirilmiştir.

---

## ✨ Özellikler

* 🎨 Modern ve karanlık tema (gradient arka plan)
* ⏱️ Canlı timer sistemi
* 💣 Kalan mayın sayacı
* ⚙️ Ayarlar paneli (satır, sütun, mayın sayısı)
* 🔄 Restart butonu
* 🚫 İlk tıklamada mayın gelmez (first-click safe)
* 🧠 Smart Click (otomatik açma)
* 🏆 Kazanma & kaybetme ekranları
* 💥 Kaybedince tüm mayınları gösterme

---

## 🛠️ Kullanılan Teknolojiler

* Python 3.x
* PyQt5 (GUI)
* OOP (Object-Oriented Programming)
* Custom UI styling (Qt Stylesheets)

---

## 💻 Kurulum (Windows)

### 1. Python Kurulumu

Eğer Python yüklü değilse:
👉 https://www.python.org/downloads/

Kurarken:
✔️ "Add Python to PATH" seçeneğini işaretle

---

### 2. Gerekli Kütüphaneler

Terminal / CMD aç:

```bash
pip install PyQt5
```

---

## ▶️ Çalıştırma

Proje klasörüne git:

```bash
cd "proje_yolu"
```

Sonra çalıştır:

```bash
python main.py
```

---

## 🎮 Oyun Nasıl Oynanır

* Sol tık → Kareyi açar
* Sağ tık → Bayrak koyar 🚩

Amaç:
👉 Mayınlara basmadan tüm güvenli kareleri açmak

### 🧠 Smart Click

Eğer bir kare:

* Açılmışsa
* Etrafındaki bayrak sayısı, sayı ile eşleşiyorsa

👉 Tekrar tıklayınca çevresindeki kareler otomatik açılır

---

## 📁 Proje Yapısı

```
Minesweeper/
│
├── core/              # Oyun mantığı
│   ├── board.py
│   └── cell.py
│
├── widgets/           # UI bileşenleri
│   ├── board_widget.py
│   ├── cell_widget.py
│   └── settings_panel.py
│
├── services/          # Ses sistemi
│   └── sound_manager.py
│
├── ui/resources/      # Görseller & ikonlar
│
├── utils/
│   └── path.py
│
├── config.py          # Stil ayarları
├── main.py            # Giriş noktası
└── README.md
```

---

## 🚀 Geliştirilecek Özellikler

* 🎞️ Animasyonlar (patlama efekti vs.)
* 🧩 Zorluk seviyeleri (Easy / Medium / Hard)
* 💾 Skor kaydetme sistemi
* 🌐 Çoklu dil desteği
* 🧠 AI solver (otomatik çözüm)

---

## 👨‍💻 Geliştirici

Bu proje öğrenme ve geliştirme amacıyla yapılmıştır.

---

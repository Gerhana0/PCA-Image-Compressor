PCA Image Compressor - Kelompok 2

1. Faadhilah Hana Gustie Fatimah    (L0124012)
2. Haliza Hana Maulina              (L0124017)
3. Jelita Kustyara Nanda Safitri    (L0124020)

---

## Deskripsi Singkat

Aplikasi web sederhana berbasis Python dan Streamlit untuk mengompresi gambar menggunakan algoritma **Principal Component Analysis (PCA)**.
Aplikasi ini bertujuan untuk mendemonstrasikan bagaimana algoritma PCA dapat digunakan untuk mengurangi dimensi data pada citra berwarna (RGB),
tanpa menghilangkan terlalu banyak informasi visual.

Pengguna dapat:
- Mengunggah gambar (jpg/png/jpeg)
- Memilih jumlah **principal components** (k)
- Mengatur kualitas simpan JPEG
- Melihat gambar asli dan hasil kompresi
- Mendapatkan metrik waktu komputasi, persentase reduksi piksel, dan rasio kompresi file
- Mengunduh gambar hasil kompresi

---

## Tech Stack

- Bahasa Pemrograman: Python
- Library:
  - `streamlit` – antarmuka web interaktif
  - `numpy` – perhitungan numerik dan PCA
  - `opencv-python` (cv2) – manipulasi gambar
- Platform: Streamlit Local App

---
## Struktur Program
-eigenface_kelompok2
    - doc
        - README.txt
    - src
        - main.py   
    - test

---

Cara Menjalankan Program

1.  Pastikan Python sudah terinstal.
2.  Install dependensi:
    ```bash
    pip install streamlit numpy opencv-python
3.  Ketik streamlit run src/main.py di terminal
4.  Masukkan foto yang ingin dikompress
5.  Pilih jumlah principal components (k)
6.  Atur kualitas simpan JPEG
7.  Klik mulai kompresi
8.  Hasil berupa foto perbandingan sebelum dan sesudah kompresi.
    Selain itu juga menampilkan:
    - Waktu komputasi
    - Kompresi matriks (PCA)
    - ukuran gambar sebelum dan sesudah
    - rasio kompresi file
    - unduh kompresi file


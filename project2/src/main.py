import streamlit as st
import numpy as np
import cv2
import os
import time

# Setup halaman
st.set_page_config(page_title="PCA Image Compressor", layout="wide")

# Buat folder penyimpanan jika belum ada
os.makedirs("saved_imgs", exist_ok=True)

# Layout 2 kolom utama
col_left, col_right = st.columns([1, 2])
with col_right:
    st.markdown("<h1>Kompresi Gambar menggunakan PCA</h1>", unsafe_allow_html=True)

# Sidebar kiri (pengaturan/input)
with col_left:
    st.subheader("Pengaturan")
    uploaded_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])
    k = st.selectbox(
        "Jumlah Principal Components (k)",
        options=[10, 25, 50, 100, 150, 250],
        index=2  # default: 50
    )
    jpeg_quality = st.slider("Kualitas Simpan JPEG", min_value=10, max_value=100, value=50)
    start_btn = st.button("Mulai Kompresi")

# Fungsi PCA untuk tiap channel
def compress_channel(channel, k):
    h, w = channel.shape
    mean = np.mean(channel, axis=0)
    centered = channel - mean
    cov_matrix = (1 / (h - 1)) * (centered.T @ centered)
    eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)
    sorted_idx = np.argsort(eig_vals)[::-1]
    eig_vecs = eig_vecs[:, sorted_idx]
    eig_vecs_k = eig_vecs[:, :k]
    projected = centered @ eig_vecs_k
    reconstructed = (projected @ eig_vecs_k.T) + mean
    return reconstructed

# Jika ada file dan tombol diklik
if uploaded_file and start_btn:
    # Baca gambar dan konversi
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, 1)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    h, w, _ = image_rgb.shape
    r, g, b = cv2.split(image_rgb)

    start_time = time.time()

    # Kompresi PCA
    r_comp = compress_channel(r, k)
    g_comp = compress_channel(g, k)
    b_comp = compress_channel(b, k)
    compressed_img = cv2.merge([r_comp, g_comp, b_comp])
    compressed_img = np.clip(compressed_img, 0, 255).astype(np.uint8)

    runtime = time.time() - start_time
    original_pixels = h * w * 3
    compressed_pixels = h * k * 3 + k * w * 3
    data_compression_ratio = (1 - compressed_pixels / original_pixels) * 100

    # Simpan hasil
    save_path = f"saved_imgs/compressed_{k}_pc.jpg"
    cv2.imwrite(
        save_path,
        cv2.cvtColor(compressed_img, cv2.COLOR_RGB2BGR),
        [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    )

    # Ukuran file
    original_size = len(file_bytes)
    compressed_size = os.path.getsize(save_path)
    file_compression_ratio = (1 - compressed_size / original_size) * 100
    original_size_mb = original_size / 1024
    compressed_size_kb = compressed_size / 1024

    # Tampilkan hasil
    with col_right:
        st.markdown(f"Hasil Kompresi (k = {k})")
        img_col1, img_col2 = st.columns(2)

        with img_col1:
            st.image(image_rgb, caption="Gambar Asli", use_container_width=True)

        with img_col2:
            st.image(compressed_img, caption=f"Gambar Setelah Kompresi (k={k})", use_container_width=True)

        st.success(f"Waktu Komputasi: {runtime:.2f} detik")
        st.info(f"Kompresi Matriks (PCA): {data_compression_ratio:.2f}% lebih ringan")

        st.write(f"Ukuran Gambar: **{original_size_mb:.2f} KB** → **{compressed_size_kb:.2f} KB**")
        st.write(f"Rasio Kompresi File: **{file_compression_ratio:.2f}%**")

        if file_compression_ratio < 0:
            st.warning("Hasil file lebih besar dari aslinya. Coba turunkan nilai 'Kualitas Simpan JPEG'.")

        # Tombol unduh
        with open(save_path, "rb") as f:
            st.download_button(
                "Unduh Hasil Kompresi",
                f,
                file_name=f"compressed_{k}_pc.jpg",
                mime="image/jpeg"
            )

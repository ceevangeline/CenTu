import streamlit as st
import base64
import os

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="CenTu - Bantuan",
    page_icon="assets/Logo_Centu.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Helper: load gambar sebagai base64 ───────────────────────────────────────
def img_to_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    ext = path.rsplit(".", 1)[-1].lower()
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{data}"

logo_centu = img_to_base64("assets/Logo_Centu.png")
logo_untar = img_to_base64("assets/Logo_Untar.png")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* Dasar Layout */
* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Nunito', sans-serif;
    background-color: #E8F5E9;
    overflow-x: hidden;
    width: 100%;
}


/* Sembunyikan elemen bawaan Streamlit */
#MainMenu, header[data-testid="stHeader"], footer { display: none !important; }
[data-testid="stAppViewContainer"] > section { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Menghilangkan navigasi sidebar bawaan */
[data-testid="stSidebarNav"] {
    display: none !important;
}

            
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 72px;
    background: #4CAF50;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    z-index: 9999;
}
.navbar-left { display: flex; align-items: center; }
.navbar-left img { height: 52px; object-fit: contain; }
.navbar-center { display: flex; gap: 40px; align-items: center; }
.navbar-center a {
    text-decoration: none;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    padding: 6px 2px;
    border-bottom: 3px solid transparent;
    transition: color .2s, border-color .2s;
}
.navbar-center a:hover { color: #FFC72C; }
.navbar-center a.active {
    color: #FFC72C;
    }
.navbar-right img { height: 48px; object-fit: contain; }


/* HEADER AREA */
.header-section {
    padding: 120px 10% 20px 10%;
    text-align: center;
    background-color: #E8F5E9;
}
             
.page-title {
    color: #4CAF50 !important;
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 10px;
}

.page-subtitle {
    color: #98B899 !important;
    font-size: 20px;
    font-weight: 600;
}

/* CARDS SECTION */
.cards-container {
    padding: 20px 10% 80px 10%;
    display: flex;
    justify-content: center;
    gap: 30px;
    background-color: #E8F5E9;
    flex-wrap: wrap;
    box-sizing: border-box;
}

.card {
    background: #ffffff;
    border: 2px solid #4CAF50;
    border-radius: 16px;
    padding: 16px;
    flex: 1;
    min-width: 300px;
    max-width: 380px;
    transition: all 0.3s ease;
    text-decoration: none !important;
}

/* Hover Effect: Menyala & Terangkat */
.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(88, 177, 94, 0.2);
    border-color: #4CAF50;
}

.card h3 {
    color: #4CAF50;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 15px;
}

.card p {
    color: #98B899;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 25px;
}

.card .link-text {
    color: #4CAF50;
    font-weight: 700;
    font-size: 15px;
    text-decoration: none !important;
    cursor: pointer;
    display: inline-block;
}

.card .link-text:hover {
    color: #4CAF50;
}

/* GREEN BODY SECTION */
.green-body {
    background-color: #009951;
    width: 100;
    padding: 40px 10%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#panduan {
    padding-bottom: 0;
}

#Kategori {
    padding-bottom: 120px;
}

.section-title {
    color: #ffffff !important;
    font-size: 40px !important;
    font-weight: 600 !important;
    margin-bottom: 40px;
    text-align: center;
}

.section-subtitle {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 400 !important;
    text-align: center;
}

.info-boxes {
    display: flex;
    gap: 60px; /* Memberikan ruang yang cukup untuk panah di tengah */
    justify-content: center;
    align-items: stretch;
    width: 100%;
    max-width: 1000px; /* Mengecilkan container utama agar card lebih compact */
    flex-wrap: wrap; /* Membuat card bisa turun ke baris berikutnya jika layar sempit */
    margin-top: 40px;
}

.info-box {
    background: #ffffff;
    padding: 32px 24px;
    border-radius: 16px;
    flex: 1;
    flex-basis: 280px; /* Memberikan ukuran dasar yang lebih kecil */
    max-width: 320px;  /* Membatasi lebar maksimal card */
    position: relative;
    transition: all 0.4s ease;
    border: 2px solid #4CAF50;
    text-align: left;
}

/* Panah di Tengah Antar Card */
.info-box:not(:last-child)::after {
    content: "→";
    position: absolute;
    right: -45px; /* Menempatkan panah tepat di tengah gap */
    top: 50%;
    transform: translateY(-50%);
    font-size: 28px;
    color: rgba(255, 255, 255, 0.6);
    font-weight: 900;
    pointer-events: none;
    transition: all 0.3s ease;
}

/* Angka Tahapan */
.step-number {
    position: absolute;
    top: -20px;
    left: 25px;
    width: 40px;
    height: 40px;
    background: #FFFFFF;
    color: #4CAF50;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 900;
    font-size: 18px;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* Hover Effects */
.info-box:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    z-index: 5;
}

.info-box:hover .step-number {
    opacity: 1;
    transform: translateY(0);
}

/* Panah menjadi emas saat card kiri di-hover */
.info-box:hover::after {
    color: #FFC72C;
    right: -48px; /* Animasi dorongan kecil ke arah card selanjutnya */
}

/* Kartu selanjutnya memberikan sinyal */
.info-box:hover + .info-box {
    background: rgba(255, 255, 255, 0.15);
    border: 2px dashed #FFD700;
    transform: scale(0.97);
}

.info-box:hover + .info-box .info-box-title,
.info-box:hover + .info-box .info-box-text {
    color: #ffffff !important;
}

/* Tipografi */
.info-box-title { color: #4CAF50; font-size: 24px; font-weight: 800; margin-bottom: 12px; display: block; }
.info-box-text { color: #98B899; font-size: 16px; line-height: 1.6; }

.big-white-card {
    background: #ffffff;
    width: 100%;
    max-width: 1000px;
    padding: 32px 32px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-top: 40px;
}

.big-white-card .label-item {
    margin-bottom: 30px;
}

.big-white-card .label-name {
    color: #4CAF50;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 10px;
}

.big-white-card .label-description {
    color: #98B899;
    font-size: 20px;
    line-height: 1;
}

.footer {
    bottom: 0; left: 0; right: 0;
    height: 50px;
    background: #E8F5E9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #58B15E;
    font-weight: 600;
    border-top: 2px solid #98B899;
    z-index: 9999;
}
            
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="navbar-left">
        <img src="{logo_centu}" alt="CenTu Logo">
    </div>
    <div class="navbar-center">
        <a href="/"target="_self">Beranda</a>
        <a href="/deteksi" target="_self">Deteksi</a>
        <a href="/tentang" target="_self">Tentang</a>
        <a href="/bantuan" target="_self" class="active">Bantuan</a>
    </div>
    <div class="navbar-right">
        <img src="{logo_untar}" alt="UNTAR Logo">
    </div>
</div>
""", unsafe_allow_html=True)

# ── HEADER SECTION ────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-section">
    <h1 class="page-title">Butuh bantuan?</h1>
    <p class="page-subtitle">Temukan solusi Anda di sini.</p>
</div>
""", unsafe_allow_html=True)

# ── CARDS SECTION ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="cards-container">
    <div class="card">
        <h3>Panduan</h3>
        <p>Temukan penjelasan lengkap dan langkah penggunaan aplikasi agar pengalaman Anda menjadi lebih optimal.</p>
        <a href="#panduan" class="link-text">Telusuri →</a>
    </div>
    <div class="card">
        <h3>Kategori</h3>
        <p>Temukan penjelasan dari hasil analisis untuk membantu Anda memahami makna dari proses deteksi dengan lebih baik.</p>
        <a href="#Kategori" class="link-text">Telusuri →</a>
    </div>
    <div class="card">
        <h3>Tentang</h3>
        <p>Temukan penjelasan mengenai aplikasi ini agar Anda dapat memahaminya dengan lebih baik.</p>
        <a href="/tentang" class="link-text" target="_self">Telusuri →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PANDUAN DETEKSI SECTION ──────────────────────────────────────────────────
st.markdown("""
<div class="green-body" id="panduan">
<h2 class="section-title">Panduan Deteksi</h2>
<p class="section-subtitle">Ikuti langkah-langkah berikut untuk mulai melakukan deteksi pada platform ini.</p>
<div class="info-boxes">
<div class="info-box">
<span class="info-box-title">1. Input Teks</span>
<p class="info-box-text">Pada halaman Beranda, klik tombol "Mulai Deteksi" untuk memulai proses analisis.</p>
</div>
<div class="info-box">
<span class="info-box-title">2. Proses Deteksi</span>
<p class="info-box-text">Masukkan teks pada kolom input yang tersedia, lalu tekan tombol "Deteksi".</p>
</div>
<div class="info-box">
<span class="info-box-title">3. Hasil Analisis</span>
<p class="info-box-text">Sistem akan memproses teks secara otomatis dan menampilkan hasil deteksi pada layar.</p>
</div>
</div>
</div>

<div class="green-body" id="Kategori">
<h2 class="section-title">Kategori</h2>
<p class="section-subtitle">
Penjelasan hasil dilakukan untuk membantu Anda memahami arti dari setiap hasil yang ditampilkan.
</p>
        
<div class="big-white-card">
<div class="label-item">
<div class="label-name">Abusive</div>
<div class="label-description">
Label ini menunjukkan bahwa teks mengandung bahasa yang bersifat kasar, menghina, atau menyerang secara verbal. Biasanya ditandai dengan penggunaan kata-kata tidak sopan yang dapat menyinggung atau melukai perasaan pihak lain.
</div>
</div>

<div class="label-item">
<div class="label-name">Rasis</div>
<div class="label-description">
Label ini menandakan adanya unsur diskriminasi atau pernyataan yang menyerang ras, etnis, maupun kelompok tertentu. Hal ini biasanya berkaitan dengan stereotip, generalisasi negatif, atau bentuk penghinaan terhadap identitas suatu kelompok.
</div>
</div>

<div class="label-item">
<div class="label-name">Non Hate Speech</div>
<div class="label-description">
Label ini menunjukkan bahwa teks tidak tergolong sebagai ujaran kebencian. Kalimat masih berada dalam kategori aman atau netral, meskipun dapat memuat opini atau ekspresi emosi tanpa unsur serangan yang berbahaya.
</div>
</div>

<div class="label-item" style="margin-bottom:0;">
<div class="label-name">Alasan</div>
<div class="label-description">
Pada bagian ini, aplikasi akan memberikan penjelasan singkat mengenai alasan suatu teks diklasifikasikan ke dalam kategori tertentu. Penjelasan tersebut disusun berdasarkan hasil analisis, sehingga pengguna dapat memahami mengapa sebuah kalimat termasuk ke dalam label yang diberikan.
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Copyright @ CenTu 2026
</div>
""", unsafe_allow_html=True)

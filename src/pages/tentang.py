import streamlit as st
import base64
import os

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="CenTu - Tentang",
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

# Muat Asset
logo_centu = img_to_base64("assets/Logo_Centu.png")
logo_untar = img_to_base64("assets/Logo_Untar.png")
logo_centularge = img_to_base64("assets/Logo_Centu.png") 
foto_levina = img_to_base64("assets/levina.jpg")
foto_janson = img_to_base64("assets/janson.jpg")
foto_irvan = img_to_base64("assets/irvan.jpg")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* Dasar Layout */
* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Nunito', sans-serif;
    background-color: #E8F5E9;
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


/* BODY AREA */
.page-body {
    margin-top: 75px; /* Sesuai tinggi navbar */
}

/* SECTION 1: MENGENAL CENTU */
.about-hero {
    padding: 80px 10%;
    display: flex;
    align-items: center;
    gap: 50px;
    background-color: #E8F5E9;
}
.hero-image { flex: 1; text-align: center; }
.hero-image img { width: 300px; }
.hero-text { flex: 2; }
.hero-text h2 {
    color: #58B15E;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 20px;
}
.hero-text p {
    color: #808080;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 15px;
    text-align: justify;
}

/* SECTION 2: TIM AKADEMIK */
.team-section {
    background-color: #009444; /* Hijau lebih gelap */
    padding: 80px 10%;
    text-align: center;
}
.team-section h3 {
    color: #ffffff;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 50px;
}
.team-grid {
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
}
.team-card {
    background: white;
    width: 240px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}
.team-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(76, 175, 80, 0.4);
}
.photo-box {
    width: 100%;
    height: 280px;
    background-color: #f0f0f0;
    overflow: hidden;
}
.photo-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}
.team-card:hover .photo-box img {
    transform: scale(1.08);
}
.card-info {
    padding: 16px;
    text-align: center;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    align-items: center;
    justify-content: center;
    height: 100px;
}
.card-info h4 {
    color: #009444;
    font-size: 16px;
    font-weight: 800;
    line-height: 1.4;
}
.card-info .role {
    color: #999999;
    font-size: 14px;
    font-weight: 600;
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
        <img src="{logo_centularge}" alt="CenTu Logo">
    </div>
    <div class="navbar-center">
        <a href="/" target="_self">Beranda</a>
        <a href="/deteksi" target="_self">Deteksi</a>
        <a href="/tentang" target="_self" class="active">Tentang</a>
        <a href="/bantuan" target="_self">Bantuan</a>
    </div>
    <div class="navbar-right">
        <img src="{logo_untar}" alt="UNTAR Logo">
    </div>
</div>
""", unsafe_allow_html=True)

# ── BODY CONTENT ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-body">
<section class="about-hero">
<div class="hero-image">
<img src="{logo_centularge}" alt="CenTu Logo Large">
</div>
<div class="hero-text">
<h2>Mengenal CenTu: Penjaga Etika Berbahasa di Era Digital</h2>
<p>
CenTu merupakan aplikasi yang dirancang untuk membantu mendeteksi dan memahami ujaran kebencian dalam teks digital. 
Nama CenTu berasal dari gabungan kata <b>Cendol</b> dan <b>Tujah</b> yang merepresentasikan keseimbangan antara kecerdasan yang segar dalam memahami konteks bahasa serta ketegasan dalam mengidentifikasi konten bernuansa negatif secara tepat.
</p>
<p>
Aplikasi ini dikembangkan sebagai bagian dari tugas akhir Strata Satu dengan tujuan mendukung terciptanya ruang digital yang lebih aman dan sehat. 
CenTu berfokus pada deteksi ujaran kebencian dalam bahasa Indonesia serta bahasa serumpun Melayu Sumatra yang masih kurang terakomodasi oleh sistem deteksi umum, sehingga diharapkan dapat membantu meningkatkan kualitas interaksi di dunia digital.
</p>
</div>
</section>

<section class="team-section">
<h3>Tim Akademik CenTu</h3>
<div class="team-grid">
<div class="team-card">
<div class="photo-box"><img src="{foto_levina}"></div>
<div class="card-info">
<h4>Levina Grace Evangeline</h4>
<p class="role">Pengembang Aplikasi</p>
</div>
</div>
<div class="team-card">
<div class="photo-box"><img src="{foto_janson}"></div>
<div class="card-info">
<h4>Janson Hendryli<br>S.Kom. M.Kom.</h4>
<p class="role">Dosen Pembimbing Utama</p>
</div>
</div>
<div class="team-card">
<div class="photo-box"><img src="{foto_irvan}"></div>
<div class="card-info">
<h4>Irvan Lewenusa<br>S.Kom., M.Kom.</h4>
<p class="role">Dosen Pembimbing Pendamping</p>
</div>
</div>
</div>
</section>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Copyright @ CenTu 2026
</div>
""", unsafe_allow_html=True)

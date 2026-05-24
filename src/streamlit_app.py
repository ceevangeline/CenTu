import streamlit as st
import base64
import os

st.set_page_config(
    page_title="CenTu - Beranda",
    page_icon="assets/Logo_Centu.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load gambar sebagai base64
def img_to_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    ext = path.rsplit(".", 1)[-1].lower()
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{data}"

logo_centu = img_to_base64("assets/Logo_CenTu.png")
logo_untar = img_to_base64("assets/Logo_Untar.png")

# CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Nunito', sans-serif;
    background-color: #e8f5e9;
    min-height: 100vh;
    overflow-y: auto !important;      
}

#MainMenu, header[data-testid="stHeader"], footer { display: none !important; }
[data-testid="stAppViewContainer"] > section { 
    padding: 0 !important; 
}
            
[data-testid="stVerticalBlock"] { 
    gap: 0 !important; 
}

.block-container { 
    padding: 0 !important; 
    max-width: 100% !important; 
}

[data-testid="stSidebarNav"] {
    display: none !important;
}

/* 1. Navbar */         
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
.navbar-center a.active { color: #FFC72C;}
.navbar-right img { height: 48px; object-fit: contain; }

/* 2. BODY AREA */
.page-body {
    margin-top: 72px;
    min-height: calc(100vh - 120px);
    background: linear-gradient(160deg, #E8F5E9 0%, #E8F5E9 60%);
    display: flex;
    align-items: center;
    padding: 60px 80px;
    position: relative;
    overflow: hidden;
    justify-content: center;
    text-align: center;
}
            
.hero-text { max-width: 100%; }
.hero-text h1 {
    font-size: 40px;
    font-weight: 900;
    color: #4CAF50;
    line-height: 1.5;
    margin-bottom: 24px;
}
.hero-text p {
    font-size: 28px;
    font-weight: 600;
    color: #98B899;
    line-height: 1.5;
    margin-bottom: 36px;
}
            
.btn-deteksi {
    display: inline-block;
    background: #009951;
    color: #fff !important;
    font-size: 1rem;
    font-weight: 700;
    padding: 12px 32px;
    border-radius: 8px;
    text-decoration: none !important;
    transition: background .2s, transform .15s;
    cursor: pointer;
    border: none;
}

.btn-deteksi:hover { 
    background: #1b5e20; 
    transform: translateY(-2px); 
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

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="navbar-left">
        <img src="{logo_centu}" alt="CenTu Logo">
    </div>
    <div class="navbar-center">
        <a href="/" target="_self" class="active">Beranda</a>
        <a href="/deteksi" target="_self">Deteksi</a>
        <a href="/tentang" target="_self">Tentang</a>
        <a href="/bantuan" target="_self">Bantuan</a>
    </div>
    <div class="navbar-right">
        <img src="{logo_untar}" alt="UNTAR Logo">
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-body">
    <div class="hero-text">
        <h1>Layaknya cendol yang melalui saringan agar manisnya terasa sempurna,
            CenTu menyaring setiap kata di dunia digital.</h1>
        <p>Masukkan teksmu sekarang dan lihat apakah<br>aman dari ujaran kebencian.</p>
        <a class="btn-deteksi" href="/deteksi" target="_self">Mulai Deteksi</a>  
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">Copyright @ CenTu 2026</div>
""", unsafe_allow_html=True)
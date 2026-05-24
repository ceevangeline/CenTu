import streamlit as st
import base64
import os
import html
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM
)

# ── Konfigurasi Halaman ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="CenTu - Deteksi",
    page_icon="assets/Logo_Centu.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Konfigurasi Model ─────────────────────────────────────────────────────────
MODEL_PATH         = "lelevinana/CenTu-Encoder"
DECODER_MODEL_PATH = "lelevinana/CenTu-Decoder"

LABEL_MAP = {
    0: "Abusive",
    1: "Rasis",
    2: "Non Hate"
}

# ── Deteksi Device (GPU jika ada, fallback ke CPU) ────────────────────────────
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Helper: Load Gambar sebagai Base64 ───────────────────────────────────────
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

# ── Fungsi Load Model ─────────────────────────────────────────────────────────
def load_encoder():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH,
        low_cpu_mem_usage=False
    )
    model.eval()
    return tokenizer, model

def load_decoder():
    decoder_tokenizer = AutoTokenizer.from_pretrained(DECODER_MODEL_PATH)
    decoder_model = AutoModelForSeq2SeqLM.from_pretrained(
        DECODER_MODEL_PATH,
        low_cpu_mem_usage=False
    )
    decoder_model.eval()
    return decoder_tokenizer, decoder_model

# ── Fungsi Prediksi Label ─────────────────────────────────────────────────────
def prediksi_teks(teks: str, threshold: float = 0.5):
    tokenizer = st.session_state["tokenizer"]
    model     = st.session_state["model"]

    inputs = tokenizer(
        teks,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    # Pindahkan input ke device yang sama dengan model
    if DEVICE.type != "cpu":
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.inference_mode():
        outputs = model(**inputs)
        probs   = torch.sigmoid(outputs.logits)[0]

    hasil = [
        {"label": LABEL_MAP.get(i, f"LABEL_{i}"), "score": prob.item()}
        for i, prob in enumerate(probs)
        if prob.item() >= threshold
    ]

    # Fallback: ambil label dengan score tertinggi jika tidak ada yang lewat threshold
    if not hasil:
        best_idx = probs.argmax().item()
        hasil.append({
            "label": LABEL_MAP.get(best_idx, f"LABEL_{best_idx}"),
            "score": probs[best_idx].item()
        })

    return hasil

# ── Fungsi Generate Alasan ────────────────────────────────────────────────────
def generate_alasan(teks: str, label: str) -> str:
    decoder_tokenizer = st.session_state["decoder_tokenizer"]
    decoder_model     = st.session_state["decoder_model"]

    prompt = f"Jelaskan alasan mengapa teks berikut termasuk {label}: {teks}"

    inputs = decoder_tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    # Pindahkan input ke device yang sama dengan model
    if DEVICE.type != "cpu":
         inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.inference_mode():
        output_ids = decoder_model.generate(
            **inputs,
            max_length=100,
            num_beams=1,
            early_stopping=True
        )

    return decoder_tokenizer.decode(output_ids[0], skip_special_tokens=True)

# ── Fungsi Reset Teks ─────────────────────────────────────────────────────────
def reset_teks():
    st.session_state["teks_key"] += 1

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Nunito', sans-serif;
    background-color: #e8f5e9;
}

#MainMenu, header[data-testid="stHeader"], footer { display: none !important; }
[data-testid="stAppViewContainer"] > section { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* Navbar */
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
.navbar-center a.active { color: #FFC72C; }
.navbar-right img { height: 48px; object-fit: contain; }

/* Body */
.page-body {
    margin-top: 20px;
    padding: 60px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: visible !important;
}

.hero-title {
    color: #4CAF50 !important;
    font-size: 40px;
    font-weight: 900;
    margin-bottom: 20px;
    text-align: center;
    width: 100%;
}

.hero-subtitle {
    color: #98B899 !important;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 30px;
    text-align: center;
    width: 100%;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 14px !important;
    border: 2px solid #c5dcc0 !important;
    padding: 20px !important;
    font-size: 16px !important;
    background-color: #ffffff !important;
    color: #000000 !important;

    box-shadow: none !important;
    outline: none !important;

    transition: 0.2s ease-in-out;
}

/* Saat textarea difokuskan */
.stTextArea textarea:focus {
    border: 2px solid #58B15E !important;
    box-shadow: 0 0 0 2px rgba(88, 177, 94, 0.15) !important;
    outline: none !important;
}

/* Placeholder */
.stTextArea textarea::placeholder {
    color: #9e9e9e !important;
    opacity: 1 !important;
}

/* ── Tombol ───────────────────────────────────────── */
div.stButton > button {
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    transition: 0.2s ease-in-out !important;
    margin-top: 10px !important;
    margin-bottom: 80px !important;
}

/* Tombol Mulai Ulang */
button[kind="secondary"] {
    background-color: #ffffff !important;
    color: #58B15E !important;
    border: 2px solid #58B15E !important;
}

/* Hover tombol Mulai Ulang */
button[kind="secondary"]:hover {
    background-color: #f3fff4 !important;
    color: #58B15E !important;
    border: 2px solid #58B15E !important;
}

/* Tombol Deteksi */
button[kind="primary"] {
    background-color: #58B15E !important;
    color: white !important;
    border: none !important;
}

/* Hover tombol Deteksi */
button[kind="primary"]:hover {
    background-color: #449d48 !important;
    color: white !important;
}

/* Footer */
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
        <a href="/" target="_self">Beranda</a>
        <a href="/deteksi" target="_self" class="active">Deteksi</a>
        <a href="/tentang" target="_self">Tentang</a>
        <a href="/bantuan" target="_self">Bantuan</a>
    </div>
    <div class="navbar-right">
        <img src="{logo_untar}" alt="UNTAR Logo">
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load Model via Session State ──────────────────────────────────────────────
if "models_loaded" not in st.session_state:
    tokenizer, model                      = load_encoder()
    decoder_tokenizer, decoder_model      = load_decoder()
    st.session_state["models_loaded"]     = True
    st.session_state["tokenizer"]         = tokenizer
    st.session_state["model"]             = model
    st.session_state["decoder_tokenizer"] = decoder_tokenizer
    st.session_state["decoder_model"]     = decoder_model

# ── Init Session State Lainnya ────────────────────────────────────────────────
if "teks_key" not in st.session_state:
    st.session_state["teks_key"] = 0

# ── Body ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-body">', unsafe_allow_html=True)

st.markdown('<h1 class="hero-title">Mulai Deteksi</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Mendeteksi ujaran kebencian secara otomatis dan menampilkan teks dengan label Abusive, Rasis atau Non-Hate.</p>',
    unsafe_allow_html=True
)

# ── Input Area ────────────────────────────────────────────────────────────────
with st.container():
    _, col_mid, _ = st.columns([1, 4, 1])

    with col_mid:
        input_user = st.text_area(
            label="Input Teks",
            placeholder="Masukkan teks yang ingin dideteksi di sini...",
            height=250,
            label_visibility="collapsed",
            key=f"input_area_{st.session_state['teks_key']}"
        )

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([2, 1, 0.8, 0.8])

        with c3:
            st.button("Mulai Ulang", use_container_width=True, on_click=reset_teks)

        with c4:
            btn_deteksi = st.button("Deteksi", type="primary", use_container_width=True)

        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# ── Hasil Analisis Teks ────────────────────────────────────────────────────────────
if btn_deteksi:
    if not input_user.strip():
        st.warning("Silakan isi teks terlebih dahulu sebelum mendeteksi.")
    else:
        with st.spinner("Sedang menganalisis teks..."):
            hasil_prediksi = prediksi_teks(input_user, threshold=0.5)

            label_output = ", ".join([
                f"{item['label']} ({item['score']:.2%})"
                for item in hasil_prediksi
            ])

            alasan_output = "\n".join([
                f"{item['label']}: {generate_alasan(input_user, item['label'])}"
                for item in hasil_prediksi
            ])

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='text-align: center; color: #4CAF50; margin-bottom: 16px;'>Hasil Analisis</h3>",
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div style="width: 100%; margin-bottom: 100px;">
            <table style="width: 100%; border-collapse: collapse; border-radius: 15px; overflow: hidden;
                          background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <thead>
                    <tr style="background-color: #58B15E; color: white; text-align: center;">
                        <th style="padding: 15px;">Teks</th>
                        <th style="padding: 15px;">Label</th>
                        <th style="padding: 15px;">Alasan</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="text-align: center; color: #555; background: white;">
                        <td style="padding: 15px; border-bottom: 1px solid #eee;">{html.escape(input_user)}</td>
                        <td style="padding: 15px; border-bottom: 1px solid #eee; font-weight: bold; color: #c0392b;">{html.escape(label_output)}</td>
                        <td style="padding: 15px; border-bottom: 1px solid #eee;">{html.escape(alasan_output)}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">Copyright @ CenTu 2026</div>
""", unsafe_allow_html=True)
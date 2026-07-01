import streamlit as st
import base64
import os
import re
from collections import Counter
from pathlib import Path
import pandas as pd
import torch
import html
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM
)


# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="CenTu - Deteksi",
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


# ── Path Model ───────────────────────────────────────────────────────────────
MODEL_PATH = "model_multilabel_final_2"
DECODER_MODEL_PATH = "decoder_model_final"


# ── Label Model Klasifikasi ──────────────────────────────────────────────────
LABEL_MAP = {
    0: "Abusive",
    1: "Rasis",
    2: "Non Hate"
}

# ── Load Model Klasifikasi ───────────────────────────────────────────────────
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )

    model.eval()
    return tokenizer, model


# ── Load Model Decoder Alasan ────────────────────────────────────────────────
@st.cache_resource
def load_decoder_model():
    decoder_tokenizer = AutoTokenizer.from_pretrained(
        DECODER_MODEL_PATH,
        local_files_only=True
    )

    decoder_model = AutoModelForSeq2SeqLM.from_pretrained(
        DECODER_MODEL_PATH,
        local_files_only=True
    )

    decoder_model.eval()
    return decoder_tokenizer, decoder_model


tokenizer, model = load_model()
decoder_tokenizer, decoder_model = load_decoder_model()


# ── Fungsi Prediksi Label ────────────────────────────────────────────────────
def prediksi_teks(teks: str, threshold: float = 0.5):
    inputs = tokenizer(
        teks,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits)[0]

    hasil = []

    for i, prob in enumerate(probs):
        if prob.item() >= threshold:
            hasil.append({
                "label": LABEL_MAP.get(i, f"LABEL_{i}"),
                "score": prob.item()
            })

    # Jika tidak ada label yang melewati threshold, ambil score tertinggi
    if not hasil:
        top_idx = torch.argmax(probs).item()
        hasil.append({
            "label": LABEL_MAP.get(top_idx, f"LABEL_{top_idx}"),
            "score": probs[top_idx].item()
        })

    return hasil


# ── Fungsi Generate Alasan ───────────────────────────────────────────────────
def generate_alasan(teks: str, label: str):
    prompt = f"Jelaskan alasan mengapa teks berikut termasuk {label}: {teks}"

    inputs = decoder_tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        output_ids = decoder_model.generate(
            **inputs,
            max_length=150,
            num_beams=4,
            early_stopping=True
        )

    alasan = decoder_tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return alasan


def reset_teks():
    # Mengubah angka di belakang key agar widget dianggap baru oleh Streamlit
    st.session_state["teks_key"] += 1
    # Juga mengosongkan variabel output jika ada
    st.session_state["input_teks_area"] = ""


# ── Konstanta Validasi Input ────────────────────────────────────────────────
MIN_WORD_LENGTH = 4
MAX_CONSONANT_VOWEL_RATIO = 3.0
VOWELS = set("aiueoAIUEO")


def is_random_word(word: str) -> bool:
    """Return True jika token terlihat seperti karakter acak (bukan kata nyata)."""
    clean = re.sub(r"[^A-Za-z]", "", word)

    # Kata terlalu pendek, abaikan (hindari flag pada "di", "ke", "if", "war", "dan")
    if len(clean) < MIN_WORD_LENGTH:
        return False

    clean_lower = clean.lower()
    vowel_count = sum(1 for c in clean_lower if c in VOWELS)
    consonant_count = len(clean_lower) - vowel_count

    # Tidak ada vokal sama sekali -> bukan kata nyata (mis. "krbbsb", "xyz")
    if vowel_count == 0:
        return True

    # Rasio konsonan:vokal terlalu tinggi (mis. "adgvasgydgyasdy")
    if (consonant_count / vowel_count) > MAX_CONSONANT_VOWEL_RATIO:
        return True

    # 3+ konsonan berurutan (mis. "karbibisbbf" mengandung "rbb")
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{3,}", clean_lower):
        return True

    return False


# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* Dasar Layout */
* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Nunito', sans-serif;
    background-color: #e8f5e9;
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

.navbar-center {
    display: flex;
    gap: 40px;
    align-items: center;
}

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

/* STYLING TEXT AREA */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #c5dcc0;
    padding: 20px !important;
    font-size: 16px !important;
    background-color: #ffffff !important;
    overscroll-behavior: contain !important;
}

/* Tombol Custom */
div.stButton > button {
    border-radius: 8px !important;
    padding: 10px 25px !important;
    margin-top: 10px !important;
    font-weight: 700 !important;
    margin-bottom: 100px;
}

/* Tombol Mulai Ulang */
div[data-testid="column"]:nth-child(1) button {
    background-color: white !important;
    color: #58B15E !important;
    border: 1px solid #58B15E !important;
    }

/* Tombol Deteksi */
div[data-testid="column"]:nth-child(2) button {
    background-color: #00A651 !important;
    color: white !important;
    border: none !important;
    }

/* FOOTER */
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


# ── NAVBAR ───────────────────────────────────────────────────────────────────
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


# ── BODY AREA ────────────────────────────────────────────────────────────────
st.markdown('<div class="page-body">', unsafe_allow_html=True)

st.markdown(
    '<h1 class="hero-title">Mulai Deteksi</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="hero-subtitle">Mendeteksi ujaran kebencian secara otomatis dan menampilkan teks dengan label Abusive, Rasis atau Non-Hate.</p>',
    unsafe_allow_html=True
)


# Container Box Input
with st.container():
    _, col_mid, _ = st.columns([1, 4, 1])

    with col_mid:
        if "teks_key" not in st.session_state:
            st.session_state["teks_key"] = 0

        # Area Input dengan KEY DINAMIS
        input_user = st.text_area(
            label="Input Teks",
            placeholder="Masukkan teks yang ingin dideteksi di sini...",
            height=250,
            label_visibility="collapsed",
            key=f"input_area_{st.session_state['teks_key']}"
        )

        # Jarak antara input dan tombol
        st.markdown(
            "<div style='margin-top: 20px;'></div>",
            unsafe_allow_html=True
        )

        # Baris Tombol
        c1, c2, c3, c4 = st.columns([2, 1, 0.8, 0.8])

        with c3:
            st.button(
                "Mulai Ulang",
                use_container_width=True,
                on_click=reset_teks
            )

        with c4:
            btn_deteksi = st.button(
                "Deteksi",
                type="primary",
                use_container_width=True
            )

        # Jarak antara tombol dan hasil
        st.markdown(
            "<div style='margin-bottom: 40px;'></div>",
            unsafe_allow_html=True
        )

        # ── HASIL ANALISIS ──
        if btn_deteksi:
            teks_stripped = input_user.strip()

            if not teks_stripped:
                st.warning("Silakan isi teks terlebih dahulu sebelum mendeteksi.")

            else:
                kata_kata = re.findall(r"[A-Za-z']+", teks_stripped)

                if len(kata_kata) < 2:
                    st.warning("Teks harus memiliki minimal 2 kata untuk dapat dideteksi.")

                elif any(is_random_word(k) for k in kata_kata):
                    st.warning("Teks ini tidak terdeteksi sebagai kalimat.")

                else:
                    # Terapkan threshold 0.5
                    hasil_prediksi = prediksi_teks(input_user, threshold=0.5)

                    # Gabungkan label yang melewati threshold
                    label_output = ", ".join([
                        f"{item['label']} ({item['score']:.2%})"
                        for item in hasil_prediksi
                    ])

                    # Generate alasan untuk setiap label
                    alasan_per_label = []
                    for item in hasil_prediksi:
                        alasan = generate_alasan(input_user, item['label'])
                        alasan_per_label.append(f"{item['label']}: {alasan}")
                    alasan_output = "\n".join(alasan_per_label)

                    st.write("<br>", unsafe_allow_html=True)

                    st.markdown(
                        "<h3 style='text-align: center; color: #4CAF50; margin-top: -60px; margin-bottom: 16px;'>Hasil Analisis</h3>",
                        unsafe_allow_html=True
                    )

                    st.markdown(f"""
                    <div style="width: 100%; margin-bottom: 100px;">
                        <table style="width: 100%; border-collapse: collapse; border-radius: 15px; overflow: hidden; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
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


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Copyright @ CenTu 2026
</div>
""", unsafe_allow_html=True)

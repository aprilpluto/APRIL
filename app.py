import streamlit as st
import time
from urllib.parse import quote
import base64
from pathlib import Path

st.set_page_config(page_title="💘 QUIZ VALENTINE", layout="centered")

# ================= CSS THEME =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg,#2a0000,#4a0000,#2a0000);
    color:white;
    text-align:center;
}
h1,h2,h3,p {color:#ffd9d9;}

div.stButton > button {
    background:#b33a3a;
    color:white;
    border-radius:14px;
    height:50px;
    font-size:18px;
    width:100%;
}
</style>
""", unsafe_allow_html=True)

# ================= MUSIC SYSTEM =================
def play_music():
    if Path("valentine.mp3").exists():
        audio_bytes = Path("valentine.mp3").read_bytes()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

if "music_started" not in st.session_state:
    st.session_state.music_started = False

if not st.session_state.music_started:
    st.title("💗 KLIK DULU SAYANG")
    if st.button("Mulai 💖"):
        st.session_state.music_started = True
        st.rerun()
    st.stop()

play_music()

# ================= SESSION =================
if "stage" not in st.session_state:
    st.session_state.stage="quiz"
    st.session_state.current=0
    st.session_state.score=0
    st.session_state.start_time=time.time()

# ================= QUIZ DATA =================
quiz = [
("Di mana pertemuan pertama Pluto dan April terjadi?",
 ["LIVE TIKTOK","INSTAGRAM","TWITTER","TELEGRAM"],"LIVE TIKTOK"),

("Sebagai anak koas fakultas kedokteran yang fokus pada kesehatan saraf, Mei paling sering mempelajari apa?",
 ["EKONOMI","SISTEM SARAF","PSIKOLOGI:)","HUKUM"],"SISTEM SARAF"),

("Kalau dua orang INFJ saling memahami, mereka paling nyaman berbicara dalam suasana seperti apa?",
 ["SUNYI DAN DALAM","RAMAI DAN HIRUK","DEBAT TERBUKA","KERAMAIAN"],"SUNYI DAN DALAM"),

("Pluto memanggil Meily dengan sebutan spontan yang sederhana namun bermakna apa itu?",
 ["MEI","APRIL","DOKTER","SAVIRA"],"APRIL"),

("Jika Pluto mengajak Mei mengasing sejenak dari dunia manusia April ingin pergi ke mana?",
 ["RUANG TENANG BERDUA","KONSER BESAR TULUS JANGAN DIKLIK:)","PUSAT PERBELANJAAN","STADION RAMAI"],"RUANG TENANG BERDUA")
]
# ================= QUIZ PAGE =================
if st.session_state.stage=="quiz":

    st.title("QUIZ CINTA 💖")

    q,choices,ans = quiz[st.session_state.current]
    st.subheader(q)

    selected = st.radio("",choices,key=f"q{st.session_state.current}")

    # TIMER NON BLOCKING
    time_limit = 10
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(time_limit - elapsed, 0)

    st.markdown(f"### ⏱️ {remaining} detik")

    # AUTO NEXT JIKA HABIS
    if remaining == 0:
        st.session_state.current += 1
        st.session_state.start_time = time.time()

        if st.session_state.current >= len(quiz):
            st.session_state.stage="coming"
        st.rerun()

    # TOMBOL JAWAB
    if st.button("Jawab ❤️"):
        if selected == ans:
            st.session_state.score += 1

        st.session_state.current += 1
        st.session_state.start_time = time.time()

        if st.session_state.current >= len(quiz):
            st.session_state.stage="coming"
        st.rerun()

# ================= COMING =================
elif st.session_state.stage=="coming":
    st.image("chocolate_comingsoon.png",width=250)
    st.subheader("COMING SOON YA BUAT COKLATNYA :)")
    time.sleep(2)
    st.session_state.stage="result"
    st.rerun()

# ================= RESULT =================
elif st.session_state.stage=="result":
    st.success("YEAY! SEMUA JAWABAN KAMU BENAR SAYANGKU 🎉")

    st.markdown("""
Mei,

Di sela ruang jaga dan hapalan tebalmu itu,
aku belajar bahwa perhatian tidak selalu harus bising dan terlihat mata.
Kadang cukup hadir, dan tidak pergi kemana-mana.

Orang lain melihatmu sangat kuat,
aku melihatmu tetap lembut setelah hari panjang dan penat.

Seperti Pluto yang jauh di kegelapan sana terdampar,
aku tidak perlu menjadi pusat semestamu atau bintang pulsar.
Cukup berada di orbit yang sama dan semestinya saja di sini pelan, mengimani tetap.

Dan jika suatu hari dunia terasa terlalu ramai dan membuatmu merasa kesal,
kita bisa diam sebentar di kesunyian.
Tidak untuk menghilang atau melarikan diri dari kenyataan,
hanya untuk tahu, bahwa kita masih ada di tempat yang sama dalam porosnya dan terus bergandeng tangan.

**Aku di sini di entah apa dan makhluk apa, 
Mei. Tidak lebih, tidak tumpah, tapi aku mengetukmu suka**
- Pluto, 14 Februari 2026.
""")

    if st.button("Lihat Galeri ❤️"):
        st.session_state.stage="gallery"
        st.rerun()

# ================= GALLERY =================
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  # naik 1 folder keluar dari /april

st.title("KENANGAN KITA 📸")
st.markdown("Beberapa potongan waktu yang pernah singgah — dan mungkin masih menyimpan sesuatu yang belum selesai.")

photos=[]
for i in range(1,16):
    for ext in ["JPG","jpg","jpeg","PNG","png"]:
        file=BASE_DIR / f"photo{i}.{ext}"
        if file.exists():
            photos.append(file)
            break

# tampilkan
for i in range(0,len(photos),5):
    cols=st.columns(5)
    for j in range(5):
        if i+j<len(photos):
            cols[j].image(str(photos[i+j]),use_container_width=True)

    if st.button("BUKA SURAT SINGKAT 💌"):
        st.info("Tidak semua pertemuan harus dijelaskan nona. Beberapa cukup dirasakan dan dinikmati keniscayaannya.")
        st.info("Dan beberapa orang datang, pergi pulang hilang… berggantian... mengajarkanmu tetap tumbun semakin terang")

    if st.button("↻ Ulangi Quiz"):
        st.session_state.clear()
        st.rerun()

    text="Aku baru saja dapat kejutan aneh dari planet yang spesial! EH mantan PLANET!!!!💖"
    wa=f"https://api.whatsapp.com/send?text={quote(text)}"
    st.markdown(f"[Share ke WhatsApp 💬]({wa})")
    st.markdown("[Share ke Instagram 📷](https://instagram.com)")
import streamlit as st
import joblib

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    body {
        background-color: #f9f7f7;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color:rgb(224, 235, 236);
    }
    .chat-container {
        background-color: #dbe2ef;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #f9d342;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        color: #333;
    }
    .bot-message {
        background-color: #3f72af;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        color: #fff;
    }
    .header {
        text-align: center;
        padding: 20px;
        background-color: #112d4e;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header"><h1>📚 BELAJAR BARENG CHATBOT</h1></div>', unsafe_allow_html=True)

# --- Sidebar Navigation ---
menu = st.sidebar.radio("Navigasi", ["Beranda", "Chatbot", "Tentang"])

# --- Load Model and Vectorizer ---
@st.cache_resource
def load_models():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vektor.pkl")
    return model, vectorizer

model, vectorizer = load_models()

# Daftar Sapaan dan Perpisahan
greetings = ["halo", "hello", "hai", "selamat pagi", "selamat siang", "selamat malam"]
farewells = ["bye", "selamat tinggal", "sampai jumpa", "terima kasih", "keluar", "dadah"]

# Fungsi untuk mengecek apakah input adalah sapaan
def is_greeting(user_input):
    return any(greeting in user_input for greeting in greetings)

# Fungsi untuk mengecek apakah input adalah perpisahan
def is_farewell(user_input):
    return any(farewell in user_input for farewell in farewells)

# --- Pages ---
if menu == "Beranda":
    st.title("Beranda")
    st.write("""
        Selamat datang di chatbot **Ilmu Pengetahuan Alam**.
    """)

elif menu == "Chatbot":
    st.title("Chatbot 💬")
    st.write("Hallo sahabat IPA :)")
    st.write("Apa kesusahanmu? Ayoo tanyakan disini!")

    # Inisialisasi Riwayat Chat
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["last_input"] = ""  # Menyimpan input terakhir

    # Tampilkan Riwayat Chat
    for message in st.session_state["messages"]:
        if message["sender"] == "user":
            st.markdown(f'<div class="chat-container user-message">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-container bot-message">{message["text"]}</div>', unsafe_allow_html=True)

    # Input Pengguna
    user_input = st.text_input("Ketik pesan Anda di sini:")

    if st.button("Kirim"):
        if user_input and user_input != st.session_state["last_input"]:
            # Simpan pesan pengguna
            st.session_state["messages"].append({"sender": "user", "text": user_input})
            st.session_state["last_input"] = user_input

            # Cek apakah input adalah sapaan
            if is_greeting(user_input.lower()):
                bot_response = "Halo! Ada yang bisa saya bantu?"
            elif is_farewell(user_input.lower()):
                bot_response = "Terima kasih sudah menggunakan chatbot ini. Sampai jumpa lagi!"
            else:
                # Proses dengan vektorizer dan model
                try:
                    input_vectorized = vectorizer.transform([user_input])
                    bot_response = model.predict(input_vectorized)[0]

                    # Logika fallback jika hasil prediksi tidak relevan
                    if bot_response.strip() == "" or bot_response.lower() == "unknown":
                        bot_response = "Maaf, saya tidak memahami pertanyaan Anda."
                except Exception as e:
                    bot_response = "Terjadi kesalahan dalam memproses input Anda."

            # Simpan respons bot
            st.session_state["messages"].append({"sender": "bot", "text": bot_response})


elif menu == "Tentang":
    st.title("Tentang 🚀")
    st.write("""
        Chatbot ini dibuat untuk mempermudah belajar **Ilmu Pengetahuan Alam**, dimana siswa dapat mengajukan pertanyaan mengenai kendala dalam mengerjakan soal. Serta bertanya terkait apa yang tidak diketahui di mata pelajaran **IPA** kelas 4 Sekolah Dasar atau Madrasah Ibtidaiyah.
    """)

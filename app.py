import streamlit as st
from PIL import Image
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TripAja Agency - Referensi Jalan-Jalan Indonesia", page_icon="✈️", layout="wide")

# --- DATABASE DUMMY DESTINASI ---
# Tambahan: "high_res_gallery", "tiket_masuk_orang", dan deskripsi yang lebih panjang.
# Cara implementasi gambar: Simpan foto-foto Anda di folder 'assets'.
# Berikan nama file sesuai kunci di dalam list "high_res_gallery" (contoh: bali1.jpg)
DESTINASI = {
    "Bali": {
        "highlight": "Pulau Dewata, surga dunia yang menawarkan perpaduan sempurna antara pantai eksotis, pura kuno yang mistis, budaya yang kental, dan kehidupan malam yang modern. Dari ketenangan Ubud hingga sunset di Seminyak.",
        "deskripsi_lengkap": """
            Bali tidak pernah gagal memukau. Kunjungi Pura Uluwatu yang bertengger di tebing, saksikan Tari Kecak di senja hari, atau jelajahi Teras Sawah Tegalalang.
            Bagi pecinta pantai, Nusa Penida menawarkan pemandangan tebing Kelingking yang ikonik. Nikmati juga spa kelas dunia dan kuliner lezat.
        """,
        "cover_img": "assets/bali.jpg",
        "high_res_gallery": ["assets/bali1.jpg", "assets/bali2.jpg", "assets/bali3.jpg"],
        "estimasi_biaya_katalog": "Estimasi Rp 3.500.000 / org",
        "tiket_masuk_orang": 75000, # Biaya rata-rata masuk wisata per orang
        "video_url": "https://www.youtube.com/watch?v=ScMzIvxBSi4"
    },
    "Yogyakarta": {
        "highlight": "Pusat budaya Jawa di mana kemegahan sejarah Candi Borobudur dan Prambanan bertemu dengan kehangatan Malioboro, keraton yang anggun, dan beragam kuliner legendaris yang memanjakan lidah.",
        "deskripsi_lengkap": """
            Eksplorasi Malioboro dengan andong, kunjungi Keraton Yogyakarta, dan saksikan keajaiban matahari terbit di Candi Borobudur (warisan UNESCO).
            Jangan lewatkan Goa Jomblang untuk petualangan cahaya surga, atau nikmati keindahan Gumuk Pasir Parangkusumo. Cobalah Gudeg dan Kopi Joss yang unik.
        """,
        "cover_img": "assets/jogja.jpg",
        "high_res_gallery": ["assets/jogja1.jpg", "assets/jogja2.jpg", "assets/jogja3.jpg"],
        "estimasi_biaya_katalog": "Estimasi Rp 1.500.000 / org",
        "tiket_masuk_orang": 50000,
        "video_url": "https://www.youtube.com/watch?v=F3zH94m9xBE"
    },
    "Lombok": {
        "highlight": "Tetangga Bali yang menenangkan, dikenal dengan Gunung Rinjani yang megah bagi pendaki, tiga Gili yang bebas kendaraan motor dengan perairan jernih, dan Sirkuit Internasional Mandalika yang mendunia.",
        "deskripsi_lengkap": """
            Gili Trawangan untuk pesta pantai dan snorkeling, Gili Meno untuk ketenangan, dan Gili Air untuk perpaduan keduanya. Jelajahi juga Pantai Pink yang unik.
            Bagi pendaki, Rinjani menawarkan jalur menantang dengan pemandangan Danau Segara Anak yang memukau. Kunjungi juga Desa SADE untuk belajar budaya Sasak asli.
        """,
        "cover_img": "assets/lombok.jpg",
        "high_res_gallery": ["assets/lombok1.jpg", "assets/lombok2.jpg", "assets/lombok3.jpg"],
        "estimasi_biaya_katalog": "Estimasi Rp 2.800.000 / org",
        "tiket_masuk_orang": 40000,
        "video_url": "https://www.youtube.com/watch?v=GjY8bA_5-B0"
    }
}

# --- INISIALISASI SESSION STATE (Backend Logic) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "favorit" not in st.session_state:
    st.session_state.favorit = []
# State untuk melacak halaman saat ini (Main Dashboard atau Detail)
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"
# State untuk melacak destinasi mana yang sedang dilihat detailnya
if "selected_destination" not in st.session_state:
    st.session_state.selected_destination = None
# State untuk index foto galeri (slideshow)
if "gallery_index" not in st.session_state:
    st.session_state.gallery_index = 0

# --- FUNGSI BANTUAN TAMPILKAN GAMBAR DENGAN UKURAN TETAP (CSS) ---
def tampilkan_gambar_fixed(path_gambar, width="100%", height="400px"):
    """Mengecek gambar dan menampilkan dengan ukuran fixed yang sudah ditetapkan via HTML/CSS."""
    if os.path.exists(path_gambar):
        # Menggunakan HTML agar bisa kontrol object-fit (crop/fill)
        st.markdown(
            f'<div style="width:{width}; height:{height}; overflow:hidden; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">'
            f'<img src="data:image/png;base64,...(Skip coding base64 for simplicity, standard streamlit image uses standard markdown or raw HTML)..." ' # In realistic Streamlit deployment, standard st.image is easier.
            f'style="object-fit:cover; width:100%; height:100%;">' # <--- INI PENTINGNYA: CSS agar foto proporsional dalam box fixed.
            f'</div>', unsafe_allow_html=True)
        # Fallback menggunakan st.image yang lebih mudah dalam server streamlit lokal
        try:
            img = Image.open(path_gambar)
            # Karena Streamlit lokal tidak mudah direct embed base64 di markdown, 
            # kita pakai st.image di dalam container dengan width/height yang diseragamkan
            st.image(img, use_container_width=True)
        except:
            st.error("Error loading image file.")
    else:
        # Placeholder jika gambar tidak ditemukan
        st.markdown(
            f'<div style="width:{width}; height:{height}; background-color:#e0e0e0; border-radius:10px; display:flex; align-items:center; justify-content:center; color:gray;">'
            f'📸 Foto: {path_gambar} belum ada'
            f'</div>', unsafe_allow_html=True)

# --- FUNGSI BANTUAN UNTUK MEMBACA FILE LOGO ---
def read_logo():
    try:
        return Image.open("assets/logo.png")
    except:
        return None

# --- HALAMAN LOGIN ---
def halaman_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("<br><br>", unsafe_allow_html=True)
        logo = read_logo()
        if logo: st.image(logo, use_container_width=True)
        else: st.title("✈️ TripAja Agency")
        
        st.markdown("<h2 style='text-align: center;'>Masuk ke Akun Anda</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Perusahaan under Cahyadi</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Sign In / Login", use_container_width=True)
            
            if submit_button:
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.current_page = "main" # Pastikan masuk ke dashboard utama
                    st.rerun()
                else:
                    st.error("⚠️ Username dan Password tidak boleh kosong!")

# --- HALAMAN DASHBOARD UTAMA (DAFTAR DESTINASI) ---
def render_dashboard_utama():
    st.title("TripAja - Eksplorasi Indonesia 🇮🇩")
    st.markdown("Temukan referensi perjalanan terbaik dan rencanakan impian liburan Anda.")
    
    # Reset selected destination saat kembali ke halaman utama
    st.session_state.selected_destination = None
    
    # Search bar (dummy filtering)
    search_query = st.text_input("🔍 Cari referensi wilayah (Contoh: Bali, Lombok)...")
    st.markdown("---")
    
    hasil = {k: v for k, v in DESTINASI.items() if search_query.lower() in k.lower()} if search_query else DESTINASI
    
    if hasil:
        for nama, info in hasil.items():
            col_img, col_text = st.columns([1, 2])
            with col_img:
                # Menampilkan cover image
                tampilkan_gambar_fixed(info["cover_img"], height="200px")
            with col_text:
                st.subheader(nama)
                st.write(f"{info['highlight']}") # Highlight sudah deskriptif
                st.markdown(f"**💰 {info['estimasi_biaya_katalog']}**")
                
                # TOMBOL 1: LIHAT DETAIL (MEMBUAT BERPINDAH HALAMAN)
                if st.button(f"🔎 Lihat Detail {nama}", key=f"det_{nama}"):
                    st.session_state.selected_destination = nama
                    st.session_state.current_page = "detail"
                    st.session_state.gallery_index = 0 # Reset galeri foto
                    st.rerun()
                
                # TOMBOL 2: SIMPAN KE FAVORIT
                if nama in st.session_state.favorit:
                    st.button(f"❤️ Tersimpan", key=f"fav_{nama}", disabled=True)
                else:
                    if st.button(f"🤍 Simpan ke Favorit", key=f"fav_{nama}"):
                        st.session_state.favorit.append(nama)
                        st.rerun()
            st.divider()
    else:
        st.warning("Wilayah belum tersedia di database kami.")

# --- HALAMAN DETAIL DESTINASI (MENAMPILKAN SLIDESHOW & DESKRIPSI LENGKAP) ---
def render_halaman_detail(dest_name):
    # Validasi input
    if dest_name not in DESTINASI:
        st.error("Destinasi tidak ditemukan.")
        if st.button("Kembali"): st.session_state.current_page = "main"; st.rerun()
        return

    dest = DESTINASI[dest_name]

    # Tombol Kembali
    col_back, _ = st.columns([1, 9])
    with col_back:
        if st.button("⬅️ Kembali"):
            st.session_state.current_page = "main"
            st.rerun()
    
    st.title(f"Eksplorasi Mendalam: {dest_name}")
    st.markdown(f"**Highlight:** *{dest['highlight']}*")
    st.markdown("---")

    # --- BAGIAN 1: GALERI SLIDESHOW FOTO (UKURAN TETAP) ---
    st.subheader("📸 Galeri Visual")
    
    # Mengontrol Slideshow via Backend
    gallery = dest["high_res_gallery"]
    num_photos = len(gallery)
    current_idx = st.session_state.gallery_index

    # Layout Galeri
    col_img_fixed, col_nav_gal = st.columns([3, 1])
    
    with col_img_fixed:
        # Menampilkan foto dengan ukuran seragam (CSS)
        # Note: Streamlitlokal terkadang sulit embed HTML raw, 
        # kita pakai fixed height pada container st.image.
        tampilkan_gambar_fixed(gallery[current_idx], height="450px") 
        st.write(f"<p style='text-align:center; color:gray;'>Foto {current_idx+1} dari {num_photos}</p>", unsafe_allow_html=True)
        
    with col_nav_gal:
        st.write("<br><br><br><br>", unsafe_allow_html=True) # Spacer
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Prev", key="prev_gal", use_container_width=True) and current_idx > 0:
                st.session_state.gallery_index -= 1
                st.rerun()
        with col_next:
            if st.button("Next ➡️", key="next_gal", use_container_width=True) and current_idx < (num_photos - 1):
                st.session_state.gallery_index += 1
                st.rerun()
        
        # Opsi cepat: Grid kecil thumbnail di bawah tombol
        st.write("---")
        st.write("**Lompat ke Foto:**")
        cols_thumb = st.columns(num_photos)
        for i in range(num_photos):
            with cols_thumb[i]:
                tampilkan_gambar_fixed(gallery[i], height="50px")
                if st.button(f"#{i+1}", key=f"th_{i}"):
                    st.session_state.gallery_index = i
                    st.rerun()


    # --- BAGIAN 2: DESKRIPSI LENGKAP & VIDEO ---
    st.markdown("---")
    st.subheader("📝 Penjelasan Destinasi")
    st.write(dest["deskripsi_lengkap"])
    st.video(dest["video_url"])


    # --- BAGIAN 3: FITUR TAMBAHAN KEREN (KALKULATOR ESTIMASI BIAYA WISATA) ---
    st.markdown("---")
    st.subheader("🧮 Kalkulator Estimasi Biaya Tiket & Wisata")
    st.markdown("Fitur ini membantu Anda menghitung **estimasi biaya dasar** (tiket masuk rata-rata wisata utama) di destinasi ini sebelum berangkat.")
    
    col_calc_input, col_calc_res = st.columns([1, 1])
    
    with col_calc_input:
        with st.container(border=True):
            st.markdown(f"**Data Destinasi:**")
            st.markdown(f"- Rata-rata Tiket/Wisata per Orang: `{dest['tiket_masuk_orang']}` IDR")
            jumlah_orang = st.number_input("Jumlah Orang dalam Rombongan:", min_value=1, value=2, step=1)
            jumlah_hari = st.number_input("Rencana Lama Berwisata (Hari):", min_value=1, value=3, step=1)
            
    with col_calc_res:
        with st.container(border=True):
            # Logika perhitungan di backend
            total_biaya_tiket = (jumlah_orang * dest['tiket_masuk_orang']) * jumlah_hari
            
            st.markdown("### Estimasi Total Biaya Wisata (Tiket):")
            st.markdown(f"<h2 style='color:#2e8b57;'>Rp {total_biaya_tiket:,.0f}</h2>", unsafe_allow_html=True)
            st.markdown("*Kalkulasi: (Orang x Tiket Rata-rata) x Hari. Ini belum termasuk akomodasi, makan, dan tiket pesawat.*")

# --- HALAMAN-HALAMAN LAIN (SIMPLE CHUNKS) ---
def render_galeri_cinematic():
    st.title("🎬 Galeri Video Cinematic")
    st.markdown("---")
    for nama, info in DESTINASI.items():
        st.subheader(f"Keindahan {nama}")
        st.video(info["video_url"])
        st.divider()

def render_profil():
    st.title("👤 Profil Saya")
    st.markdown("---")
    st.write(f"**Nama Pengguna:** {st.session_state.username}")
    st.subheader("❤️ Destinasi Favorit Saya")
    if st.session_state.favorit:
        for fav in st.session_state.favorit:
            st.markdown(f"- **{fav}**")
    else: st.info("Belum ada favorit.")

def render_pengaturan():
    st.title("⚙️ Pengaturan")
    st.markdown("---")
    st.selectbox("Bahasa Aplikasi", ["Indonesia", "English"])
    st.button("Simpan Pengaturan")


# --- ROUTING APLIKASI (MENU UTAMA) ---
def render_page_flow():
    # --- SIDEBAR MENU ---
    st.sidebar.title(f"TripAja Agency 👋")
    
    logo = read_logo()
    if logo: st.sidebar.image(logo, width=150)
    st.sidebar.markdown(f"**Username:** `{st.session_state.username}`")
    st.sidebar.markdown("---")
    
    # Navigasi Menu Utama
    menu = st.sidebar.radio(
        "Menu Navigasi", 
        ["🏠 Dashboard Utama", "🎬 Galeri Cinematic", "👤 Profil Saya", "⚙️ Pengaturan"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # --- PENANGANAN ROUTING HALAMAN ---
    # Jika di Dashboard Utama, kita cek apakah sedang melihat detail atau daftar
    if menu == "🏠 Dashboard Utama":
        if st.session_state.current_page == "main":
            render_dashboard_utama()
        elif st.session_state.current_page == "detail":
            render_halaman_detail(st.session_state.selected_destination)
    
    # Halaman-halaman lainnya
    elif menu == "🎬 Galeri Cinematic": render_galeri_cinematic()
    elif menu == "👤 Profil Saya": render_profil()
    elif menu == "⚙️ Pengaturan": render_pengaturan()

# --- ENTRY POINT ---
if not st.session_state.logged_in:
    halaman_login()
else:
    render_page_flow()
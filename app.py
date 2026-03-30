import streamlit as st
from PIL import Image, ImageOps
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TripAja Agency", page_icon="✈️", layout="wide")

# --- SUNTIKAN CSS CUSTOM ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .harga-text { color: #2e8b57; font-size: 20px; font-weight: bold; }
    .harga-kecil { color: #2e8b57; font-size: 16px; font-weight: bold; margin-bottom: 0px;}
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI BANTUAN ICONIFY ---
def iconify(icon_name, color="#333", size=24):
    return f'<img src="https://api.iconify.design/{icon_name}.svg?color={color.replace("#", "%23")}" width="{size}" height="{size}" style="vertical-align: middle; margin-right: 8px;">'

# --- DATABASE DUMMY DESTINASI ---
# Penambahan "biaya_dasar_int" untuk sistem backend kalkulator tabungan
DESTINASI = {
    "Bali": {
        "highlight": "Pulau Dewata, surga dunia yang menawarkan perpaduan sempurna antara pantai eksotis, pura kuno yang mistis, budaya yang kental, dan kehidupan malam yang modern.",
        "deskripsi_lengkap": "Bali tidak pernah gagal memukau. Kunjungi Pura Uluwatu yang bertengger di tebing, saksikan Tari Kecak di senja hari, atau jelajahi Teras Sawah Tegalalang. Bagi pecinta pantai, Nusa Penida menawarkan pemandangan tebing Kelingking yang ikonik. Nikmati juga spa kelas dunia dan kuliner lezat.",
        "cover_img": "assets/bali.jpg",
        "high_res_gallery": ["assets/bali1.jpg", "assets/bali2.jpg", "assets/bali3.jpg"],
        "estimasi_biaya_katalog": "Rp 3.500.000 / org",
        "biaya_dasar_int": 3500000, 
        "tiket_masuk_orang": 75000,
        "video_url": "https://youtu.be/sY6BGVE-PBE?si=K6fsvwQ6xNMV1bJ0"
    },
    "Yogyakarta": {
        "highlight": "Pusat budaya Jawa di mana kemegahan sejarah Candi Borobudur dan Prambanan bertemu dengan kehangatan Malioboro, keraton yang anggun, dan kuliner legendaris.",
        "deskripsi_lengkap": "Eksplorasi Malioboro dengan andong, kunjungi Keraton Yogyakarta, dan saksikan keajaiban matahari terbit di Candi Borobudur (warisan UNESCO). Jangan lewatkan Goa Jomblang untuk petualangan cahaya surga, atau nikmati keindahan Gumuk Pasir Parangkusumo.",
        "cover_img": "assets/jogja.jpg",
        "high_res_gallery": ["assets/jogja1.jpg", "assets/jogja2.jpg", "assets/jogja3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.500.000 / org",
        "biaya_dasar_int": 1500000,
        "tiket_masuk_orang": 50000,
        "video_url": "https://youtu.be/0Fi4JeizyZg?si=bd-AyAn-8yeFrNJ8"
    },
    "Lombok": {
        "highlight": "Tetangga Bali yang menenangkan, dikenal dengan Gunung Rinjani yang megah bagi pendaki, tiga Gili yang bebas kendaraan motor, dan Sirkuit Mandalika.",
        "deskripsi_lengkap": "Gili Trawangan untuk pesta pantai dan snorkeling, Gili Meno untuk ketenangan, dan Gili Air untuk perpaduan keduanya. Bagi pendaki, Rinjani menawarkan jalur menantang dengan pemandangan Danau Segara Anak yang memukau. Kunjungi juga Desa SADE.",
        "cover_img": "assets/lombok.jpg",
        "high_res_gallery": ["assets/lombok1.jpg", "assets/lombok2.jpg", "assets/lombok3.jpg"],
        "estimasi_biaya_katalog": "Rp 2.800.000 / org",
        "biaya_dasar_int": 2800000,
        "tiket_masuk_orang": 40000,
        "video_url": "https://youtu.be/379EEoRIbIs?si=wL9IIue4WWGHDY59"
    }
}

# --- INISIALISASI SESSION STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "favorit" not in st.session_state: st.session_state.favorit = []
if "current_page" not in st.session_state: st.session_state.current_page = "main"
if "selected_destination" not in st.session_state: st.session_state.selected_destination = None
if "gallery_index" not in st.session_state: st.session_state.gallery_index = 0

# --- FUNGSI TAMPILKAN GAMBAR ---
def tampilkan_gambar_rapi(path_gambar, target_width=800, target_height=450):
    if os.path.exists(path_gambar):
        try:
            img = Image.open(path_gambar)
            img_cropped = ImageOps.fit(img, (target_width, target_height), Image.Resampling.LANCZOS)
            st.image(img_cropped, use_container_width=True)
        except Exception:
            st.error(f"Gagal memuat {path_gambar}")
    else:
        st.warning(f"📸 Foto belum ada di: {path_gambar}")

# --- HALAMAN LOGIN ---
def halaman_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("<br><br>", unsafe_allow_html=True)
        try:
            logo = Image.open("assets/logo.png")
            st.image(logo, use_container_width=True)
        except:
            st.title("✈️ TripAja Agency")
        
        st.markdown("<h2 style='text-align: center;'>Masuk ke Akun Anda</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Sign In / Login", use_container_width=True)
            
            if submit_button:
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("⚠️ Username dan Password tidak boleh kosong!")

# --- HALAMAN DASHBOARD UTAMA ---
def render_dashboard_utama():
    st.markdown(f"<h1>{iconify('fluent-emoji:airplane')} Eksplorasi Indonesia</h1>", unsafe_allow_html=True)
    st.markdown("Temukan referensi perjalanan terbaik dan rencanakan impian liburan Anda.")
    
    st.session_state.selected_destination = None
    search_query = st.text_input("🔍 Cari referensi wilayah (Contoh: Bali, Lombok)...")
    st.markdown("---")
    
    hasil = {k: v for k, v in DESTINASI.items() if search_query.lower() in k.lower()} if search_query else DESTINASI
    
    if hasil:
        for nama, info in hasil.items():
            with st.container(border=True):
                col_img, col_text = st.columns([1, 2.5])
                with col_img:
                    tampilkan_gambar_rapi(info["cover_img"], target_width=600, target_height=400)
                with col_text:
                    st.markdown(f"<h3>{iconify('mdi:map-marker', color='#ff4b4b', size=28)} {nama}</h3>", unsafe_allow_html=True)
                    st.write(f"{info['highlight']}")
                    st.markdown(f"<p class='harga-text'>{iconify('mdi:wallet', color='#2e8b57')} Mulai dari {info['estimasi_biaya_katalog']}</p>", unsafe_allow_html=True)
                    
                    st.write("") 
                    col_btn1, col_btn2, _ = st.columns([1.5, 1.5, 3])
                    
                    with col_btn1:
                        if st.button(f"🔎 Lihat Detail", key=f"det_{nama}", use_container_width=True):
                            st.session_state.selected_destination = nama
                            st.session_state.current_page = "detail"
                            st.session_state.gallery_index = 0
                            st.rerun()
                    
                    with col_btn2:
                        if nama in st.session_state.favorit:
                            st.button(f"❤️ Tersimpan", key=f"fav_{nama}", disabled=True, use_container_width=True)
                        else:
                            if st.button(f"🤍 Simpan Favorit", key=f"fav_{nama}", use_container_width=True):
                                st.session_state.favorit.append(nama)
                                st.rerun()
    else:
        st.warning("Wilayah belum tersedia di database kami.")

# --- HALAMAN DETAIL DESTINASI ---
def render_halaman_detail(dest_name):
    dest = DESTINASI[dest_name]

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.current_page = "main"
        st.rerun()
    
    st.markdown(f"<h1>{iconify('mdi:compass-outline', size=40)} {dest_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"*{dest['highlight']}*")
    st.markdown("---")

    st.markdown(f"<h3>{iconify('mdi:camera-burst')} Galeri Visual</h3>", unsafe_allow_html=True)
    
    gallery = dest["high_res_gallery"]
    num_photos = len(gallery)
    current_idx = st.session_state.gallery_index

    col_img_fixed, col_nav_gal = st.columns([3, 1])
    
    with col_img_fixed:
        tampilkan_gambar_rapi(gallery[current_idx], target_width=1000, target_height=562) 
        st.write(f"<p style='text-align:center; color:gray;'>Foto {current_idx+1} dari {num_photos}</p>", unsafe_allow_html=True)
        
    with col_nav_gal:
        st.write("<br><br><br>", unsafe_allow_html=True)
        if st.button("⬅️ Sebelumnya", use_container_width=True) and current_idx > 0:
            st.session_state.gallery_index -= 1
            st.rerun()
        if st.button("Selanjutnya ➡️", use_container_width=True) and current_idx < (num_photos - 1):
            st.session_state.gallery_index += 1
            st.rerun()

    st.markdown("---")
    st.markdown(f"<h3>{iconify('mdi:text-box-outline')} Tentang Destinasi</h3>", unsafe_allow_html=True)
    st.write(dest["deskripsi_lengkap"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.video(dest["video_url"])

    st.markdown("---")
    st.markdown(f"<h3>{iconify('mdi:calculator-variant-outline')} Kalkulator Tiket & Wisata</h3>", unsafe_allow_html=True)
    
    col_calc_input, col_calc_res = st.columns([1, 1])
    with col_calc_input:
        with st.container(border=True):
            jumlah_orang = st.number_input("Jumlah Rombongan (Orang):", min_value=1, value=2)
            jumlah_hari = st.number_input("Lama Berwisata (Hari):", min_value=1, value=3)
            
    with col_calc_res:
        with st.container(border=True):
            total_biaya = (jumlah_orang * dest['tiket_masuk_orang']) * jumlah_hari
            st.markdown("Estimasi Total Biaya Dasar:")
            st.markdown(f"<h2 class='harga-text'>Rp {total_biaya:,.0f}</h2>", unsafe_allow_html=True)
            st.caption(f"*Asumsi tiket wisata rata-rata: Rp {dest['tiket_masuk_orang']:,}/orang/hari")

# --- ROUTING APLIKASI UTAMA ---
def render_page_flow():
    st.sidebar.markdown(f"<h2>{iconify('mdi:account-circle', color='white', size=30)} {st.session_state.username}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu Navigasi", 
        ["🏠 Dashboard", "🎬 Cinematic", "👤 Profil"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.favorit = [] # Reset favorit saat logout
        st.session_state.current_page = "main"
        st.rerun()

    if menu == "🏠 Dashboard":
        if st.session_state.current_page == "main":
            render_dashboard_utama()
        elif st.session_state.current_page == "detail":
            render_halaman_detail(st.session_state.selected_destination)
            
    elif menu == "🎬 Cinematic":
        st.title("🎬 Galeri Video")
        for nama, info in DESTINASI.items():
            st.subheader(nama)
            st.video(info["video_url"])
            
    elif menu == "👤 Profil":
        st.markdown(f"<h1>{iconify('mdi:card-account-details-outline', size=40)} Profil & Preferensi</h1>", unsafe_allow_html=True)
        st.write(f"Selamat datang di panel kontrol Anda, **{st.session_state.username}**!")
        st.markdown("---")
        
        # Layout terbagi: Kiri untuk Favorit, Kanan untuk Fitur Baru
        col_fav, col_fitur = st.columns([1.5, 1])
        
        with col_fav:
            st.markdown(f"<h3>{iconify('mdi:heart', color='#ff4b4b')} Destinasi Favorit</h3>", unsafe_allow_html=True)
            if not st.session_state.favorit:
                st.info("Anda belum memiliki destinasi favorit. Yuk cari di Dashboard!")
            else:
                for fav in st.session_state.favorit:
                    if fav in DESTINASI:
                        info = DESTINASI[fav]
                        with st.container(border=True):
                            c_img, c_txt = st.columns([1, 2.5])
                            with c_img:
                                tampilkan_gambar_rapi(info["cover_img"], target_width=300, target_height=200)
                            with c_txt:
                                st.markdown(f"<h4>{fav}</h4>", unsafe_allow_html=True)
                                st.markdown(f"<p class='harga-kecil'>{info['estimasi_biaya_katalog']}</p>", unsafe_allow_html=True)
                                st.write("") # spacer
                                if st.button(f"❌ Hapus dari Favorit", key=f"del_{fav}"):
                                    st.session_state.favorit.remove(fav)
                                    st.rerun()
                                    
        with col_fitur:
            # FITUR BARU: KALKULATOR TABUNGAN
            st.markdown(f"<h3>{iconify('mdi:piggy-bank', color='#ffb6c1')} Planner Tabungan</h3>", unsafe_allow_html=True)
            with st.container(border=True):
                st.write("Mulai rencanakan tabungan untuk mewujudkan liburan ke destinasi impian Anda.")
                
                if st.session_state.favorit:
                    target_dest = st.selectbox("Pilih Target Destinasi:", st.session_state.favorit)
                    if target_dest in DESTINASI:
                        target_budget = DESTINASI[target_dest]["biaya_dasar_int"]
                        
                        st.markdown(f"**Target Dana (Estimasi):**<br><span style='font-size: 18px; color:#2e8b57; font-weight:bold;'>Rp {target_budget:,.0f}</span>", unsafe_allow_html=True)
                        
                        bulan = st.slider("Target Berangkat (Bulan):", min_value=1, max_value=24, value=6)
                        tabungan_per_bulan = target_budget / bulan
                        
                        st.success(f"Anda perlu menabung:\n\n**Rp {tabungan_per_bulan:,.0f} / bulan**")
                else:
                    st.warning("Tambahkan minimal 1 destinasi ke Favorit terlebih dahulu untuk menggunakan fitur ini.")

if not st.session_state.logged_in:
    halaman_login()
else:
    render_page_flow()
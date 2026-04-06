import streamlit as st
from PIL import Image, ImageOps
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TripAja Agency - Eksplorasi Indonesia", page_icon="✈️", layout="wide")

# --- SUNTIKAN CSS CUSTOM ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .harga-text { color: #2e8b57; font-size: 20px; font-weight: bold; }
    .harga-kecil { color: #2e8b57; font-size: 16px; font-weight: bold; margin-bottom: 0px;}
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; padding: 10px 16px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI BANTUAN ICONIFY ---
def iconify(icon_name, color="#333", size=24):
    return f'<img src="https://api.iconify.design/{icon_name}.svg?color={color.replace("#", "%23")}" width="{size}" height="{size}" style="vertical-align: middle; margin-right: 8px;">'

# --- DATABASE DESTINASI (DITAMBAH 3 WILAYAH & DATA ITINERARY) ---
DESTINASI = {
    "Bali": {
        "highlight": "Pulau Dewata, menawarkan perpaduan sempurna pantai eksotis, pura kuno yang mistis, budaya kental, dan kehidupan malam modern.",
        "deskripsi_lengkap": "Bali tidak pernah gagal memukau. Kunjungi Pura Uluwatu di tebing, saksikan Tari Kecak, atau jelajahi Teras Sawah Tegalalang. Bagi pecinta pantai, Nusa Penida menawarkan tebing Kelingking yang ikonik. Nikmati juga kuliner lezat khas Bali.",
        "cover_img": "assets/bali.jpg",
        "high_res_gallery": ["assets/bali1.jpg", "assets/bali2.jpg", "assets/bali3.jpg"],
        "estimasi_biaya_katalog": "Rp 3.500.000 / org",
        "biaya_dasar_int": 3500000, 
        "tiket_masuk_orang": 75000,
        "video_url": "https://youtu.be/sY6BGVE-PBE",
        "itinerary": [
            "Hari 1: Tiba di Ngurah Rai, Check-in Hotel, Sunset di Pantai Kuta & Makan Malam Seafood di Jimbaran.",
            "Hari 2: Eksplorasi Ubud (Monkey Forest, Tegalalang), Kunjungan ke Pura Tirta Empul.",
            "Hari 3: Perjalanan ke Nusa Penida (Kelingking Beach, Broken Beach), Kembali ke Bali & Belanja Oleh-oleh."
        ]
    },
    "Yogyakarta": {
        "highlight": "Pusat budaya Jawa dengan kemegahan sejarah Candi Borobudur, kehangatan Malioboro, dan kuliner legendaris.",
        "deskripsi_lengkap": "Eksplorasi Malioboro dengan andong, kunjungi Keraton Yogyakarta, dan saksikan matahari terbit di Candi Borobudur. Jangan lewatkan petualangan Goa Jomblang atau keindahan Gumuk Pasir Parangkusumo.",
        "cover_img": "assets/jogja.jpg",
        "high_res_gallery": ["assets/jogja1.jpg", "assets/jogja2.jpg", "assets/jogja3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.500.000 / org",
        "biaya_dasar_int": 1500000,
        "tiket_masuk_orang": 50000,
        "video_url": "https://youtu.be/0Fi4JeizyZg",
        "itinerary": [
            "Hari 1: Tiba di Stasiun/Bandara, Makan Gudeg Mbah Lindu, Jalan-jalan santai & Belanja di Malioboro.",
            "Hari 2: Sunrise di Candi Borobudur, Wisata VW Safari Magelang, Sore di Candi Prambanan.",
            "Hari 3: Kunjungan ke Keraton Yogyakarta & Tamansari, Beli Bakpia Pathok, Pulang."
        ]
    },
    "Lombok": {
        "highlight": "Keindahan alam yang menenangkan, dengan Gunung Rinjani yang megah, tiga Gili mempesona, dan Sirkuit Mandalika.",
        "deskripsi_lengkap": "Gili Trawangan untuk bersantai dan snorkeling, menikmati pemandangan bawah laut. Jelajahi juga Pantai Pink yang unik atau kunjungi Desa Adat Sade untuk belajar budaya Sasak asli.",
        "cover_img": "assets/lombok.jpg",
        "high_res_gallery": ["assets/lombok1.jpg", "assets/lombok2.jpg", "assets/lombok3.jpg"],
        "estimasi_biaya_katalog": "Rp 2.800.000 / org",
        "biaya_dasar_int": 2800000,
        "tiket_masuk_orang": 40000,
        "video_url": "https://youtu.be/379EEoRIbIs",
        "itinerary": [
            "Hari 1: Tiba di Bandara, Eksplorasi Sirkuit Mandalika & Bukit Merese, Check-in Hotel.",
            "Hari 2: Penyeberangan ke Gili Trawangan, Snorkeling Trip (Patung Bawah Laut), Bersepeda keliling pulau.",
            "Hari 3: Kunjungan ke Desa Adat Sade, Belanja Mutiara & Tenun Lombok, Persiapan Pulang."
        ]
    },
    "Bandung": {
        "highlight": "Kota Kembang dengan udara sejuk, surga belanja, kuliner estetik, dan wisata alam pegunungan yang asri.",
        "deskripsi_lengkap": "Kunjungi Kawah Putih yang memukau dengan danau vulkanik sulfurnya, Tangkuban Perahu, atau bersantai di Ranca Upas berinteraksi dengan rusa. Nikmati suasana sejuk Lembang dan berbagai kafe estetik di kawasan bersejarah Braga.",
        "cover_img": "assets/bandung.jpg",
        "high_res_gallery": ["assets/bandung1.jpg", "assets/bandung2.jpg", "assets/bandung3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.200.000 / org",
        "biaya_dasar_int": 1200000,
        "tiket_masuk_orang": 35000,
        "video_url": "https://youtu.be/dummy_bandung", 
        "itinerary": [
            "Hari 1: Tiba di Bandung, Wisata sejarah & ngopi di Jalan Braga, Makan malam di Puncak Ciumbuleuit (Punclut).",
            "Hari 2: Eksplorasi Lembang (Farmhouse / Floating Market), Interaksi dengan Rusa di Ranca Upas.",
            "Hari 3: Wisata Kawah Putih Ciwidey, Belanja di Cibaduyut / Factory Outlet, Kembali ke kota asal."
        ]
    },
    "Surabaya": {
        "highlight": "Kota Pahlawan yang kaya nilai sejarah, tata kota modern, taman-taman asri, dan aneka kuliner khas Jawa Timur yang pedas & gurih.",
        "deskripsi_lengkap": "Jelajahi ikon Jembatan Suramadu yang menghubungkan Jawa dan Madura, Monumen Kapal Selam, dan kawasan bersejarah Tugu Pahlawan. Jangan lupa mencicipi Rawon Kalkulator, Rujak Cingur, dan Sate Kelopo yang legendaris.",
        "cover_img": "assets/surabaya.jpg",
        "high_res_gallery": ["assets/surabaya1.jpg", "assets/surabaya2.jpg", "assets/surabaya3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.400.000 / org",
        "biaya_dasar_int": 1400000,
        "tiket_masuk_orang": 25000,
        "video_url": "https://youtu.be/dummy_surabaya",
        "itinerary": [
            "Hari 1: Tiba di Surabaya, Kunjungan ke Tugu Pahlawan & Museum 10 Nopember, Makan Siang Rujak Cingur.",
            "Hari 2: Menjelajahi Monumen Kapal Selam (Monkasel), Santai di Taman Bungkul, Perjalanan malam melewati Jembatan Suramadu.",
            "Hari 3: Beli oleh-oleh Spikoe Resep Kuno & Sambal Bu Rudy, Kuliner Lontong Balap, Pulang."
        ]
    },
    "Papua": {
        "highlight": "Surga bahari Raja Ampat di ujung timur Indonesia dengan gugusan pulau karang karst mempesona dan keanekaragaman hayati bawah laut kelas dunia.",
        "deskripsi_lengkap": "Raja Ampat adalah impian setiap penyelam. Gugusan kepulauan Piaynemo dan Wayag menawarkan pemandangan dari atas bukit yang menakjubkan. Lakukan diving atau snorkeling untuk bertemu pari manta, hiu karang, dan terumbu karang yang masih sangat alami dan tak tersentuh.",
        "cover_img": "assets/papua.jpg",
        "high_res_gallery": ["assets/papua1.jpg", "assets/papua2.jpg", "assets/papua3.jpg"],
        "estimasi_biaya_katalog": "Rp 8.500.000 / org",
        "biaya_dasar_int": 8500000,
        "tiket_masuk_orang": 250000,
        "video_url": "https://youtu.be/dummy_papua",
        "itinerary": [
            "Hari 1: Tiba di Sorong, Penyeberangan Kapal Feri ke Waisai (Raja Ampat), Check-in Resort/Homestay pinggir pantai.",
            "Hari 2: Trekking ke Puncak Piaynemo yang ikonik, Snorkeling di Arborek Village.",
            "Hari 3: Berenang bersama ikan Pari Manta di Manta Point, Menikmati sunset, Persiapan kembali ke Sorong."
        ]
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
        # Menampilkan placeholder warna abu-abu jika gambar belum dimasukkan pengguna
        st.markdown(f"<div style='width:100%; height:200px; background-color:#e0e0e0; border-radius:10px; display:flex; align-items:center; justify-content:center;'>📸 {path_gambar} (Belum Ditambahkan)</div>", unsafe_allow_html=True)

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
    search_query = st.text_input("🔍 Cari referensi wilayah (Contoh: Bali, Lombok, Bandung)...")
    st.markdown("---")
    
    hasil = {k: v for k, v in DESTINASI.items() if search_query.lower() in k.lower()} if search_query else DESTINASI
    
    # Layout Grid (2 kolom) untuk Dashboard agar memuat lebih banyak destinasi
    col_kiri, col_kanan = st.columns(2)
    
    for i, (nama, info) in enumerate(hasil.items()):
        with (col_kiri if i % 2 == 0 else col_kanan):
            with st.container(border=True):
                tampilkan_gambar_rapi(info["cover_img"], target_width=600, target_height=350)
                st.markdown(f"<h3>{iconify('mdi:map-marker', color='#ff4b4b', size=28)} {nama}</h3>", unsafe_allow_html=True)
                st.write(f"{info['highlight']}")
                st.markdown(f"<p class='harga-text'>{iconify('mdi:wallet', color='#2e8b57')} Mulai dari {info['estimasi_biaya_katalog']}</p>", unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
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
                        if st.button(f"🤍 Simpan", key=f"fav_{nama}", use_container_width=True):
                            st.session_state.favorit.append(nama)
                            st.rerun()
                st.write("") # Spacer bawah kartu

# --- HALAMAN DETAIL DESTINASI (DENGAN TABS) ---
def render_halaman_detail(dest_name):
    dest = DESTINASI[dest_name]

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.current_page = "main"
        st.rerun()
    
    st.markdown(f"<h1>{iconify('mdi:compass-outline', size=40)} {dest_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"*{dest['highlight']}*")
    st.markdown("---")

    # FITUR BARU: SISTEM TABS
    tab_overview, tab_galeri, tab_itinerary, tab_kalkulator = st.tabs([
        f"📝 Overview", 
        f"📸 Galeri Visual", 
        f"🗺️ Rencana Perjalanan", 
        f"🧮 Kalkulator Wisata"
    ])

    # TAB 1: OVERVIEW
    with tab_overview:
        st.markdown(f"<h3>Tentang Destinasi</h3>", unsafe_allow_html=True)
        st.write(dest["deskripsi_lengkap"])
        st.markdown("<br>", unsafe_allow_html=True)
        st.video(dest["video_url"])

    # TAB 2: GALERI
    with tab_galeri:
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

    # TAB 3: FITUR ITINERARY & CHECKLIST
    with tab_itinerary:
        st.markdown(f"<h3>Rekomendasi Rencana Perjalanan (3 Hari)</h3>", unsafe_allow_html=True)
        for i, aktivitas in enumerate(dest["itinerary"]):
            with st.expander(f"✨ Aktivitas {aktivitas.split(':')[0]}", expanded=True):
                st.write(aktivitas.split(':')[1])
                
        st.markdown("---")
        st.markdown(f"<h3>{iconify('mdi:check-all')} Checklist Bawaan Wajib</h3>", unsafe_allow_html=True)
        st.checkbox("Pakaian Nyaman & Jaket (Sesuai cuaca)")
        st.checkbox("Obat-obatan Pribadi")
        st.checkbox("Kamera / Powerbank")
        st.checkbox("Uang Tunai Cukup")

    # TAB 4: KALKULATOR
    with tab_kalkulator:
        st.markdown("Fitur ini membantu Anda menghitung **estimasi biaya dasar** (tiket masuk rata-rata wisata utama) di destinasi ini sebelum berangkat.")
        col_calc_input, col_calc_res = st.columns([1, 1])
        with col_calc_input:
            with st.container(border=True):
                jumlah_orang = st.number_input("Jumlah Rombongan (Orang):", min_value=1, value=2)
                jumlah_hari = st.number_input("Lama Berwisata (Hari):", min_value=1, value=3)
                
        with col_calc_res:
            with st.container(border=True):
                total_biaya = (jumlah_orang * dest['tiket_masuk_orang']) * jumlah_hari
                st.markdown("Estimasi Total Biaya Tiket Dasar:")
                st.markdown(f"<h2 class='harga-text'>Rp {total_biaya:,.0f}</h2>", unsafe_allow_html=True)
                st.caption(f"*Asumsi tiket wisata rata-rata: Rp {dest['tiket_masuk_orang']:,}/orang/hari. (Belum termasuk tiket pesawat/hotel).")

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
        st.session_state.favorit = [] 
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
                                st.write("") 
                                if st.button(f"❌ Hapus dari Favorit", key=f"del_{fav}"):
                                    st.session_state.favorit.remove(fav)
                                    st.rerun()
                                    
        with col_fitur:
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
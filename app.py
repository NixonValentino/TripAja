import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image, ImageOps
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TripAja Agency - Eksplorasi Indonesia", page_icon="✈️", layout="wide")

# --- SUNTIKAN CSS CUSTOM ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    .harga-text { color: #2e8b57; font-size: 22px; font-weight: 800; }
    .harga-kecil { color: #2e8b57; font-size: 16px; font-weight: bold; margin-bottom: 0px;}
    div[data-testid="stTabs"] button {
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }
    /* Hover effect untuk widget cuaca biru */
    .widget-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .widget-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI BANTUAN ICONIFY ---
def iconify(icon_name, color="#333", size=24):
    return f'<img src="https://api.iconify.design/{icon_name}.svg?color={color.replace("#", "%23")}" width="{size}" height="{size}" style="vertical-align: middle; margin-right: 6px;">'

# --- DATABASE DESTINASI ---
DESTINASI = {
    "Bali": {
        "highlight": "Pulau Dewata, menawarkan perpaduan sempurna antara pantai-pantai eksotis dengan pasir putih dan ombak memikat, deretan pura kuno yang sarat nuansa mistis dan spiritual, serta budaya lokal yang masih sangat kental dan terjaga hingga kini. Tidak hanya itu, Bali juga menghadirkan kehidupan malam modern yang semarak, lengkap dengan beach club, kafe estetik, hingga hiburan kelas dunia.",
        "deskripsi_lengkap": "Bali tidak pernah gagal memukau. Kunjungi Pura Uluwatu di tebing, saksikan Tari Kecak, atau jelajahi Teras Sawah Tegalalang. Bagi pecinta pantai, Nusa Penida menawarkan tebing Kelingking yang ikonik. Nikmati juga kuliner lezat khas Bali.",
        "cover_img": "assets/bali.jpg",
        "high_res_gallery": ["assets/bali1.jpg", "assets/bali2.jpg", "assets/bali3.jpg"],
        "estimasi_biaya_katalog": "Rp 3.500.000 / org",
        "biaya_dasar_int": 3500000, 
        "tiket_masuk_orang": 75000,
        "video_url": "https://www.youtube.com/watch?v=sY6BGVE-PBE",
        "itinerary": [
            "Hari 1: Tiba di Ngurah Rai, Check-in Hotel, Sunset di Pantai Kuta & Makan Malam Seafood di Jimbaran.",
            "Hari 2: Eksplorasi Ubud (Monkey Forest, Tegalalang), Kunjungan ke Pura Tirta Empul.",
            "Hari 3: Perjalanan ke Nusa Penida (Kelingking Beach, Broken Beach), Kembali ke Bali & Belanja Oleh-oleh."
        ],
        "koordinat": {"lat": -8.409518, "lon": 115.188919},
        "waktu_terbaik": "April - Oktober",
        "cuaca": "Tropis Cerah, 27°C - 30°C",
        "cuaca_ikon": "fluent:weather-sunny-28-filled"
    },
    "Yogyakarta": {
        "highlight": "Pusat budaya Jawa yang kaya akan nilai sejarah, seni, dan tradisi yang masih hidup dalam keseharian masyarakatnya. Yogyakarta menghadirkan pesona kemegahan Candi Borobudur yang mendunia, kehangatan suasana Malioboro yang selalu ramai dan penuh cerita, serta ragam kuliner legendaris seperti gudeg yang menggugah selera. Selain itu, kota ini juga menawarkan pengalaman autentik melalui keraton, pertunjukan seni.",
        "deskripsi_lengkap": "Eksplorasi Malioboro dengan andong, kunjungi Keraton Yogyakarta, dan saksikan matahari terbit di Candi Borobudur. Jangan lewatkan petualangan Goa Jomblang atau keindahan Gumuk Pasir Parangkusumo.",
        "cover_img": "assets/jogja.jpg",
        "high_res_gallery": ["assets/jogja1.jpg", "assets/jogja2.jpg", "assets/jogja3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.500.000 / org",
        "biaya_dasar_int": 1500000,
        "tiket_masuk_orang": 50000,
        "video_url": "https://youtu.be/0Fi4JeizyZg?si=Mx-TqQ5QwUbWdkOB",
        "itinerary": [
            "Hari 1: Tiba di Stasiun/Bandara, Makan Gudeg Mbah Lindu, Jalan-jalan santai & Belanja di Malioboro.",
            "Hari 2: Sunrise di Candi Borobudur, Wisata VW Safari Magelang, Sore di Candi Prambanan.",
            "Hari 3: Kunjungan ke Keraton Yogyakarta & Tamansari, Beli Bakpia Pathok, Pulang."
        ],
        "koordinat": {"lat": -7.795580, "lon": 110.369490},
        "waktu_terbaik": "Mei - September",
        "cuaca": "Hangat Berawan, 26°C - 32°C",
        "cuaca_ikon": "fluent:weather-partly-cloudy-day-48-filled"
    },
    "Lombok": {
        "highlight": "Keindahan alam yang menenangkan dengan suasana yang masih relatif lebih tenang dibandingkan destinasi populer lainnya. Pulau ini menghadirkan kemegahan Gunung Rinjani yang menjadi favorit para pendaki, lengkap dengan panorama danau Segara Anak yang memukau. Selain itu, pesona tiga Gili—Gili Trawangan, Gili Meno, dan Gili Air—menawarkan air laut jernih, pasir putih, dan suasana tropis yang sempurna untuk relaksasi.",
        "deskripsi_lengkap": "Gili Trawangan untuk bersantai dan snorkeling, menikmati pemandangan bawah laut. Jelajahi juga Pantai Pink yang unik atau kunjungi Desa Adat Sade untuk belajar budaya Sasak asli.",
        "cover_img": "assets/lombok.jpg",
        "high_res_gallery": ["assets/lombok1.jpg", "assets/lombok2.jpg", "assets/lombok3.jpg"],
        "estimasi_biaya_katalog": "Rp 2.800.000 / org",
        "biaya_dasar_int": 2800000,
        "tiket_masuk_orang": 40000,
        "video_url": "https://www.youtube.com/watch?v=379EEoRIbIs",
        "itinerary": [
            "Hari 1: Tiba di Bandara, Eksplorasi Sirkuit Mandalika & Bukit Merese, Check-in Hotel.",
            "Hari 2: Penyeberangan ke Gili Trawangan, Snorkeling Trip (Patung Bawah Laut), Bersepeda keliling pulau.",
            "Hari 3: Kunjungan ke Desa Adat Sade, Belanja Mutiara & Tenun Lombok, Persiapan Pulang."
        ],
        "koordinat": {"lat": -8.583333, "lon": 116.116667},
        "waktu_terbaik": "Juli - Agustus",
        "cuaca": "Tropis Cerah, 25°C - 31°C",
        "cuaca_ikon": "fluent:weather-sunny-28-filled"
    },
    "Bandung": {
        "highlight": "Kota Kembang yang dikenal dengan udara sejuk khas pegunungan dan suasana yang nyaman untuk berlibur. Bandung merupakan surga belanja dengan berbagai factory outlet dan distro kreatif, sekaligus destinasi kuliner estetik yang terus berkembang mengikuti tren anak muda. Keindahan alamnya pun tak kalah memikat, mulai dari kawasan Lembang yang asri hingga panorama kawah di Kawah Putih yang eksotis.",
        "deskripsi_lengkap": "Kunjungi Kawah Putih yang memukau dengan danau vulkanik sulfurnya, Tangkuban Perahu, atau bersantai di Ranca Upas berinteraksi dengan rusa. Nikmati suasana sejuk Lembang dan berbagai kafe estetik di kawasan bersejarah Braga.",
        "cover_img": "assets/bandung.jpg",
        "high_res_gallery": ["assets/bandung1.jpg", "assets/bandung2.jpg", "assets/bandung3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.200.000 / org",
        "biaya_dasar_int": 1200000,
        "tiket_masuk_orang": 35000,
        "video_url": "https://youtu.be/2JW5B6xLAEA?si=tNfC39RxkOEDTAcC",
        "itinerary": [
            "Hari 1: Tiba di Bandung, Wisata sejarah & ngopi di Jalan Braga, Makan malam di Puncak Ciumbuleuit (Punclut).",
            "Hari 2: Eksplorasi Lembang (Farmhouse / Floating Market), Interaksi dengan Rusa di Ranca Upas.",
            "Hari 3: Wisata Kawah Putih Ciwidey, Belanja di Cibaduyut / Factory Outlet, Kembali ke kota asal."
        ],
        "koordinat": {"lat": -6.917464, "lon": 107.619123},
        "waktu_terbaik": "Sepanjang Tahun",
        "cuaca": "Sejuk Pegunungan, 20°C - 26°C",
        "cuaca_ikon": "fluent:weather-rain-showers-day-24-filled"
    },
    "Surabaya": {
        "highlight": "Kota Pahlawan yang sarat akan nilai sejarah perjuangan bangsa, sekaligus berkembang menjadi kota metropolitan dengan tata kota yang modern dan tertata rapi. Ikon bersejarah seperti Tugu Pahlawan menjadi simbol semangat perjuangan, sementara ruang publik seperti Taman Bungkul menghadirkan suasana hijau yang nyaman di tengah hiruk-pikuk kota. Surabaya juga dikenal dengan ragam kuliner khas Jawa Timur yang kaya rasa",
        "deskripsi_lengkap": "Jelajahi ikon Jembatan Suramadu yang menghubungkan Jawa dan Madura, Monumen Kapal Selam, dan kawasan bersejarah Tugu Pahlawan. Jangan lupa mencicipi Rawon Kalkulator, Rujak Cingur, dan Sate Kelopo yang legendaris.",
        "cover_img": "assets/surabaya.jpg",
        "high_res_gallery": ["assets/surabaya1.jpg", "assets/surabaya2.jpg", "assets/surabaya3.jpg"],
        "estimasi_biaya_katalog": "Rp 1.400.000 / org",
        "biaya_dasar_int": 1400000,
        "tiket_masuk_orang": 25000,
        "video_url": "https://youtu.be/h2MZNZuvcLU?si=t1ogHu0MSprBFxcq",
        "itinerary": [
            "Hari 1: Tiba di Surabaya, Kunjungan ke Tugu Pahlawan & Museum 10 Nopember, Makan Siang Rujak Cingur.",
            "Hari 2: Menjelajahi Monumen Kapal Selam (Monkasel), Santai di Taman Bungkul, Perjalanan malam melewati Jembatan Suramadu.",
            "Hari 3: Beli oleh-oleh Spikoe Resep Kuno & Sambal Bu Rudy, Kuliner Lontong Balap, Pulang."
        ],
        "koordinat": {"lat": -7.250445, "lon": 112.768845},
        "waktu_terbaik": "Mei - November",
        "cuaca": "Panas & Terik, 28°C - 34°C",
        "cuaca_ikon": "fluent:weather-sunny-high-24-filled"
    },
    "Papua": {
        "highlight": "Surga tersembunyi di ujung timur Indonesia yang menawarkan keindahan alam luar biasa dan masih sangat alami. Kawasan Raja Ampat menjadi ikon wisata bahari dunia dengan gugusan pulau karst yang dramatis, air laut sebening kristal, serta keanekaragaman hayati bawah laut yang termasuk terkaya di planet ini. Tidak hanya itu, Papua juga menyimpan kekayaan budaya lokal yang unik dan autentik",
        "deskripsi_lengkap": "Raja Ampat adalah impian setiap penyelam. Gugusan kepulauan Piaynemo dan Wayag menawarkan pemandangan dari atas bukit yang menakjubkan. Lakukan diving atau snorkeling untuk bertemu pari manta, hiu karang, dan terumbu karang yang masih sangat alami dan tak tersentuh.",
        "cover_img": "assets/papua.jpg",
        "high_res_gallery": ["assets/papua1.jpg", "assets/papua2.jpg", "assets/papua3.jpg"],
        "estimasi_biaya_katalog": "Rp 8.500.000 / org",
        "biaya_dasar_int": 8500000,
        "tiket_masuk_orang": 250000,
        "video_url": "https://youtu.be/E8P8CW-fHy0?si=4NdjnPwnYsjeOmZa",
        "itinerary": [
            "Hari 1: Tiba di Sorong, Penyeberangan Kapal Feri ke Waisai (Raja Ampat), Check-in Resort/Homestay pinggir pantai.",
            "Hari 2: Trekking ke Puncak Piaynemo yang ikonik, Snorkeling di Arborek Village.",
            "Hari 3: Berenang bersama ikan Pari Manta di Manta Point, Menikmati sunset, Persiapan kembali ke Sorong."
        ],
        "koordinat": {"lat": -0.233333, "lon": 130.516667},
        "waktu_terbaik": "Okt - April (Diving)",
        "cuaca": "Tropis Lembab, 26°C - 31°C",
        "cuaca_ikon": "fluent:weather-partly-cloudy-day-48-filled"
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
        st.markdown(f"<div style='width:100%; height:200px; background-color:#e0e0e0; border-radius:10px; display:flex; align-items:center; justify-content:center; color: gray;'>📸 {path_gambar} (Belum Ditambahkan)</div>", unsafe_allow_html=True)

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
    st.markdown(f"<h1>{iconify('mdi:compass-rose', size=36)} Eksplorasi Indonesia</h1>", unsafe_allow_html=True)
    st.markdown("Temukan referensi perjalanan terbaik dan rencanakan impian liburan Anda bersama TripAja.")
    
    st.session_state.selected_destination = None
    search_query = st.text_input("🔍 Cari referensi wilayah (Contoh: Bali, Lombok, Bandung)...")
    st.markdown("---")
    
    hasil = {k: v for k, v in DESTINASI.items() if search_query.lower() in k.lower()} if search_query else DESTINASI
    
    col_kiri, col_kanan = st.columns(2)
    
    for i, (nama, info) in enumerate(hasil.items()):
        with (col_kiri if i % 2 == 0 else col_kanan):
            with st.container(border=True):
                tampilkan_gambar_rapi(info["cover_img"], target_width=600, target_height=350)
                st.markdown(f"<h3>{iconify('mdi:map-marker', color='#ff4b4b', size=28)} {nama}</h3>", unsafe_allow_html=True)
                st.write(f"{info['highlight']}")
                st.markdown(f"<p class='harga-text'>{iconify('mdi:wallet', color='#2e8b57', size=26)} Mulai dari {info['estimasi_biaya_katalog']}</p>", unsafe_allow_html=True)
                
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
                st.write("") 

# --- HALAMAN DETAIL DESTINASI ---
def render_halaman_detail(dest_name):
    dest = DESTINASI[dest_name]

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.current_page = "main"
        st.rerun()
    
    st.markdown(f"<h1>{iconify('mdi:map-legend', size=40)} {dest_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"*{dest['highlight']}*")
    st.markdown("---")

    tab_overview, tab_galeri, tab_peta, tab_itinerary, tab_kalkulator, tab_ulasan = st.tabs([
        f"📝 Overview", 
        f"📸 Galeri Visual", 
        f"🗺️ Peta Lokasi",
        f"🧭 Itinerary", 
        f"🧮 Kalkulator",
        f"⭐ Ulasan"
    ])

    with tab_overview:
        st.markdown(f"<h3>{iconify('mdi:information-outline', size=28)} Tentang Destinasi</h3>", unsafe_allow_html=True)
        st.write(dest["deskripsi_lengkap"])
        st.write("<br>", unsafe_allow_html=True)
        
        # --- UI/UX WIDGET CUACA & WAKTU (DIPERTAHANKAN WARNA BIRUNYA) ---
        col_cuaca, col_waktu = st.columns(2)
        
        with col_cuaca:
            st.markdown(f"""
            <div class="widget-card" style="background: linear-gradient(135deg, #2b70e4 0%, #5a9bf5 100%); padding: 20px; border-radius: 12px; color: white; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <div style="flex: 1;">
                    <p style="margin:0; font-size: 13px; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">Live Cuaca & Suhu</p>
                    <h3 style="margin: 5px 0 0 0; color: white; font-size: 22px;">{dest['cuaca']}</h3>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 50%;">
                    {iconify(dest['cuaca_ikon'], color='white', size=40)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_waktu:
            st.markdown(f"""
            <div class="widget-card" style="background: linear-gradient(135deg, #1f5bbd 0%, #4686e6 100%); padding: 20px; border-radius: 12px; color: white; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <div style="flex: 1;">
                    <p style="margin:0; font-size: 13px; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">Waktu Berkunjung Ideal</p>
                    <h3 style="margin: 5px 0 0 0; color: white; font-size: 22px;">{dest['waktu_terbaik']}</h3>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 50%;">
                    {iconify('mdi:calendar-check', color='white', size=40)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.video(dest["video_url"])

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

    with tab_peta:
        st.markdown(f"<h3>{iconify('mdi:google-maps', color='#4285F4', size=28)} Peta Google Maps: {dest_name}</h3>", unsafe_allow_html=True)
        st.markdown("Jelajahi area sekitar, cari restoran terdekat, atau lihat review tempat wisata langsung dari peta ini.")
        
        lat = dest["koordinat"]["lat"]
        lon = dest["koordinat"]["lon"]
        map_html = f'''
            <iframe 
                width="100%" 
                height="450" 
                frameborder="0" 
                scrolling="no" 
                marginheight="0" 
                marginwidth="0" 
                src="https://maps.google.com/maps?q={lat},{lon}&t=&z=12&ie=UTF8&iwloc=&output=embed"
                style="border-radius: 10px; border: 2px solid #e0e0e0;"
            ></iframe>
        '''
        components.html(map_html, height=450)

    with tab_itinerary:
        st.markdown(f"<h3>{iconify('mdi:clipboard-text-clock', size=28)} Rekomendasi Rencana Perjalanan (3 Hari)</h3>", unsafe_allow_html=True)
        for i, aktivitas in enumerate(dest["itinerary"]):
            with st.expander(f"Hari ke-{i+1} : {aktivitas.split(':')[0].split(' ')[1]}", expanded=True):
                st.write(f"✨ {aktivitas.split(':')[1]}")
                
        st.markdown("---")
        st.markdown(f"<h3>{iconify('mdi:bag-checked', color='#ff8c00', size=28)} Checklist Bawaan Wajib</h3>", unsafe_allow_html=True)
        st.checkbox("Pakaian Nyaman & Jaket (Sesuai cuaca)")
        st.checkbox("Obat-obatan Pribadi")
        st.checkbox("Kamera / Powerbank")
        st.checkbox("Uang Tunai Cukup")

    with tab_kalkulator:
        st.markdown(f"<h3>{iconify('mdi:calculator-variant', size=28)} Kalkulator Biaya Wisata Dasar</h3>", unsafe_allow_html=True)
        st.markdown("Hitung estimasi biaya dasar tiket masuk berdasarkan jumlah rombongan Anda.")
        
        col_calc_input, col_calc_res = st.columns([1, 1.5])
        with col_calc_input:
            with st.container(border=True):
                jumlah_orang = st.number_input("Jumlah Rombongan (Orang):", min_value=1, value=2)
                jumlah_hari = st.number_input("Lama Berwisata (Hari):", min_value=1, value=3)
                
        with col_calc_res:
            with st.container(border=True):
                total_biaya_idr = (jumlah_orang * dest['tiket_masuk_orang']) * jumlah_hari
                
                konversi = st.radio("Tampilkan dalam mata uang:", ["IDR (Rupiah)", "USD (Dolar AS)", "EUR (Euro)"], horizontal=True)
                
                st.markdown("Estimasi Total Biaya Tiket Dasar:")
                if konversi == "IDR (Rupiah)":
                    st.markdown(f"<h2 class='harga-text'>Rp {total_biaya_idr:,.0f}</h2>", unsafe_allow_html=True)
                elif konversi == "USD (Dolar AS)":
                    usd = total_biaya_idr / 15500 
                    st.markdown(f"<h2 class='harga-text'>$ {usd:,.2f}</h2>", unsafe_allow_html=True)
                else:
                    eur = total_biaya_idr / 16800
                    st.markdown(f"<h2 class='harga-text'>€ {eur:,.2f}</h2>", unsafe_allow_html=True)
                    
                st.caption(f"*Asumsi tiket wisata rata-rata: Rp {dest['tiket_masuk_orang']:,}/orang/hari. (Belum termasuk akomodasi).")

    with tab_ulasan:
        st.markdown(f"<h3>{iconify('mdi:comment-star', color='#fbbc04', size=28)} Ulasan Pengunjung</h3>", unsafe_allow_html=True)
        
        kunci_ulasan = f"ulasan_db_{dest_name}"
        if kunci_ulasan not in st.session_state:
            st.session_state[kunci_ulasan] = [
                {"user": "TravelerSejati", "rating": 5, "komen": f"{dest_name} sangat luar biasa! Pemandangannya bikin betah, rekomen banget buat liburan keluarga."},
                {"user": "JalanJalanTerus", "rating": 4, "komen": "Overall bagus, tapi usahakan datang pagi hari supaya tidak terlalu ramai dan terik."}
            ]
            
        for u in st.session_state[kunci_ulasan]:
            with st.container(border=True):
                st.markdown(f"**{u['user']}** {'⭐' * u['rating']}")
                st.write(u['komen'])
                
        st.markdown("---")
        st.markdown("**Berikan Ulasan Anda**")
        
        with st.form(f"form_ulasan_{dest_name}"):
            rating_input = st.slider("Seberapa puas Anda dengan referensi destinasi ini?", 1, 5, 5)
            komen_input = st.text_area("Tuliskan komentar atau pertanyaan Anda...")
            submit_ulasan = st.form_submit_button("Kirim Ulasan")
            
            if submit_ulasan:
                if komen_input.strip() == "":
                    st.error("Komentar tidak boleh kosong!")
                else:
                    ulasan_baru = {
                        "user": f"{st.session_state.username} (Anda)",
                        "rating": rating_input,
                        "komen": komen_input
                    }
                    st.session_state[kunci_ulasan].insert(0, ulasan_baru)
                    st.success("Ulasan berhasil dikirim!")
                    st.rerun()

# --- ROUTING APLIKASI UTAMA ---
def render_page_flow():
    st.sidebar.markdown(f"<h2>{iconify('mdi:account-circle', size=30)} {st.session_state.username}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu Navigasi Utama", 
        ["🏠 Dashboard", "🎬 Galeri Cinematic", "👤 Profil & Preferensi"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Keluar / Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.favorit = [] 
        st.session_state.current_page = "main"
        st.rerun()

    # Konten Utama
    if menu == "🏠 Dashboard":
        if st.session_state.current_page == "main":
            render_dashboard_utama()
        elif st.session_state.current_page == "detail":
            render_halaman_detail(st.session_state.selected_destination)
            
    elif menu == "🎬 Galeri Cinematic":
        st.markdown(f"<h1>{iconify('mdi:movie-open-play', size=36)} Galeri Video Cinematic</h1>", unsafe_allow_html=True)
        st.write("Rasakan suasana destinasi impian Anda melalui kumpulan video cinematic.")
        st.markdown("---")
        
        col_vid1, col_vid2 = st.columns(2)
        for i, (nama, info) in enumerate(DESTINASI.items()):
            with (col_vid1 if i % 2 == 0 else col_vid2):
                st.markdown(f"<h4>{nama}</h4>", unsafe_allow_html=True)
                st.video(info["video_url"])
                st.write("")
            
    elif menu == "👤 Profil & Preferensi":
        st.markdown(f"<h1>{iconify('mdi:card-account-details', size=36)} Profil & Preferensi</h1>", unsafe_allow_html=True)
        st.write(f"Selamat datang di panel kontrol Anda, **{st.session_state.username}**!")
        st.markdown("---")
        
        col_fav, col_fitur = st.columns([1.5, 1])
        
        with col_fav:
            st.markdown(f"<h3>{iconify('mdi:heart', color='#ff4b4b', size=28)} Destinasi Favorit</h3>", unsafe_allow_html=True)
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
                                if st.button(f"❌ Hapus", key=f"del_{fav}"):
                                    st.session_state.favorit.remove(fav)
                                    st.rerun()
                                    
        with col_fitur:
            st.markdown(f"<h3>{iconify('mdi:piggy-bank', color='#ffb6c1', size=28)} Planner Tabungan</h3>", unsafe_allow_html=True)
            with st.container(border=True):
                st.write("Mulai rencanakan tabungan untuk mewujudkan liburan ke destinasi impian Anda.")
                
                if st.session_state.favorit:
                    target_dest = st.selectbox("Pilih Target Destinasi:", st.session_state.favorit)
                    if target_dest in DESTINASI:
                        target_budget = DESTINASI[target_dest]["biaya_dasar_int"]
                        st.markdown(f"**Target Dana:**<br><span class='harga-text'>Rp {target_budget:,.0f}</span>", unsafe_allow_html=True)
                        bulan = st.slider("Target Berangkat (Bulan):", min_value=1, max_value=24, value=6)
                        tabungan_per_bulan = target_budget / bulan
                        st.success(f"Anda perlu menabung:\n\n**Rp {tabungan_per_bulan:,.0f} / bulan**")
                else:
                    st.warning("Tambahkan minimal 1 destinasi ke Favorit terlebih dahulu.")

# --- ENTRY POINT UTAMA ---
if not st.session_state.logged_in:
    halaman_login()
else:
    render_page_flow()
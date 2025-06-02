# ✅ SMARTMOOD FINAL - GOOGLE COLAB (BERDASARKAN DATASET KAGGLE)

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta


DATA_FOLDER = "user_data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Skor aktivitas berdasarkan hasil analisis dari FitLife Kaggle Dataset (disederhanakan)
aktivitas_skor = {
    "Belajar": 5,
    "Ngerjain tugas": 6,
    "Proyekan": 7,
    "Dikejar deadline": 3,
    "Ikut kelas/zoom": 5,
    "Bertemu teman": 8,
    "Rapat organisasi": 6,
    "Nongkrong": 7,
    "Diam di kos": 3,
    "Chat panjang": 6,
    "Tidur cukup": 9,
    "Makan sehat": 7,
    "Olahraga": 8,
    "Begadang": 2,
    "Lupa makan": 1,
    "Scroll TikTok": 3,
    "Main game": 4,
    "Nonton film": 5,
    "Ngegalau": 2,
    "Tidak melakukan apa-apa": 1
}

kategori_aktivitas = {
    "Akademik": ["Belajar", "Ngerjain tugas", "Proyekan", "Dikejar deadline", "Ikut kelas/zoom"],
    "Sosial": ["Bertemu teman", "Rapat organisasi", "Nongkrong", "Diam di kos", "Chat panjang"],
    "Kesehatan": ["Tidur cukup", "Makan sehat", "Olahraga", "Begadang", "Lupa makan"],
    "Lainnya": ["Scroll TikTok", "Main game", "Nonton film", "Ngegalau", "Tidak melakukan apa-apa"]
}

saran_dict = {
    "😢 Sedih": "Sepertinya harimu berat. Coba tarik napas dalam, dengarkan musik tenang, dan beri dirimu ruang untuk istirahat.",
    "😐 Biasa": "Mungkin hari ini terasa datar, tapi kamu hebat karena tetap menjalani. Pelan-pelan saja, semua baik-baik aja.",
    "😊 Bahagia": "Wah, kamu lagi di atas angin! Simpan energi ini dan bagi kebahagiaanmu ke orang terdekat, yuk."
}

def classify_mood(score):
    if score < 10:
        mood = "😢 Sedih"
    elif score < 20:
        mood = "😐 Biasa"
    else:
        mood = "😊 Bahagia"
    return mood, saran_dict[mood]

def simpan_data(username, tanggal, aktivitas_data, rating, mood, saran, catatan):
    filename = f"{DATA_FOLDER}/data_{username}.csv"
    records = []
    for kategori, aktivitas in aktivitas_data.items():
        skor = aktivitas_skor.get(aktivitas, 0)
        records.append([tanggal, kategori, aktivitas, skor, rating, mood, saran, catatan])
    df_new = pd.DataFrame(records, columns=["Tanggal", "Kategori", "Aktivitas", "Skor", "Rating", "Mood", "Saran", "Catatan"])
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(filename, index=False)

def hitung_streak(df):
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df = df.sort_values('Tanggal', ascending=False)
    streak = 0
    today = datetime.now().date()
    for t in df['Tanggal']:
        if t.date() == today - timedelta(days=streak):
            streak += 1
        else:
            break
    return streak

# ------------------ LOGIN ------------------
print("\n===== SELAMAT DATANG DI SMARTMOOD =====")
username = input("Masukkan username: ").strip().lower()
password = input("Masukkan password: ")  # Untuk simulasi, tidak dicek benar/salah
print(f"\n✅ Login berhasil sebagai: {username}")

# ------------------ MENU UTAMA ------------------
while True:
    print("\n===== MENU SMARTMOOD =====")
    print("1. Input Aktivitas & Mood")
    print("2. Lihat Grafik Mood Harian")
    print("3. Reset Data")
    print("4. Tentang Aplikasi")
    print("5. Keluar")
    pilih = input("Pilih menu [1-5]: ")

    if pilih == "1":
        aktivitas_data = {}
        total_skor = 0
        for kategori, daftar in kategori_aktivitas.items():
            print(f"\nKategori {kategori}:")
            for i, act in enumerate(daftar, 1):
                print(f"{i}. {act}")
            try:
                idx = int(input(f"Pilih 1 aktivitas dari {kategori}: ")) - 1
                aktivitas = daftar[idx]
                aktivitas_data[kategori] = aktivitas
                total_skor += aktivitas_skor.get(aktivitas, 0)
            except:
                print("❌ Lewatkan kategori ini.")

        try:
            rating = int(input("\nRating mood kamu hari ini (1-5): "))
            catatan = input("Catatan harian (opsional): ")
            tanggal = datetime.now().strftime("%Y-%m-%d")
            mood, saran = classify_mood(total_skor + rating * 2)
            simpan_data(username, tanggal, aktivitas_data, rating, mood, saran, catatan)
            print(f"\n✅ Data berhasil disimpan. Mood: {mood}\n💡 Saran: {saran}")
        except:
            print("❌ Input tidak valid.")

    elif pilih == "2":
        file = f"{DATA_FOLDER}/data_{username}.csv"
        if not os.path.exists(file):
            print("❌ Belum ada data.")
            continue
        df = pd.read_csv(file)
        if len(df) < 3:
            print("⚠️ Data belum cukup (minimal 3 hari) untuk menampilkan grafik.")
        else:
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])
            df_daily = df.groupby("Tanggal").mean(numeric_only=True).reset_index()
            warna = df.groupby("Tanggal")["Mood"].last().map(lambda m: "green" if "Bahagia" in m else ("gold" if "Biasa" in m else "blue"))
            plt.figure(figsize=(10,4))
            plt.bar(df_daily["Tanggal"].dt.strftime("%d-%b"), df_daily["Skor"], color=warna)
            plt.title(f"Mood Harian - {username}")
            plt.xlabel("Tanggal")
            plt.ylabel("Skor Mood")
            plt.grid(True)
            plt.show()

            streak = hitung_streak(df)
            print(f"🔥 Kamu sudah konsisten selama {streak} hari berturut-turut! Pertahankan ya 💪")

    elif pilih == "3":
        file = f"{DATA_FOLDER}/data_{username}.csv"
        if os.path.exists(file):
            os.remove(file)
            print("✅ Data berhasil direset.")
        else:
            print("Tidak ada data untuk dihapus.")

    elif pilih == "4":
        print("""
📌 SmartMood Tracker membantu kamu merefleksikan suasana hati
berdasarkan aktivitas harian yang kamu lakukan.

✅ Input aktivitas 4 kategori + rating mood
✅ Saran mood otomatis berdasarkan data nyata
✅ Visualisasi grafik + deteksi streak
✅ Data pribadi tersimpan aman (per user)
""")

    elif pilih == "5":
        print("👋 Terima kasih sudah menggunakan SmartMood!")
        break

    else:
        print("❌ Menu tidak dikenali.")

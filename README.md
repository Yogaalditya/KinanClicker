# KinanClicker - Auto Clicker Python

Auto Clicker sederhana dengan GUI yang memungkinkan Anda mengotomatisasi klik mouse dengan interval yang dapat disesuaikan.

## 🎯 Fitur

- ✅ **UI Sederhana**: Interface yang rapi dan mudah dipahami
- ✅ **Input Interval**: Atur interval klik dalam milisecond (ms)
- ✅ **Jenis Klik**: Pilih antara klik kiri atau kanan
- ✅ **Global Hotkey**: F6 untuk Start, F7 untuk Stop
- ✅ **Background Execution**: Tetap berjalan meski jendela tidak aktif
- ✅ **Validasi Input**: Memastikan input yang valid
- ✅ **Status Real-time**: Menampilkan status Running/Stopped
- ✅ **Multi-Platform**: Bekerja di Windows, Linux, dan macOS

## 📁 Struktur Folder Project

```
KinanClicker/
├── main.py              # File utama - GUI dan entry point
├── auto_clicker.py      # Module logic auto clicker
├── requirements.txt     # Dependencies project
└── README.md           # Dokumentasi (file ini)
```

## 🔧 Cara Kerja Program

### Backend Logic (auto_clicker.py)
- **Threading**: Auto click berjalan di thread terpisah agar tidak memblokir UI
- **Interval**: Setiap interval (ms) yang ditentukan, program melakukan klik mouse
- **Click Type**: Mendukung left click dan right click
- **Validasi**: Input interval harus berupa angka positif

### Frontend (main.py)
- **tkinter GUI**: Interface sederhana dengan entry input, dropdown, dan buttons
- **Global Hotkey**: Menggunakan library `keyboard` untuk mendeteksi F6 dan F7
- **Status Update**: Label status diupdate setiap 500ms
- **Button Toggle**: Tombol Start/Stop aktif/nonaktif sesuai status

### Mekanisme Klik
```
┌─────────────────────────────────────┐
│ Thread Terpisah (_click_loop)       │
├─────────────────────────────────────┤
│ 1. Loop: while running == True      │
│ 2. Klik mouse (left/right)          │
│ 3. Sleep sesuai interval_ms         │
│ 4. Ulangi sampai stop ditekan       │
└─────────────────────────────────────┘
```

## 📦 Requirements

- Python 3.6+
- mouse (untuk kontrol mouse)
- keyboard (untuk global hotkey)
- tkinter (built-in dengan Python)

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau manual install:
```bash
pip install mouse keyboard
```

### 2. Jalankan Program

```bash
python main.py
```

### 3. Menggunakan Program

1. **Set Interval (ms)**: Masukkan interval dalam ms (default: 100 ms)
2. **Pilih Jenis Klik**: Dropdown untuk memilih Left atau Right
3. **Start/Stop**:
   - Click tombol "▶ START" atau tekan **F6** untuk memulai
   - Click tombol "⏹ STOP" atau tekan **F7** untuk berhenti
4. **Monitor Status**: Lihat label status berubah menjadi 🟢 RUNNING atau 🔴 STOPPED

## ⚠️ Catatan Penting

- **Admin/Root Access**: Di beberapa sistem, Anda mungkin perlu menjalankan dengan admin/root untuk akses global hotkey
- **Dangerous**: Gunakan dengan hati-hati! Klik otomatis bisa merusak data jika tidak dikelola dengan benar
- **Stop Cepat**: Selalu ada tombol STOP dan hotkey F7 untuk menghentikan kapan saja
- **Background**: Program tetap berjalan di background, jadi Anda bisa melakukan kegiatan lain

## 📋 Validasi Input

- **Interval**: Harus berupa angka > 0, jika invalid akan muncul error message
- **Jenis Klik**: Hanya bisa "left" atau "right" dari dropdown
- **Status**: Tidak bisa start ketika sudah running, dan stop ketika sudah stopped

## 🔐 Keamanan

- Tidak ada data yang dikirim ke internet
- Tidak ada logging atau tracking
- Semua proses lokal di mesin Anda

## 🐛 Troubleshooting

| Issue | Solusi |
|-------|--------|
| Hotkey tidak bekerja | Jalankan dengan admin/root access |
| Mouse click tidak terdeteksi | Pastikan fokus pada window yang ingin di-click |
| Program error saat start | Pastikan interval adalah angka positif |
| Permission denied | Jalankan terminal dengan `sudo` atau RunAs Admin |

## 📝 Contoh Penggunaan

1. **Farming Game**: Set interval 500ms untuk auto-click
2. **Clicker Game**: Set interval 100ms untuk cepat
3. **Form Filling**: Set interval 1000ms untuk klik interval besar

## 💡 Tips

- Mulai dengan interval 500ms, kemudian adjust sesuai kebutuhan
- Gunakan Right Click untuk context menu automation
- Gunakan F7 untuk emergency stop
- Monitor CPU usage jika interval terlalu kecil (< 50ms)

## 📄 Lisensi

Bebas digunakan untuk keperluan pribadi dan edukatif.

---

**Dibuat dengan ❤️ untuk otomasi mouse clicking**

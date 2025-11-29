# 🚀 Quick Start Guide - KinanClicker

## Langkah 1: Persiapan

```bash
cd KinanClicker
pip install -r requirements.txt
```

## Langkah 2: Jalankan

```bash
python main.py
```

## Langkah 3: Gunakan

1. **Input Interval**: Masukkan nilai interval klik (ms), default 100. Hanya angka positif yang valid.
   - 100 ms = 10 klik per detik
   - 500 ms = 2 klik per detik
   - 1000 ms = 1 klik per detik
   - Jika input tidak valid, akan muncul error.
2. **Pilih Jenis Klik**: Pilih "left" atau "right" dari dropdown.
3. **Pengaturan Hotkey**: Klik tombol "🔧 HOTKEY SETTINGS" untuk mengubah hotkey Start/Stop sesuai keinginan.
   - Default: F6 (Start), F7 (Stop)
   - Info hotkey tampil di bawah tombol
4. **Start**:
   - Klik tombol "START" atau tekan hotkey Start
   - Status akan berubah menjadi 🟢 RUNNING
   - Tombol Start nonaktif saat running
5. **Stop**:
   - Klik tombol "STOP" atau tekan hotkey Stop
   - Status akan berubah menjadi 🔴 STOPPED
   - Tombol Stop nonaktif saat stopped
6. **Status & Info**:
   - Status real-time di label bawah tombol
   - Info hotkey dan mode background tampil di UI

## 📌 Contoh Interval

| Use Case     | Interval |
|-------------|----------|
| Super cepat | 50 ms    |
| Cepat       | 100-200 ms |
| Normal      | 500 ms   |
| Lambat      | 1000+ ms |

## ⚙️ Pengaturan Lanjut

Edit `auto_clicker.py` jika ingin customize:
- Ganti `interval_ms = 100` untuk default berbeda
- Tambah fitur baru di class `AutoClicker`

## 🆘 Bantuan

Lihat README.md untuk dokumentasi lengkap dan troubleshooting.

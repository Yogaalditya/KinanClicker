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

1. **Input Interval**: Ubah nilai 100 (default) sesuai kebutuhan
   - 100 ms = 10 klik per detik
   - 500 ms = 2 klik per detik
   - 1000 ms = 1 klik per detik

2. **Pilih Jenis Klik**: Left atau Right dari dropdown

3. **Start**:
   - Klik tombol "START" atau tekan **F6**
   - Status akan berubah menjadi 🟢 RUNNING

4. **Stop**:
   - Klik tombol "STOP" atau tekan **F7**
   - Status akan berubah menjadi 🔴 STOPPED

## 📌 Contoh Interval

| Use Case | Interval |
|----------|----------|
| Super cepat | 50 ms |
| Cepat | 100-200 ms |
| Normal | 500 ms |
| Lambat | 1000+ ms |

## ⚙️ Pengaturan Lanjut

Edit `auto_clicker.py` jika ingin customize:
- Ganti `interval_ms = 100` untuk default berbeda
- Tambah fitur baru di class `AutoClicker`

## 🆘 Bantuan

Lihat README.md untuk dokumentasi lengkap dan troubleshooting.

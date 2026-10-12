<div align="center">

# 🎬 snatch

**Download video dari 1000+ situs — YouTube, TikTok, Instagram, Twitter/X, Reddit, Bilibili, dan lainnya.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dl-red)](https://github.com/yt-dlp/yt-dlp)

</div>

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/Syqmhmmd-commits/snatch-downloader-cli.git
cd snatch-downloader-cli

# 2. Buat & aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Install
pip install -e .

# 4. Test
snatch --help
```

Kalau muncul `usage: snatch [-h] {info,download,batch} ...` → **berhasil!**

> ⚠️ **Wajib install `ffmpeg`** dulu. Lihat bagian Instalasi per OS di bawah.

---

## 📖 Deskripsi

**snatch** adalah tool download video yang simpel, cepat, dan open source — alternatif ringan dari situs download yang penuh iklan popup. Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp), engine download paling stabil saat ini.

### ✨ Fitur

- 🎬 **Multi-platform** — YouTube, TikTok, Twitter/X, Reddit, Bilibili, Vimeo, Twitch, Instagram, dan **1000+ situs** lainnya
- 📺 **Multi-resolusi** — Dari **144p sampai 8K**
- 🎵 **Audio only** — Ekstrak audio jadi **MP3**
- 🍪 **Cookie support** — Untuk situs yang butuh login (Bilibili, Instagram, Facebook)
- ⚡ **Prioritas H.264** — Kompatibel di semua device (HP lama, TV, dll)
- 🎯 **Auto format selection** — Pilih codec & protocol terbaik otomatis
- 💻 **CLI interaktif** — Prompt pilih resolusi dengan arrow keys (↑↓)
- 📦 **Batch download** — Download banyak URL dari file `.txt`
- 🗂️ **Auto-archive** — Skip video yang sudah pernah didownload

---

## 🧰 Kebutuhan

| Tool | Wajib? | Versi | Fungsi |
|------|--------|-------|--------|
| **Python** | ✅ | 3.10+ | Menjalankan `snatch` |
| **pip** | ✅ | — | Install dependencies |
| **ffmpeg** | ✅ | 4.0+ | Merge video + audio, ekstrak MP3 |
| **git** | ⚠️ | — | Clone repo |
| **Node.js** | 💡 | 22+ | Solve JS challenge YouTube (recommended) |

---

## 🚀 Instalasi

### 🐧 Linux (Ubuntu / Debian / Mint)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git nodejs npm
```

### 🐧 Fedora / RHEL

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv ffmpeg git nodejs npm
```

### 🐧 Arch / Manjaro

```bash
sudo pacman -S --needed python python-pip ffmpeg git nodejs npm
```

### 🪟 Windows

1. Install Python dari [python.org](https://www.python.org/downloads/) — ⚠️ centang **"Add Python to PATH"**
2. Install ffmpeg: `winget install ffmpeg`
3. Install Node.js LTS dari [nodejs.org](https://nodejs.org/)

```powershell
git clone https://github.com/Syqmhmmd-commits/snatch-downloader-cli.git
cd snatch-downloader-cli
python -m venv venv
venv\Scripts\activate
pip install -e .
```

### 🍎 macOS

```bash
brew install python@3.12 ffmpeg git node
git clone https://github.com/Syqmhmmd-commits/snatch-downloader-cli.git
cd snatch-downloader-cli
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## 🎯 Cara Pakai

```bash
# Cek instalasi
snatch --help

# Download interaktif (pilih resolusi dengan ↑↓)
snatch download "https://youtu.be/dQw4w9WgXcQ"

# Download kualitas 720p
snatch download "https://youtu.be/dQw4w9WgXcQ" -q 720

# Audio only (MP3)
snatch download "https://youtu.be/dQw4w9WgXcQ" -a

# Info video tanpa download
snatch info "https://youtu.be/dQw4w9WgXcQ"

# Bilibili / Instagram (butuh cookies, tutup browser dulu)
snatch download "URL" --cookies firefox

# Batch download dari file
snatch batch urls.txt -q 720
```

---

## ⚙️ Opsi CLI

```
snatch download URL [opsi]

  -o, --output PATH       Folder output (default: downloads/)
  -q, --quality RES       Kualitas: 4320, 2160, 1440, 1080, 720, 480
  -a, --audio             Hanya audio (MP3)
  --cookies BROWSER       Cookies dari browser (firefox/chrome/edge)
  --cookies-file PATH     Path ke cookies.txt
  --archive PATH          Skip video yang sudah didownload
```

---

## 📋 Platform yang Didukung

YouTube, TikTok, Twitter/X, Reddit, Vimeo, Twitch, Bilibili, Instagram, Facebook, dan **1000+ situs** lainnya.

Daftar lengkap: [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

---

## 🐛 Troubleshooting

| Error | Solusi |
|-------|--------|
| `snatch: command not found` | Aktifkan venv dulu, lalu `pip install -e .` |
| `ffmpeg not found` | Install ffmpeg, cek `ffmpeg -version` |
| `No supported JavaScript runtime` | Install Node.js ≥ 22, lalu `pip install -U "yt-dlp[default]"` |
| `You need to log in` | Pakai `--cookies firefox` |
| `ModuleNotFoundError: downloader` | Pastikan `pyproject.toml` di root folder project |

---

## 🏗️ Struktur Project

```
snatch-downloader-cli/
├── downloader/
│   ├── __init__.py
│   ├── core.py          # Logika download
│   ├── cli.py           # Interface CLI
│   └── interactive.py   # Prompt interaktif
├── main.py
├── pyproject.toml       # ⚠️ HARUS di root
├── README.md
└── LICENSE
```

---

## ⚠️ Disclaimer

`snatch` hanya untuk **penggunaan pribadi**. Hormati hak cipta pembuat konten.

---

## 📄 Lisensi

MIT License — lihat [LICENSE](LICENSE).

---

<div align="center">

**Dibuat dengan Python & yt-dlp.**

⭐ Kalau project ini berguna, kasih bintang di GitHub!

</div>

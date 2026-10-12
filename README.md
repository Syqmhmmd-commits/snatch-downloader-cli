<div align="center">

# 🎬 vdl

**Download video dari 1000+ situs — YouTube, TikTok, Instagram, Twitter/X, Reddit, Bilibili, dan lainnya.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dl-red)](https://github.com/yt-dlp/yt-dlp)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

</div>

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/Syqmhmmd-commits/vdl-Downloader-cli.git
cd vdl-Downloader-cli

# 2. Buat & aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Install
pip install -e .

# 4. Test
vdl --help
```

Kalau muncul `usage: vdl [-h] {info,download,batch} ...` → **berhasil!**

> ⚠️ **Wajib install `ffmpeg`** dulu. Lihat bagian Instalasi per OS di bawah.

---

## 📖 Deskripsi

**vdl** adalah tool download video yang simpel, cepat, dan open source — alternatif ringan dari situs download yang penuh iklan popup. Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp), engine download paling stabil saat ini.

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
| **Python** | ✅ | 3.10+ | Menjalankan `vdl` |
| **pip** | ✅ | — | Install dependencies |
| **ffmpeg** | ✅ | 4.0+ | Merge video + audio, ekstrak MP3 |
| **git** | ⚠️ | — | Clone repo (opsional kalau download ZIP) |
| **Node.js** | 💡 | 22+ | Solve JS challenge YouTube (recommended) |
| **aria2c** | 💡 | — | Multi-connection download (lebih cepat) |
| **curl_cffi** | 💡 | — | Browser impersonation (beberapa situs butuh) |

---

## 🚀 Instalasi per OS

### 🐧 Linux

#### Ubuntu / Debian / Mint / Pop!_OS / Kali

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git nodejs npm
```

#### Fedora / RHEL / CentOS Stream

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv ffmpeg git nodejs npm
```

#### Arch / Manjaro / EndeavourOS

```bash
sudo pacman -S --needed python python-pip ffmpeg git nodejs npm
```

#### openSUSE

```bash
sudo zypper install -y python3 python3-pip python3-virtualenv ffmpeg git nodejs npm
```

#### Alpine

```bash
sudo apk add python3 py3-pip py3-virtualenv ffmpeg git nodejs npm
```

**Lalu clone & install** (semua distro Linux):

```bash
git clone https://github.com/Syqmhmmd-commits/vdl-Downloader-cli.git
cd vdl-Downloader-cli
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

### 🪟 Windows

**1. Install Python**

Download dari [python.org/downloads](https://www.python.org/downloads/) → jalankan installer → ⚠️ **centang "Add Python to PATH"** → Install Now.

Atau via Microsoft Store: cari **Python 3.12** → Install.

**2. Install ffmpeg**

```powershell
winget install ffmpeg
```

Alternatif:
```powershell
choco install ffmpeg
```

Atau manual download dari [ffmpeg.org](https://ffmpeg.org/download.html), ekstrak ke `C:\ffmpeg`, lalu tambahkan `C:\ffmpeg\bin` ke PATH.

**3. Install Node.js (opsional, recommended)**

Download LTS dari [nodejs.org](https://nodejs.org/), jalankan installer.

**4. Clone & install vdl**

```powershell
git clone https://github.com/Syqmhmmd-commits/vdl-Downloader-cli.git
cd vdl-Downloader-cli

python -m venv venv
venv\Scripts\activate
pip install -e .
```

---

### 🍎 macOS

**1. Install Homebrew** (kalau belum ada)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install dependencies**

```bash
brew install python@3.12 ffmpeg git node
```

**3. Clone & install vdl**

```bash
git clone https://github.com/Syqmhmmd-commits/vdl-Downloader-cli.git
cd vdl-Downloader-cli
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## 🎯 Cara Pakai

### Cek instalasi

```bash
vdl --help
```

Harus muncul:
```
usage: vdl [-h] {info,download,batch} ...
```

### Download interaktif

```bash
vdl download "https://youtu.be/dQw4w9WgXcQ"
```
Navigasi resolusi dengan **↑↓**, konfirmasi dengan **Enter**.

### Download dengan kualitas tertentu

```bash
vdl download "https://youtu.be/dQw4w9WgXcQ" -q 720
```

### Audio only (MP3)

```bash
vdl download "https://youtu.be/dQw4w9WgXcQ" -a
```

### Lihat info video tanpa download

```bash
vdl info "https://youtu.be/dQw4w9WgXcQ"
```

### Bilibili / Instagram (butuh cookies)

```bash
vdl download "URL" --cookies firefox
```
> Tutup browser dulu sebelum pakai opsi ini.

### Batch download dari file

```bash
# Bikin file urls.txt berisi daftar URL (satu per baris)
vdl batch urls.txt -q 720
```

---

## ⚙️ Opsi CLI

```
vdl download URL [opsi]

  -o, --output PATH       Folder output (default: downloads/)
  -q, --quality RES       Kualitas: 4320, 2160, 1440, 1080, 720, 480
  -a, --audio             Hanya audio (MP3)
  --cookies BROWSER       Cookies dari browser (firefox/chrome/edge)
  --cookies-file PATH     Path ke cookies.txt
  --archive PATH          Skip video yang sudah didownload
```

---

## 📋 Platform yang Didukung

| Platform | Contoh URL | Cookies? |
|----------|-----------|----------|
| **YouTube** | `https://youtu.be/VIDEO_ID` | ❌ |
| **TikTok** | `https://www.tiktok.com/@user/video/ID` | ❌ |
| **Twitter/X** | `https://x.com/user/status/ID` | ❌ |
| **Reddit** | `https://www.reddit.com/r/sub/comments/ID/` | ❌ |
| **Vimeo** | `https://vimeo.com/ID` | ❌ |
| **Twitch** | `https://www.twitch.tv/videos/ID` | ⚠️ |
| **Bilibili** | `https://www.bilibili.tv/video/ID` | ✅ |
| **Instagram** | `https://www.instagram.com/reel/ID/` | ✅ |
| **Facebook** | `https://www.facebook.com/watch?v=ID` | ⚠️ |

Daftar lengkap: [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

---

## 🐛 Troubleshooting

| Error | Solusi |
|-------|--------|
| `vdl: command not found` | Aktifkan venv: `source venv/bin/activate` (Linux/Mac) atau `venv\Scripts\activate` (Windows), lalu `pip install -e .` |
| `ffmpeg not found` | Install ffmpeg, cek dengan `ffmpeg -version` |
| `No supported JavaScript runtime` | Install Node.js ≥ 22, lalu `pip install -U "yt-dlp[default]"` |
| `You need to log in to access this content` | Pakai `--cookies firefox` |
| `429 Too Many Requests` | Rate limit (biasanya Instagram). Tunggu 30-60 menit |
| `ModuleNotFoundError: No module named downloader` | Pastikan `pyproject.toml` ada di **root** folder project (bukan di subfolder), lalu `pip install -e .` |
| `pip install` error di Python 3.14 | Pakai Python 3.12: hapus venv, lalu `python3.12 -m venv venv` |

---

## 🏗️ Struktur Project

```
vdl-Downloader-cli/
├── downloader/
│   ├── __init__.py
│   ├── core.py          # Logika download (single source of truth)
│   ├── cli.py           # Interface CLI
│   └── interactive.py   # Prompt interaktif
├── main.py
├── pyproject.toml       # ⚠️ HARUS di root, jangan dipindah
├── README.md
└── LICENSE
```

> **Prinsip desain**: `core.py` adalah **single source of truth** — logic download dipakai bareng oleh CLI dan interactive prompt.

---

## 🛠️ Teknologi

- **[Python 3.10+](https://www.python.org/)**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — Engine download
- **[questionary](https://github.com/tmbo/questionary)** — Prompt interaktif
- **[ffmpeg](https://ffmpeg.org/)** — Merge video + audio
- **[Node.js](https://nodejs.org/)** — JS runtime untuk YouTube

---

## ⚠️ Disclaimer

`vdl` hanya untuk **penggunaan pribadi**. Hormati hak cipta pembuat konten. Jangan gunakan untuk mendistribusikan ulang konten berhak cipta.

---

## 🤝 Kontribusi

Pull request selalu welcome! Fork repo, buat branch baru, commit, push, dan buka Pull Request.

---

## 📄 Lisensi

MIT License — lihat [LICENSE](LICENSE).

---

<div align="center">

**Dibuat dengan Python & yt-dlp.**

⭐ Kalau project ini berguna, kasih bintang di GitHub!

</div>

<div align="center">

# 🎬 vdl

**Download video dari 1000+ situs — YouTube, Instagram, TikTok, Twitter/X, Reddit, Bilibili, dan lainnya.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dl-red)](https://github.com/yt-dlp/yt-dlp)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

</div>

---

## 📖 Deskripsi

**vdl** adalah tool download video yang simpel, cepat, dan open source. Dibuat sebagai alternatif ringan dari situs download yang penuh iklan popup. Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) — engine download paling stabil saat ini.

Tersedia dalam **2 mode**:
- 💻 **CLI** — Command line interaktif dengan prompt pilih resolusi
- 🌐 **Web UI** — Interface modern untuk diakses dari browser (termasuk HP via LAN/ngrok)

### ✨ Fitur Utama

- 🎬 **Multi-platform** — YouTube, TikTok, Twitter/X, Reddit, Bilibili, Vimeo, Twitch, Instagram (dengan cookies), dan **1000+ situs** lainnya
- 📺 **Multi-resolusi** — Dari **144p sampai 8K**
- 🎵 **Audio only** — Ekstrak audio jadi **MP3**
- 🍪 **Cookie support** — Untuk situs yang butuh login (Bilibili, Instagram private, Facebook)
- ⚡ **Prioritas H.264** — Kompatibel di semua device (HP lama, TV, dll)
- 🎯 **Auto format selection** — Pilih codec & protocol terbaik secara otomatis (H.264 > VP9 > AV1, DASH > HLS)
- 💻 **CLI interaktif** — Prompt pilih resolusi dengan arrow keys (↑↓)
- 🌐 **Web UI** — Preview video, pilih resolusi, download dari browser
- 📦 **Batch download** — Download banyak URL dari file `.txt`
- 🗂️ **Auto-archive** — Skip video yang sudah pernah didownload
- 🧹 **Auto-delete** — File di server otomatis dihapus setelah dikirim ke device

---

## 🧰 Tools yang Dibutuhkan

### Wajib

| Tool | Versi Minimal | Fungsi |
|------|---------------|--------|
| **Python** | 3.10+ | Menjalankan `vdl` |
| **pip** | (bawaan Python) | Install dependencies |
| **ffmpeg** | 4.0+ | Merge video + audio, ekstrak MP3 |
| **git** | (opsional) | Clone repo |

### Opsional (untuk performa)

| Tool | Fungsi | Tanpa ini |
|------|--------|-----------|
| **Node.js** | Solve JS challenge YouTube | Warning, beberapa format tidak tersedia |
| **aria2c** | Multi-connection download | Download lebih lambat |
| **curl_cffi** | Browser impersonation | Beberapa situs gagal |

---

## 🚀 Instalasi

Pilih sesuai OS kamu:

### 🪟 Windows

#### 1. Install Python

**Cara A — Microsoft Store (paling mudah):**
1. Buka **Microsoft Store**
2. Cari **Python 3.12** (atau versi 3.10+)
3. Klik **Install**

**Cara B — Installer Resmi:**
1. Buka [python.org/downloads](https://www.python.org/downloads/)
2. Download **Windows installer (64-bit)**
3. Jalankan installer
4. ⚠️ **PENTING**: Centang **"Add Python to PATH"** sebelum klik Install
5. Klik **Install Now**

Cek instalasi — buka **Command Prompt** atau **PowerShell**:

```powershell
python --version
pip --version
```

#### 2. Install ffmpeg

**Cara A — winget (Windows 10/11):**
```powershell
winget install ffmpeg
```

**Cara B — Chocolatey:**
```powershell
choco install ffmpeg
```

**Cara C — Manual:**
1. Download dari [ffmpeg.org/download.html](https://ffmpeg.org/download.html) → pilih **Windows builds**
2. Ekstrak ke `C:\ffmpeg`
3. Tambahkan `C:\ffmpeg\bin` ke **PATH**:
   - Tekan `Win + R` → ketik `sysdm.cpl` → Enter
   - Tab **Advanced** → **Environment Variables**
   - Di **System variables**, pilih **Path** → **Edit**
   - Klik **New** → ketik `C:\ffmpeg\bin` → OK

Cek instalasi (buka terminal baru):

```powershell
ffmpeg -version
```

#### 3. Install Node.js (opsional, direkomendasikan)

1. Buka [nodejs.org](https://nodejs.org/)
2. Download **LTS version**
3. Jalankan installer (semua default OK)

Cek:

```powershell
node --version   # harus v22.0.0 atau lebih baru
```

#### 4. Clone & Install vdl

```powershell
# Clone repo
git clone https://github.com/Syqmhmmd-commits/vdl.git
cd vdl

# Buat virtual environment
python -m venv venv

# Aktifkan venv
venv\Scripts\activate

# Install vdl
pip install -e .
```

**Catatan**: Kalau `git` tidak ada, install dari [git-scm.com](https://git-scm.com/) atau download repo sebagai ZIP.

---

### 🍎 macOS

#### 1. Install Homebrew (kalau belum ada)

Buka **Terminal** (`Cmd + Space` → "Terminal"), lalu:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Ikuti instruksi yang muncul. Setelah selesai, tutup dan buka ulang Terminal.

Cek:

```bash
brew --version
```

#### 2. Install Python, ffmpeg, git, Node.js

```bash
brew install python@3.12 ffmpeg git node
```

Cek:

```bash
python3 --version   # harus 3.10+
ffmpeg -version
node --version      # harus v22.0.0+
```

#### 3. Clone & Install vdl

```bash
git clone https://github.com/Syqmhmmd-commits/vdl.git
cd vdl

python3 -m venv venv
source venv/bin/activate

pip install -e .
```

---

### 🐧 Linux

#### 📦 Ubuntu / Debian / Linux Mint / Pop!_OS / Kali

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git nodejs npm

python3 --version    # harus 3.10+
ffmpeg -version
```

**Kalau Python versi < 3.10** (misal Ubuntu 20.04):

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-pip
```

Ganti `python3` jadi `python3.12` di langkah berikutnya.

#### 📦 Fedora / RHEL / CentOS Stream

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv ffmpeg git nodejs npm
```

#### 📦 Arch Linux / Manjaro / EndeavourOS

```bash
sudo pacman -S --needed python python-pip ffmpeg git nodejs npm
```

#### 📦 openSUSE / SLES

```bash
sudo zypper install -y python3 python3-pip python3-virtualenv ffmpeg git nodejs npm
```

#### 📦 Alpine Linux

```bash
sudo apk add python3 py3-pip py3-virtualenv ffmpeg git nodejs npm
```

#### 📦 Gentoo

```bash
sudo emerge --ask dev-lang/python dev-python/pip media-video/ffmpeg dev-vcs/git net-libs/nodejs
```

#### 📦 Void Linux

```bash
sudo xbps-install -S python3 python3-pip ffmpeg git nodejs
```

#### Clone & Install vdl (semua distro)

```bash
git clone https://github.com/Syqmhmmd-commits/vdl.git
cd vdl

python3 -m venv venv
source venv/bin/activate

pip install -e .
```

**Catatan untuk distro immutable** (Fedora Silverblue, openSUSE MicroOS, Bazzite) — gunakan `toolbox`:

```bash
toolbox create vdl-dev
toolbox enter vdl-dev
# Di dalam toolbox:
sudo dnf install -y python3-pip ffmpeg git nodejs npm
git clone https://github.com/Syqmhmmd-commits/vdl.git
cd vdl
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## 🎯 Cara Pakai — Sampai Berhasil

### 📌 Cek Instalasi

```bash
vdl --help
```

Output yang diharapkan:

```
usage: vdl [-h] {info,download,batch} ...
```

**Kalau `vdl: command not found`** → pastikan venv aktif.

### 🎬 Contoh 1: Download Interaktif

```bash
vdl download "https://youtu.be/dQw4w9WgXcQ"
```

Akan muncul prompt pilih resolusi. Navigasi dengan **↑↓**, konfirmasi dengan **Enter**.

### 🎬 Contoh 2: Download Non-Interaktif

```bash
vdl download "https://youtu.be/dQw4w9WgXcQ" -q 720
```

### 🎬 Contoh 3: Audio Only (MP3)

```bash
vdl download "https://youtu.be/dQw4w9WgXcQ" -a
```

### 🎬 Contoh 4: Lihat Info

```bash
vdl info "https://youtu.be/dQw4w9WgXcQ"
```

### 🎬 Contoh 5: Bilibili (Butuh Cookies)

```bash
# Tutup Firefox dulu
vdl download "https://www.bilibili.tv/video/xxx" --cookies firefox
```

### 🎬 Contoh 6: Batch Download

```bash
cat > urls.txt << 'URLS'
https://youtu.be/video1
https://youtu.be/video2
URLS

vdl batch urls.txt -q 720
```

### 🌐 Contoh 7: Web UI

```bash
uvicorn web.app:app --host 0.0.0.0 --port 8000
```

Buka **http://127.0.0.1:8000**

Akses dari HP (1 WiFi):
1. Cek IP laptop: `hostname -I | awk '{print $1}'` (Linux/Mac) atau `ipconfig` (Windows)
2. Di HP: `http://IP_LAPTOP:8000`

Akses dari mana saja via ngrok:
```bash
ngrok http 8000
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

| Platform | URL Pattern | Cookies? |
|----------|-------------|----------|
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

### `vdl: command not found`

Aktifkan venv dulu:
```bash
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
pip install -e .
```

### `ffmpeg not found`

Install ffmpeg (lihat bagian Instalasi). Cek: `ffmpeg -version`

### `No supported JavaScript runtime` (YouTube)

Install Node.js ≥ 22.0, lalu:
```bash
pip install -U "yt-dlp[default]"
```

### `You need to log in to access this content`

```bash
vdl download "URL" --cookies firefox
```

### `429 Too Many Requests`

Rate limit (biasanya Instagram). Tunggu 30-60 menit.

### `pip install` error di Python 3.14

Pakai Python 3.12:
```bash
sudo apt install python3.12 python3.12-venv   # Linux
brew install python@3.12                       # macOS
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## 🏗️ Struktur Project

```
vdl/
├── downloader/
│   ├── core.py          # Logika download (shared CLI + Web)
│   ├── cli.py           # Interface CLI
│   └── interactive.py   # Prompt interaktif
├── web/
│   ├── app.py           # FastAPI
│   ├── templates/
│   └── static/
├── pyproject.toml
├── README.md
└── LICENSE
```

**Prinsip desain**: `core.py` adalah **single source of truth** — logic download dipakai bareng oleh CLI, Web, dan interactive prompt.

---

## 🛠️ Teknologi

- **[Python 3.10+](https://www.python.org/)**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — Engine download
- **[questionary](https://github.com/tmbo/questionary)** — Prompt interaktif
- **[FastAPI](https://fastapi.tiangolo.com/)** — Web framework
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server
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

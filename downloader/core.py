import os
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


class VDLError(Exception):
    """Base error untuk vdl."""
    pass


class RateLimitedError(VDLError):
    """IP kena rate limit (429)."""
    pass


class LoginRequiredError(VDLError):
    """Butuh cookies/login."""
    pass


class VideoUnavailableError(VDLError):
    """Video tidak tersedia / dihapus / private."""
    pass


class AlreadyDownloadedError(VDLError):
    """Video sudah pernah didownload (ada di archive)."""
    pass


QUALITY_HEIGHTS = {
    "4320": 4320,
    "2160": 2160,
    "1440": 1440,
    "1080": 1080,
    "720": 720,
    "480": 480,
}


def build_opts(output_dir: str = "downloads", quality: str = "best", audio_only: bool = False) -> dict:
    """Bangun opsi yt-dlp. Ini yang nanti bisa dipakai web juga."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    outtmpl = os.path.join(output_dir, "%(title)s [%(id)s].%(ext)s")

    if audio_only:
        fmt = "bestaudio/best"
        postprocessors = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
        format_sort = ["abr", "asr"]
    else:
        if quality in QUALITY_HEIGHTS and quality != "best":
            h = QUALITY_HEIGHTS[quality]
            # Filter protocol: prioritize http/https (DASH), exclude m3u8 (HLS)
            # HLS di YouTube punya fragmentasi tidak lengkap
            fmt = (
                f"bestvideo[vcodec^=avc1][height={h}][protocol^=http]+bestaudio[protocol^=http]/"
                f"bestvideo[height={h}][protocol^=http]+bestaudio[protocol^=http]/"
                f"bestvideo[vcodec^=avc1][height={h}]+bestaudio/"
                f"bestvideo[height={h}]+bestaudio/"
                f"bestvideo[vcodec^=avc1][height<={h}][protocol^=http]+bestaudio[protocol^=http]/"
                f"bestvideo[height<={h}][protocol^=http]+bestaudio[protocol^=http]/"
                f"bestvideo[vcodec^=avc1][height<={h}]+bestaudio/"
                f"bestvideo[height<={h}]+bestaudio/"
                f"best[height<={h}]"
            )
            format_sort = [f"res:{h}", "vbr", "abr"]
        else:
            fmt = (
                "bestvideo[vcodec^=avc1][protocol^=http]+bestaudio[protocol^=http]/"
                "bestvideo[protocol^=http]+bestaudio[protocol^=http]/"
                "bestvideo[vcodec^=avc1]+bestaudio/"
                "bestvideo+bestaudio/best"
            )
            format_sort = ["res", "vbr", "abr"]

        postprocessors = []

    return {
        "format": fmt,
        "format_sort": format_sort,
        "outtmpl": outtmpl,
        "merge_output_format": "mp4",
        "postprocessors": postprocessors,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [],
        "js_runtimes": {"node": {}},
        "remote_components": {"ejs:github"},
        "keepvideo": False,
        "keep_fragments": False,
    }


def get_info(url: str) -> dict:
    """Ambil metadata tanpa download (buat preview di CLI/web)."""
    with YoutubeDL({
        "quiet": True,
        "skip_download": True,
        "js_runtimes": {"node": {}},
        "remote_components": {"ejs:github"},
    }) as ydl:
        return ydl.extract_info(url, download=False)


def download(url: str, output_dir: str = "downloads", quality: str = "best",
             audio_only: bool = False, cookies_from_browser: str | None = None,
             cookiefile: str | None = None,
             archive_file: str | None = None,
             progress_hook=None) -> str:
    opts = build_opts(output_dir, quality, audio_only)

    if cookies_from_browser:
        opts["cookiesfrombrowser"] = (cookies_from_browser,)
    if cookiefile:
        opts["cookiefile"] = cookiefile
    if archive_file:
        opts["download_archive"] = archive_file
    if progress_hook:
        opts["progress_hooks"].append(progress_hook)

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except DownloadError as e:
        msg = str(e).lower()
        if "429" in msg or "too many requests" in msg:
            raise RateLimitedError(
                "IP kena rate limit (429). Tunggu 30-60 menit."
            ) from e
        if "log in" in msg or "login required" in msg:
            raise LoginRequiredError(
                "Butuh login. Coba --cookies firefox atau --cookies-file."
            ) from e
        if "not available" in msg or "private" in msg:
            raise VideoUnavailableError(
                "Video tidak tersedia (dihapus/private/region lock)."
            ) from e
        raise VDLError(str(e)) from e

    if info is None:
        raise AlreadyDownloadedError(
            "Video sudah pernah didownload (ada di archive). "
            "Hapus .vdl-archive.txt kalau mau download ulang."
        )

    if "entries" in info:
        info = info["entries"][0]

    try:
        with YoutubeDL(opts) as ydl:
            filename = ydl.prepare_filename(info)
    except Exception:
        video_id = info.get("id", "")
        for f in Path(output_dir).glob(f"*[{video_id}]*"):
            return str(f)
        raise VDLError("Tidak bisa menemukan file hasil download")

    base, _ = os.path.splitext(filename)
    for ext in (".mp4", ".mp3", ".mkv", ".webm"):
        if os.path.exists(base + ext):
            return base + ext
    return filename

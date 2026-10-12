import argparse
import sys
from .core import (
    download, get_info,
    VDLError, RateLimitedError, LoginRequiredError,
    VideoUnavailableError, AlreadyDownloadedError,
)
from .interactive import run_interactive


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RED = "\033[31m"


def _c(text, color):
    return f"{color}{text}{C.RESET}"


def _banner():
    print(_c("╭─────────────────────────────────────╮", C.CYAN))
    print(_c("│", C.CYAN) + _c("  🎬 snatch ", C.BOLD) + _c("— Video Downloader", C.DIM) + _c("     │", C.CYAN))
    print(_c("╰─────────────────────────────────────╯", C.CYAN))


def cmd_info(url: str):
    _banner()
    print()
    info = get_info(url)
    print(f"  {_c('📌 Judul   :', C.BOLD)} {info.get('title')}")
    print(f"  {_c('⏱️  Durasi  :', C.BOLD)} {info.get('duration')} detik")
    print(f"  {_c('👤 Uploader:', C.BOLD)} {info.get('uploader')}")
    print(f"  {_c('🌐 Situs   :', C.BOLD)} {info.get('extractor')}")

    formats = info.get("formats", [])
    video_formats = [f for f in formats
                     if f.get("vcodec") != "none" and f.get("height")]
    if video_formats:
        print(f"\n  {_c('📺 Format video tersedia:', C.BOLD)}")
        seen = set()
        for f in sorted(video_formats, key=lambda x: x.get("height", 0), reverse=True):
            h = f["height"]
            codec = (f.get("vcodec") or "").split(".")[0]
            key = (h, codec)
            if key in seen:
                continue
            seen.add(key)
            size = f.get("filesize") or f.get("filesize_approx")
            size_str = f"{size / 1024 / 1024:.1f} MB" if size else "?"
            codec_color = C.GREEN if codec == "avc1" else C.MAGENTA
            print(f"    {_c('•', C.DIM)} {_c(f'{h}p', C.BOLD)} "
                  f"{_c(codec, codec_color)} {_c(size_str, C.DIM)}")


def cmd_download(args):
    _banner()

    interactive = args.quality is None

    if interactive:
        if not sys.stdin.isatty():
            print(_c("\n  ⚠️  Non-interactive mode (bukan TTY). Pakai -q untuk kualitas.", C.YELLOW))
            print(_c("  Contoh: vdl download \"URL\" -q 1080", C.DIM))
            sys.exit(1)

        result, out_dir = run_interactive(args.url, args.output)
        if result is None:
            sys.exit(0)

        if result == "audio":
            quality = "best"
            audio_only = True
        else:
            quality = str(result)
            audio_only = False
        output = out_dir
    else:
        quality = args.quality
        audio_only = args.audio
        output = args.output
        print()
        print(f"  {_c('URL:', C.DIM)} {args.url}")
        print(f"  {_c('Kualitas:', C.DIM)} {quality}")
        if audio_only:
            print(f"  {_c('Mode:', C.DIM)} Audio only (mp3)")

    print()

    try:
        path = download(
            url=args.url,
            output_dir=output,
            quality=quality,
            audio_only=audio_only,
            cookies_from_browser=args.cookies,
            cookiefile=args.cookies_file,
            archive_file=args.archive,
            progress_hook=None,
        )
        print()
        print(_c("  ✓ Selesai!", C.GREEN))
        print(f"  {_c('💾 Tersimpan di:', C.BOLD)} {path}")
    except AlreadyDownloadedError as e:
        print(_c(f"\n  ℹ️  {e}", C.CYAN))
        sys.exit(0)
    except RateLimitedError as e:
        print(_c(f"\n  ⏸️  {e}", C.YELLOW))
        sys.exit(2)
    except LoginRequiredError as e:
        print(_c(f"\n  🔒 {e}", C.YELLOW))
        sys.exit(3)
    except VideoUnavailableError as e:
        print(_c(f"\n  🚫 {e}", C.RED))
        sys.exit(4)
    except VDLError as e:
        print(_c(f"\n  ❌ Gagal: {e}", C.RED))
        sys.exit(1)


def cmd_batch(args):
    _banner()
    try:
        with open(args.file) as f:
            urls = [line.strip() for line in f
                    if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(_c(f"❌ File tidak ditemukan: {args.file}", C.RED))
        sys.exit(1)

    if not urls:
        print(_c(f"❌ File {args.file} kosong atau hanya berisi komentar", C.RED))
        sys.exit(1)

    print(f"\n  {_c(f'📋 {len(urls)} URL akan didownload', C.BOLD)}\n")
    success, failed = 0, 0

    for i, url in enumerate(urls, 1):
        print(_c(f"  [{i}/{len(urls)}]", C.CYAN), end=" ")
        print(url)
        try:
            path = download(
                url=url,
                output_dir=args.output,
                quality=args.quality,
                audio_only=args.audio,
                cookies_from_browser=args.cookies,
                cookiefile=args.cookies_file,
                archive_file=args.archive,
                progress_hook=None,
            )
            print(f"  {_c('✓', C.GREEN)} {path}")
            success += 1
        except AlreadyDownloadedError:
            print(f"  {_c('⏭️', C.CYAN)} Skip (sudah pernah didownload)")
            success += 1
        except VDLError as e:
            print(f"  {_c('✗', C.RED)} {e}")
            failed += 1
        print()

    print(_c(f"  📊 Selesai: {success} sukses, {failed} gagal", C.BOLD))


def main():
    parser = argparse.ArgumentParser(
        prog="vdl",
        description="Download video dari hampir semua situs (via yt-dlp)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="Lihat metadata video")
    p_info.add_argument("url")

    p_dl = sub.add_parser("download", help="Download video (interaktif kalau tanpa -q)")
    p_dl.add_argument("url")
    p_dl.add_argument("-o", "--output", default="downloads", help="Folder output")
    p_dl.add_argument("-q", "--quality", default=None,
                      help="Kualitas (4320, 2160, 1440, 1080, 720, 480). "
                           "Kalau tidak diisi, akan muncul prompt interaktif.")
    p_dl.add_argument("-a", "--audio", action="store_true",
                      help="Hanya audio (mp3)")
    p_dl.add_argument("--cookies", default=None,
                      help="Cookies dari browser (chrome/firefox/edge)")
    p_dl.add_argument("--cookies-file", default=None,
                      help="Path ke cookies.txt (format Netscape)")
    p_dl.add_argument("--archive", default=".vdl-archive.txt",
                      help="File untuk skip video yang sudah didownload")

    p_batch = sub.add_parser("batch", help="Download banyak URL dari file .txt")
    p_batch.add_argument("file", help="File .txt berisi URL (satu per baris)")
    p_batch.add_argument("-o", "--output", default="downloads")
    p_batch.add_argument("-q", "--quality", default="best",
                         choices=["best", "4320", "2160", "1440", "1080", "720", "480"])
    p_batch.add_argument("-a", "--audio", action="store_true")
    p_batch.add_argument("--cookies", default=None)
    p_batch.add_argument("--cookies-file", default=None)
    p_batch.add_argument("--archive", default=".vdl-archive.txt")

    args = parser.parse_args()

    if args.command == "info":
        cmd_info(args.url)
    elif args.command == "download":
        cmd_download(args)
    elif args.command == "batch":
        cmd_batch(args)


if __name__ == "__main__":
    main()

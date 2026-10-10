"""Interactive prompts untuk vdl CLI."""
import sys
from pathlib import Path

import questionary
from questionary import Style

from .core import get_info, VDLError


VDL_STYLE = Style([
    ("qmark", "fg:#6366f1 bold"),
    ("question", "bold"),
    ("answer", "fg:#10b981 bold"),
    ("pointer", "fg:#6366f1 bold"),
    ("highlighted", "fg:#6366f1 bold"),
    ("selected", "fg:#10b981"),
    ("separator", "fg:#8b8d9a"),
    ("instruction", "fg:#8b8d9a"),
    ("text", ""),
    ("disabled", "fg:#8b8d9a italic"),
])


def _human_size(n):
    if not n:
        return None
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def _human_duration(sec):
    if not sec:
        return "?"
    sec = int(sec)
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _codec_priority(codec):
    return {"H.264": 0, "VP9": 1, "AV1": 2}.get(codec, 9)


def _codec_label(vcodec):
    if not vcodec:
        return "?"
    if vcodec.startswith("avc1"):
        return "H.264"
    if vcodec.startswith("vp09") or vcodec.startswith("vp9"):
        return "VP9"
    if vcodec.startswith("av01"):
        return "AV1"
    return vcodec.split(".")[0] or "?"


def _truncate(text, max_len):
    if not text:
        return ""
    return text if len(text) <= max_len else text[:max_len - 3] + "..."


def show_video_info(info: dict) -> None:
    """Tampilkan preview video (simple)."""
    title = _truncate(info.get("title", "Tanpa judul"), 60)
    uploader = _truncate(info.get("uploader") or info.get("channel") or "?", 40)
    duration = _human_duration(info.get("duration"))
    extractor = info.get("extractor") or "?"

    print()
    print(f"  📺 {title}")
    print(f"     {uploader} · {duration} · {extractor}")


def _pick_best_for_height(variants: list) -> dict:
    """
    Pilih format terbaik untuk 1 resolusi.
    Prioritas:
      1. Format dengan filesize (bukan approx)
      2. DASH (https/http) > HLS (m3u8)
      3. Codec: H.264 > VP9 > AV1
      4. Bitrate tinggi
    """
    def score(f):
        has_size = 1 if f.get("filesize") else 0
        has_approx = 1 if f.get("filesize_approx") else 0
        proto = f.get("protocol", "")
        is_dash = 1 if (proto.startswith("http") and "m3u8" not in proto) else 0
        codec_prio = 10 - _codec_priority(_codec_label(f.get("vcodec", "")))
        tbr = f.get("tbr") or 0
        return (has_size, has_approx, is_dash, codec_prio, tbr)

    return sorted(variants, key=score, reverse=True)[0]


def build_choices(info: dict) -> list:
    formats = info.get("formats", [])

    by_height = {}
    for f in formats:
        vcodec = f.get("vcodec", "none")
        height = f.get("height")

        if not vcodec or vcodec == "none":
            continue
        if not height:
            continue
        ext = f.get("ext", "")
        if ext in ("mhtml",):
            continue
        note = (f.get("format_note") or "").lower()
        if "storyboard" in note:
            continue
        if "images" in (vcodec or "").lower():
            continue

        by_height.setdefault(height, []).append(f)

    choices = []
    for h in sorted(by_height.keys(), reverse=True):
        variants = by_height[h]
        best = _pick_best_for_height(variants)

        size = best.get("filesize") or best.get("filesize_approx")
        size_str = _human_size(size)
        codec = _codec_label(best.get("vcodec", ""))
        ext = best.get("ext", "").upper()

        if size_str:
            label = f"{h}p  ·  {codec}  ·  ~{size_str}  ({ext})"
        else:
            label = f"{h}p  ·  {codec}  ·  (size tidak tersedia)"

        choices.append(questionary.Choice(title=label, value=h))

    choices.append(questionary.Separator())
    choices.append(questionary.Choice(title="🎵 Audio only (MP3)", value="audio"))
    choices.append(questionary.Choice(title="🚫 Batal", value=None))

    return choices


def pick_resolution(info: dict, preselected: str = None):
    choices = build_choices(info)

    default = None
    if preselected and preselected != "best":
        try:
            target = int(preselected)
            for c in choices:
                if c.value == target:
                    default = c
                    break
        except (ValueError, TypeError):
            pass

    return questionary.select(
        "Pilih resolusi:",
        choices=choices,
        default=default,
        style=VDL_STYLE,
        qmark="?",
        instruction="(↑↓ pilih, Enter konfirmasi)",
    ).ask()


def confirm_download(output_dir: str) -> bool:
    return questionary.confirm(
        f"Download ke folder '{output_dir}'?",
        default=True,
        style=VDL_STYLE,
    ).ask()


def run_interactive(url: str, output_dir: str = "downloads", preselected: str = None):
    print()
    print("  🔍 Mengambil info video...")

    try:
        info = get_info(url)
    except Exception as e:
        print(f"\n  ❌ Gagal ambil info: {e}")
        return None, None

    if not info:
        print("\n  ❌ Tidak ada info yang bisa diambil dari URL ini.")
        return None, None

    show_video_info(info)

    formats = info.get("formats", [])
    has_video = any(
        (f.get("vcodec") or "none") != "none" and f.get("height")
        for f in formats
    )
    has_audio = any(
        (f.get("acodec") or "none") != "none" for f in formats
    )

    if not has_video and not has_audio:
        print("\n  ❌ Tidak ada format yang bisa didownload dari URL ini.")
        return None, None

    result = pick_resolution(info, preselected)

    if result is None:
        print("\n  🚫 Dibatalkan.")
        return None, None

    if not confirm_download(output_dir):
        print("\n  🚫 Dibatalkan.")
        return None, None

    return result, output_dir

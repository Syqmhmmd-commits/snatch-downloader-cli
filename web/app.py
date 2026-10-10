import uuid
import threading
import subprocess
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTask

from downloader.core import (
    download, get_info,
    VDLError, RateLimitedError, LoginRequiredError,
    VideoUnavailableError, AlreadyDownloadedError,
)

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI(title="vdl — Video Downloader")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

JOBS: dict[str, dict] = {}


def _human_size(n):
    if not n:
        return "?"
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


def render(request: Request, template: str, **kwargs):
    ctx = {"request": request, "active": ""}
    ctx.update(kwargs)
    return templates.TemplateResponse(request=request, name=template, context=ctx)


# ─── HALAMAN ───────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def page_index(request: Request):
    return render(request, "index.html", active="home")


@app.get("/downloader", response_class=HTMLResponse)
def page_downloader(request: Request):
    return render(request, "downloader.html", active="downloader")


@app.get("/about", response_class=HTMLResponse)
def page_about(request: Request):
    return render(request, "about.html", active="about")


@app.get("/faq", response_class=HTMLResponse)
def page_faq(request: Request):
    return render(request, "faq.html", active="faq")


@app.get("/contact", response_class=HTMLResponse)
def page_contact(request: Request):
    return render(request, "contact.html", active="contact")


@app.get("/supported", response_class=HTMLResponse)
def page_supported(request: Request):
    return render(request, "supported.html", active="supported")


# ─── API ───────────────────────────────────────────────────

@app.post("/api/info")
def api_info(url: str = Form(...)):
    try:
        info = get_info(url)
        thumbnail = info.get("thumbnail")
        if not thumbnail and info.get("thumbnails"):
            thumbnail = info["thumbnails"][-1].get("url")

        formats = []
        for f in info.get("formats", []):
            if f.get("vcodec") == "none":
                continue
            height = f.get("height")
            if not height:
                continue
            filesize = f.get("filesize") or f.get("filesize_approx")
            vcodec = f.get("vcodec") or ""
            if vcodec.startswith("avc1"):
                codec_label = "H.264"
            elif vcodec.startswith("vp09") or vcodec.startswith("vp9"):
                codec_label = "VP9"
            elif vcodec.startswith("av01"):
                codec_label = "AV1"
            else:
                codec_label = vcodec.split(".")[0] or "?"

            formats.append({
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "height": height,
                "filesize": filesize,
                "filesize_str": _human_size(filesize) if filesize else "?",
                "codec_label": codec_label,
            })

        seen = {}
        for f in formats:
            key = (f["height"], f["codec_label"])
            if key not in seen or (f["filesize"] or 0) > (seen[key]["filesize"] or 0):
                seen[key] = f
        formats = sorted(
            seen.values(),
            key=lambda x: (x["height"], {"H.264": 0, "VP9": 1, "AV1": 2}.get(x["codec_label"], 9)),
            reverse=True,
        )

        return {
            "ok": True,
            "title": info.get("title"),
            "duration_str": _human_duration(info.get("duration")),
            "uploader": info.get("uploader"),
            "extractor": info.get("extractor"),
            "thumbnail": thumbnail,
            "formats": formats,
        }
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=400)


@app.get("/api/stream")
def api_stream(url: str, quality: str = "720"):
    """
    Stream video langsung dari sumber ke device user.
    Tidak disimpan di laptop. Cocok untuk resolusi ≤720p (single format).
    """
    height = quality if quality.isdigit() else "720"
    fmt = (
        f"best[height<={height}][ext=mp4][vcodec^=avc1]/"
        f"best[height<={height}][ext=mp4]/"
        f"best[height<={height}]/"
        f"best"
    )

    def generate():
        cmd = [
            "yt-dlp",
            "-f", fmt,
            "--no-playlist",
            "--no-warnings",
            "-o", "-",
            url,
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=1024 * 64,
        )
        try:
            while True:
                chunk = proc.stdout.read(64 * 1024)
                if not chunk:
                    break
                yield chunk
        finally:
            proc.stdout.close()
            proc.wait()

    return StreamingResponse(
        generate(),
        media_type="video/mp4",
        headers={
            "Content-Disposition": 'attachment; filename="video.mp4"',
            "Cache-Control": "no-cache",
        },
    )


@app.post("/api/download")
def api_download(
    url: str = Form(...),
    quality: str = Form("best"),
    audio_only: bool = Form(False),
):
    job_id = uuid.uuid4().hex[:8]
    JOBS[job_id] = {
        "status": "queued",
        "progress": 0,
        "path": None,
        "filename": None,
        "filesize": None,
        "error": None,
    }

    def run():
        def hook(d):
            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes") or 0
                total = (d.get("total_bytes")
                         or d.get("total_bytes_estimate")
                         or 0)
                if total > 0:
                    pct = (downloaded / total) * 100
                else:
                    pct_str = d.get("_percent_str", "0%").strip().replace("%", "")
                    try:
                        pct = float(pct_str)
                    except ValueError:
                        pct = 0
                JOBS[job_id]["progress"] = min(pct, 100)
                JOBS[job_id]["status"] = "downloading"
            elif d["status"] == "finished":
                JOBS[job_id]["status"] = "processing"
                JOBS[job_id]["progress"] = 100

        try:
            JOBS[job_id]["status"] = "starting"
            path = download(
                url=url,
                quality=quality,
                audio_only=audio_only,
                progress_hook=hook,
            )
            p = Path(path)
            JOBS[job_id]["status"] = "done"
            JOBS[job_id]["path"] = str(p)
            JOBS[job_id]["filename"] = p.name
            JOBS[job_id]["filesize"] = p.stat().st_size if p.exists() else None
        except AlreadyDownloadedError as e:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["error"] = "Video sudah pernah didownload. Hapus .vdl-archive.txt kalau mau ulang."
        except VDLError as e:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["error"] = str(e)
            print(f"[job {job_id}] VDLError: {e}")
        except Exception as e:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["error"] = f"Unexpected: {e}"
            print(f"[job {job_id}] Unexpected: {e}")

    threading.Thread(target=run, daemon=True).start()
    return {"ok": True, "job_id": job_id}


@app.get("/api/job/{job_id}")
def api_job(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        return JSONResponse({"ok": False, "error": "Job not found"}, status_code=404)
    if job.get("filesize"):
        job["filesize_str"] = _human_size(job["filesize"])
    return {"ok": True, **job}


@app.get("/api/file/{job_id}")
def api_file(job_id: str, keep: bool = False):
    """
    Serve file untuk didownload dari device user.
    Setelah selesai, file di laptop otomatis dihapus (kecuali ?keep=1).
    """
    job = JOBS.get(job_id)
    if not job:
        return JSONResponse({"ok": False, "error": "Job not found"}, status_code=404)
    if job["status"] != "done":
        return JSONResponse({"ok": False, "error": "File belum siap"}, status_code=400)
    if not job.get("path") or job["path"].startswith("("):
        return JSONResponse({"ok": False, "error": "File tidak tersedia"}, status_code=404)

    path = Path(job["path"])
    if not path.exists():
        return JSONResponse({"ok": False, "error": "File tidak ditemukan"}, status_code=404)

    background = None
    if not keep:
        def cleanup():
            try:
                path.unlink()
                print(f"[cleanup] Deleted: {path.name}")
                JOBS[job_id]["path"] = "(deleted)"
            except Exception as e:
                print(f"[cleanup] Failed: {e}")
        background = BackgroundTask(cleanup)

    return FileResponse(
        path,
        filename=path.name,
        media_type="application/octet-stream",
        background=background,
    )


def run():
    import uvicorn
    uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=True)

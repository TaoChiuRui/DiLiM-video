"""
broll_cataloger.py
Danh muc noi dung thu vien B-roll cho DiLiM AI Editor.

MUC TIEU: sinh mo ta noi dung THAT cua tung clip B-roll (khong chi dua vao ten
thu muc/chu de), de buoc so khop B-roll <-> loi thoai A-roll sau nay chinh xac
hon so voi chi so khop theo tu khoa chu de nhu he thong cu.

Day CHI la buoc danh danh muc (offline, chay 1 lan / tang dan khi co clip moi).
Buoc so khop voi transcript thuc te khi dung video la mot script rieng, chay sau.

Cach chay:
    pip install anthropic
    # Windows:  set ANTHROPIC_API_KEY=sk-ant-...
    # Mac/Linux: export ANTHROPIC_API_KEY=sk-ant-...

    # Chay thu 5 clip dau tien de kiem tra chat luong mo ta truoc:
    python broll_cataloger.py --input "D:\\Broll_Catalog_Test" --output catalog.json --limit 5

    # Chay full sau khi thay ket qua on:
    python broll_cataloger.py --input "D:\\Broll_Catalog_Test" --output catalog.json

Yeu cau: da cai ffmpeg + ffprobe va co trong PATH (dung de trich khung hinh).
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import anthropic

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v"}
DEFAULT_MODEL = "claude-sonnet-5"
FRAME_COUNT_DEFAULT = 6

# Prompt duoc thiet ke rieng cho muc tieu: tang do chinh xac khi chon B-roll
# theo LOI NOI cua A-roll. Vi vay khong chi xin "mo ta chung", ma xin cac
# cum tu/cau loi thoai mau ma clip nay phu hop minh hoa - de buoc so khop
# sau nay co thu cu the de doi chieu voi transcript that.
PROMPT_TEMPLATE = """Ban dang xem {n} khung hinh trich ra tu mot clip B-roll (video minh hoa, khong loi) theo thu tu thoi gian tu dau den cuoi clip. Clip nay dang nam trong thu muc chu de "{topic}" cua thu vien B-roll cho video quang cao suc khoe / thuc pham chuc nang.

MUC TIEU QUAN TRONG: mo ta phai du chi tiet de phan biet duoc clip nay voi CAC CLIP KHAC trong CUNG thu muc chu de "{topic}" - khong duoc chi lap lai ten chu de mot cach chung chung. Neu ban chi viet duoc mot cau kieu "mot nguoi dang {topic}" thi coi nhu chua dat yeu cau.

Tra loi CHI BANG JSON dung dinh dang sau, khong them chu nao khac ngoai JSON, khong bao trong dau ``` :
{{
  "description": "1-2 cau mo ta cu the: ai/cai gi xuat hien, dang lam gi (hanh dong cu the, khong chung chung), boi canh/khong gian cu the.",
  "shot_type": "can canh | trung canh | toan canh | goc rong | khong ro",
  "subjects": ["danh sach ngan cac doi tuong/nhan vat xuat hien"],
  "action": "hanh dong chinh dang dien ra, cang cu the cang tot",
  "mood": "cam giac/tong cua canh, vi du: cang thang, thu gian, vui ve, trang nghiem, am ap",
  "possible_narration_phrases": ["2 den 4 cum tu hoac cau noi mau bang tieng Viet ma clip nay PHU HOP de minh hoa, neu nguoi dan chuong trinh noi toi dieu do"],
  "confidence": "cao | trung binh | thap (muc tu tin cua ban khi mo ta, de thap neu khung hinh khong ro rang / qua toi / qua mo / kho xac dinh)"
}}"""


def get_duration(video_path: Path) -> Optional[float]:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path),
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(out.stdout.strip())
    except Exception:
        return None


def extract_frames(video_path: Path, n: int, tmp_dir: Path) -> list[Path]:
    """Trich n khung hinh cach deu nhau trong clip (tranh lay dung khung dau/cuoi
    vi thuong den hoac mo). Tra ve danh sach duong dan anh da trich."""
    duration = get_duration(video_path)
    if not duration or duration <= 0:
        return []
    tmp_dir.mkdir(parents=True, exist_ok=True)
    frame_paths: list[Path] = []
    for i in range(n):
        t = duration * (i + 1) / (n + 1)
        out_path = tmp_dir / f"{video_path.stem}_f{i}.jpg"
        cmd = [
            "ffmpeg", "-y", "-ss", str(t), "-i", str(video_path),
            "-frames:v", "1", "-q:v", "2", str(out_path),
        ]
        subprocess.run(cmd, capture_output=True)
        if out_path.exists():
            frame_paths.append(out_path)
    return frame_paths


def encode_image(path: Path) -> dict:
    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}


def clean_json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()
    return text


def describe_clip(client: anthropic.Anthropic, frame_paths: list[Path], topic: str, model: str) -> dict:
    content = [encode_image(p) for p in frame_paths]
    content.append({"type": "text", "text": PROMPT_TEMPLATE.format(n=len(frame_paths), topic=topic)})
    resp = client.messages.create(
        model=model,
        max_tokens=700,
        messages=[{"role": "user", "content": content}],
    )
    text = "".join(block.text for block in resp.content if block.type == "text")
    try:
        return json.loads(clean_json_text(text))
    except json.JSONDecodeError:
        return {"description": text.strip(), "parse_error": True}


def load_catalog(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_catalog(catalog: dict, path: Path) -> None:
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Danh danh muc noi dung thu vien B-roll bang Claude vision.")
    ap.add_argument("--input", required=True, help="Thu muc goc chua B-roll (co the co thu muc con theo chu de)")
    ap.add_argument("--output", default="broll_catalog.json", help="File JSON catalog dau ra")
    ap.add_argument("--frames", type=int, default=FRAME_COUNT_DEFAULT, help="So khung hinh trich moi clip (mac dinh 6)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Model dung de mo ta (mac dinh claude-sonnet-5; doi sang claude-haiku-4-5-20251001 de tiet kiem chi phi khi chay full thu vien)")
    ap.add_argument("--tmp-dir", default="._frames_tmp", help="Thu muc tam de luu khung hinh trich ra")
    ap.add_argument("--limit", type=int, default=None, help="Chi chay thu N clip dau (dung de kiem tra truoc khi chay full)")
    ap.add_argument("--save-every", type=int, default=10, help="Luu tam catalog sau moi bao nhieu clip")
    args = ap.parse_args()

    input_dir = Path(args.input)
    output_path = Path(args.output)
    tmp_dir = Path(args.tmp_dir)

    if not input_dir.exists():
        print(f"Khong tim thay thu muc: {input_dir}")
        sys.exit(1)

    client = anthropic.Anthropic()  # doc ANTHROPIC_API_KEY tu bien moi truong

    catalog = load_catalog(output_path)

    video_files = sorted(p for p in input_dir.rglob("*") if p.suffix.lower() in VIDEO_EXTS)
    if args.limit:
        video_files = video_files[: args.limit]

    print(f"Tim thay {len(video_files)} clip. Da co {len(catalog)} clip trong catalog hien tai.")

    processed_this_run = 0
    for idx, video_path in enumerate(video_files, 1):
        key = str(video_path.resolve())
        if key in catalog and not catalog[key].get("parse_error") and not catalog[key].get("error"):
            continue  # da xu ly roi, bo qua (resumable)

        topic = video_path.parent.name  # ten thu muc cha = chu de hien co
        print(f"[{idx}/{len(video_files)}] {video_path.name} (chu de: {topic}) ...", end=" ", flush=True)

        try:
            frames = extract_frames(video_path, args.frames, tmp_dir)
            if not frames:
                print("BO QUA (khong trich duoc khung hinh)")
                catalog[key] = {"topic": topic, "error": "no_frames"}
                continue

            result = describe_clip(client, frames, topic, args.model)
            result["topic"] = topic
            result["path"] = key
            result["frame_count"] = len(frames)
            catalog[key] = result
            processed_this_run += 1
            print("xong" if not result.get("parse_error") else "xong (JSON loi, luu raw text)")

        except Exception as e:
            print(f"LOI: {e}")
            catalog[key] = {"topic": topic, "error": str(e)}

        finally:
            for f in tmp_dir.glob(f"{video_path.stem}_f*.jpg"):
                f.unlink(missing_ok=True)
            if processed_this_run and processed_this_run % args.save_every == 0:
                save_catalog(catalog, output_path)
                print(f"  (da luu tam sau {processed_this_run} clip xu ly trong lan chay nay)")
            time.sleep(0.5)  # tranh don request qua nhanh

    save_catalog(catalog, output_path)
    print(f"\nHoan tat. Catalog luu tai: {output_path.resolve()}")
    print(f"Tong so clip trong catalog: {len(catalog)}")


if __name__ == "__main__":
    main()

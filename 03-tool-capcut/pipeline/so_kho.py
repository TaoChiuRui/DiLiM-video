# -*- coding: utf-8 -*-
"""SO KHO — bang HTML doc duoc cua moi clip DA KHAI trong clips.py.

    python3 so_kho.py                 # -> 05-footage-moi/so_kho.html
    python3 so_kho.py --moi           # chi clip CHUA co tu khoa

VI SAO CO FILE NAY: ten file chi mo ta ngan (`daudau-ongcu-omtran-01.mp4`),
con TU KHOA / MOC GIAY / HO CHONG LAP deu nam trong clips.py — tuc la trong
code. Anh Thanh khong co ly do gi phai doc Python de biet kho co gi.

Bang nay cho SUA TU KHOA ngay tren trinh duyet, bam «TAI JSON VE» roi:
    python3 nap_tu_khoa.py --file ~/Downloads/tu_khoa.json --apply

DUNG `Read` FILE HTML SINH RA — no chua anh base64, doc la no context.
"""
import argparse
import base64
import html
import io
import json
import os
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "05-footage-moi", "so_kho.html")
THUMB_W = 300


def N(s):
    return unicodedata.normalize("NFC", s)


def dur(p):
    if p.lower().endswith(C.IMG_EXT):
        return 0.0
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def thumb(p, ss):
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if not p.lower().endswith(C.IMG_EXT):
        cmd += ["-ss", str(ss)]
    cmd += ["-i", p, "-frames:v", "1", "-vf", f"scale={THUMB_W}:-1",
            "-f", "image2", "-c:v", "mjpeg", "-q:v", "6", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode or not r.stdout:
        return ""
    return base64.b64encode(r.stdout).decode()


def used_counts():
    cnt = {}
    du_an = os.path.join(ROOT, "04-du-an")
    if not os.path.isdir(du_an):
        return cnt
    for job in os.listdir(du_an):
        for rel in ("plan.py", "edit/plan.json"):
            f = os.path.join(du_an, job, rel)
            if not os.path.isfile(f):
                continue
            for chunk in open(f, encoding="utf-8").read().split('"')[1::2]:
                if chunk.startswith("/Volumes/T7"):
                    k = N(chunk)
                    cnt[k] = cnt.get(k, 0) + 1
    return cnt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--moi", action="store_true", help="chi clip chua co tu khoa")
    a = ap.parse_args()

    use = used_counts()
    ho = {}
    for ten, ds in C.FAMILIES.items():
        for p in ds:
            ho.setdefault(N(p), []).append(ten)

    rows = []
    for k, v in sorted(vars(C).items()):
        if not (k.isupper() and isinstance(v, str) and v.startswith("/Volumes")):
            continue
        if not os.path.isfile(v):           # bo hang so thu muc (B, MM, DD)
            continue
        tags = C.TAGS.get(v, [])
        if a.moi and tags:
            continue
        ss = C.MIN_START.get(v, 0.0)
        d = dur(v)
        rows.append(dict(
            const=k, path=v, name=os.path.basename(v), dur=d,
            ss=ss, tags=tags, ho=ho.get(N(v), []),
            use=use.get(N(v), 0),
            doc=v in C.VERTICAL,
            folder=os.path.basename(os.path.dirname(v)),
            img=thumb(v, ss if ss else min(2.0, d * 0.25)),
        ))

    rows.sort(key=lambda r: (-r["use"], r["folder"], r["name"]))
    cards = []
    for r in rows:
        tags = ", ".join(r["tags"])
        badge = []
        if r["use"]:
            badge.append(f'<b class="u">đã dùng {r["use"]}×</b>')
        if not r["tags"]:
            badge.append('<b class="w">CHƯA CÓ TỪ KHOÁ</b>')
        if r["doc"]:
            badge.append('<b class="v">DỌC — không dùng cho dải</b>')
        if r["ss"]:
            badge.append(f'<b class="s">bắt đầu từ {r["ss"]}s</b>')
        ds = "ảnh" if r["dur"] == 0 else f'{r["dur"]:.1f}s'
        cards.append(f"""
<div class="c" data-t="{html.escape((r['const']+' '+r['name']+' '+tags+' '+r['folder']).lower())}">
 <img src="data:image/jpeg;base64,{r['img']}">
 <div class="m">
  <div class="h"><span class="k">{html.escape(r['const'])}</span>
   <span class="d">{ds}</span> {' '.join(badge)}</div>
  <div class="f">{html.escape(r['folder'])} / {html.escape(r['name'])}</div>
  <div class="ho">{' '.join('<i>'+html.escape(x)+'</i>' for x in r['ho']) or '<i class="no">chưa vào hồ nào</i>'}</div>
  <textarea data-k="{html.escape(r['const'])}"
    placeholder="từ khoá tiếng Việt, cách nhau bởi dấu phẩy">{html.escape(tags)}</textarea>
 </div>
</div>""")

    n_tag = sum(1 for r in rows if r["tags"])
    doc = f"""<!doctype html><meta charset="utf-8">
<title>Sổ kho B-roll DiLiM</title>
<style>
*{{box-sizing:border-box}}
body{{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
 margin:0;background:#12141a;color:#e8e8ea}}
header{{position:sticky;top:0;background:#12141aee;backdrop-filter:blur(8px);
 padding:14px 20px;border-bottom:1px solid #2a2e38;z-index:9}}
h1{{margin:0 0 8px;font-size:19px}}
.sub{{color:#98a0ae;font-size:13px}}
input#q{{width:100%;max-width:520px;margin-top:10px;padding:9px 12px;font-size:15px;
 border-radius:8px;border:1px solid #333947;background:#1b1f28;color:#e8e8ea}}
button{{padding:9px 16px;font-size:14px;border-radius:8px;border:0;
 background:#3d7bfd;color:#fff;cursor:pointer;margin-left:8px}}
main{{padding:16px 20px;display:grid;gap:12px}}
.c{{display:flex;gap:14px;background:#191d25;border:1px solid #262b36;
 border-radius:10px;padding:12px}}
.c img{{width:300px;height:auto;border-radius:6px;flex:none;align-self:flex-start}}
.m{{flex:1;min-width:0}}
.h{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px}}
.k{{font-weight:700;font-size:16px;color:#8fc6ff;font-family:ui-monospace,monospace}}
.d{{color:#98a0ae;font-size:13px}}
.f{{color:#7b8493;font-size:12.5px;margin-bottom:7px;word-break:break-all}}
.ho i{{display:inline-block;background:#26303f;color:#9fc0e8;border-radius:5px;
 padding:2px 8px;font-style:normal;font-size:12px;margin:0 5px 5px 0}}
.ho i.no{{background:none;color:#5c6472;padding-left:0}}
textarea{{width:100%;min-height:52px;padding:8px 10px;border-radius:7px;
 border:1px solid #333947;background:#11141b;color:#e8e8ea;font:14px inherit;resize:vertical}}
textarea:focus{{outline:0;border-color:#3d7bfd}}
b{{font-size:11.5px;padding:2px 8px;border-radius:20px;font-weight:600}}
b.u{{background:#1d4429;color:#8fe0a6}} b.w{{background:#4d2020;color:#ff9d9d}}
b.v{{background:#4a3a12;color:#f3cd72}} b.s{{background:#2b2f57;color:#a9b3ff}}
</style>
<header>
 <h1>Sổ kho B-roll DiLiM — {len(rows)} clip đã khai</h1>
 <div class="sub">{n_tag} clip có từ khoá · {len(rows)-n_tag} clip chưa ·
  sửa từ khoá ngay trong ô, xong bấm nút để tải về</div>
 <input id="q" placeholder="lọc: gõ tên clip, từ khoá, hoặc tên thư mục…">
 <button onclick="tai()">TẢI JSON VỀ</button>
</header>
<main id="m">{''.join(cards)}</main>
<script>
q.oninput=()=>{{const v=q.value.toLowerCase().trim();
 document.querySelectorAll('.c').forEach(c=>
  c.style.display=!v||c.dataset.t.includes(v)?'flex':'none')}};
function tai(){{const o={{}};
 document.querySelectorAll('textarea').forEach(t=>{{
  const a=t.value.split(',').map(s=>s.trim()).filter(Boolean);
  if(a.length)o[t.dataset.k]=a;}});
 const b=new Blob([JSON.stringify(o,null,1)],{{type:'application/json'}});
 const a=document.createElement('a');a.href=URL.createObjectURL(b);
 a.download='tu_khoa.json';a.click();}}
</script>"""

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(doc)
    print(f"{len(rows)} clip ({n_tag} co tu khoa, {len(rows)-n_tag} chua)")
    print(f"-> {os.path.relpath(OUT, ROOT)}  ({os.path.getsize(OUT)/1024:.0f} KB)")


if __name__ == "__main__":
    main()

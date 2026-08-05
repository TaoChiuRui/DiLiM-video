# -*- coding: utf-8 -*-
"""BUOC 4 — Bang duyet GOP (Tinh Media): caption + mau + B-roll + SFX + ghi chu
trong 1 bang HTML duy nhat. Anh preview trich DUNG giay se render.

    python 4_make_table.py v1 "Tieu de video" bang_v1.html
"""
import base64, html, io, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import BROLL_ROOT  # noqa: E402
from PIL import Image  # noqa: E402

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
TITLE = sys.argv[2]
OUTF = sys.argv[3]
rows = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))
segs = json.load(open(os.path.join(HERE, "segments.json"), encoding="utf-8"))
B = str(BROLL_ROOT)
BUBBLES = []

SFX = ["", "Whoosh 05.wav", "Whoosh 04.wav", "Whoosh 01.wav", "Whoosh 06.wav",
       "SWOOSH - DRAMATIC.mp3", "killpop.mp3", "ding-sound-effect_1.mp3",
       "bell-ding-resonate-SBA-300156894.wav", "mouse-click_gt1reD8.mp3", "Paper - mid.wav"]
SFX_LABEL = {"": "— không —", "Whoosh 05.wav": "Whoosh 05 · chữ vào (0.48s)",
             "Whoosh 04.wav": "Whoosh 04 · chữ vào, dày hơn", "Whoosh 01.wav": "Whoosh 01 · chuyển cảnh",
             "Whoosh 06.wav": "Whoosh 06 · chuyển cảnh dài", "SWOOSH - DRAMATIC.mp3": "Swoosh kịch tính · nhấn mạnh",
             "killpop.mp3": "Pop · điểm nhấn ngắn", "ding-sound-effect_1.mp3": "Ding · chốt ý",
             "bell-ding-resonate-SBA-300156894.wav": "Bell ding · chốt ý ngân",
             "mouse-click_gt1reD8.mp3": "Click · CTA", "Paper - mid.wav": "Paper · lật trang"}
VARIANTS = [("warning", "Đỏ — ý tiêu cực"), ("positive", "Xanh — ý tích cực"),
            ("product", "Trắng/vàng — sản phẩm"), ("cta", "CTA — kết video"),
            ("yellow", "Vàng"), ("highlight", "Nhấn")]


def say(t0, t1):
    out = [s["text"] for s in segs if s["end"] > t0 + 0.15 and s["start"] < t1 - 0.15]
    return " ".join(out).strip()


def thumb(path, ss):
    try:
        if path == "MULTI_BUBBLE":
            ims = []
            for b in BUBBLES:
                r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "6", "-i", b, "-frames:v", "1",
                                    "-vf", "crop=760:760:160:320,scale=104:104", "-f", "image2pipe",
                                    "-vcodec", "png", "-"], capture_output=True)
                if r.stdout:
                    ims.append(Image.open(io.BytesIO(r.stdout)).convert("RGB"))
            if not ims:
                return ""
            c = Image.new("RGB", (104 * len(ims), 104), (0, 0, 0))
            for k, im in enumerate(ims):
                c.paste(im, (k * 104, 0))
            im = c
        else:
            cmd = ["ffmpeg", "-v", "error"]
            if not path.lower().endswith((".jpg", ".jpeg", ".png")):
                cmd += ["-ss", f"{ss:.2f}"]
            cmd += ["-i", path, "-frames:v", "1", "-vf", "scale=320:-2",
                    "-f", "image2pipe", "-vcodec", "png", "-"]
            r = subprocess.run(cmd, capture_output=True)
            if not r.stdout:
                return ""
            im = Image.open(io.BytesIO(r.stdout)).convert("RGB")
            im.thumbnail((320, 180))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=72)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        print("thumb loi", path, e)
        return ""


TR = []
for r in rows:
    p = r["path"]
    img = thumb(p, r["src_start"]) if p else ""
    name = "3 bubble thành phần" if p == "MULTI_BUBBLE" else (os.path.basename(p) if p else "")
    folder = ""
    if p and p != "MULTI_BUBBLE":
        parts = p.replace("/", "\\").split("\\")
        try:
            folder = parts[parts.index("Footage B-roll") + 1]
        except ValueError:
            folder = ""
    opts_v = "".join(
        f'<option value="{v}"{" selected" if v == r["variant"] else ""}>{html.escape(lab)}</option>'
        for v, lab in VARIANTS)
    opts_s = "".join(f'<option value="{html.escape(s)}">{html.escape(SFX_LABEL[s])}</option>' for s in SFX)
    TR.append(f"""<tr data-idx="{r['idx']}">
 <td class="n">{r['idx']}<div class="t">{r['t']:.2f}<br>↓<br>{r['t_end']:.2f}</div></td>
 <td class="say">{html.escape(say(r['t'], r['t_end']))}</td>
 <td><div class="cap" contenteditable data-f="d1">{html.escape(r['d1'])}</div>
     <div class="cap l2" contenteditable data-f="d2">{html.escape(r['d2'])}</div>
     <select data-f="variant" class="var {r['variant']}">{opts_v}</select></td>
 <td class="pv">{f'<img src="{img}">' if img else '<div class="none">— không có B-roll —</div>'}
     <div class="fn">{html.escape(folder)}{' › ' if folder else ''}{html.escape(name)}</div></td>
 <td><div class="path" contenteditable data-f="path">{html.escape(p if p != 'MULTI_BUBBLE' else '')}</div></td>
 <td><select data-f="sfx">{opts_s}</select></td>
 <td><div class="note" contenteditable data-f="note">{html.escape(r['note'])}</div></td>
</tr>""")

HTML = """<!doctype html><meta charset="utf-8"><title>Duyệt — __TITLE__</title>
<style>
*{box-sizing:border-box}
body{font:14px/1.45 "Segoe UI",system-ui,sans-serif;margin:0;background:#12141a;color:#e8eaf0}
header{position:sticky;top:0;z-index:9;background:#1b1e26;border-bottom:1px solid #2c3140;padding:12px 18px}
h1{margin:0 0 4px;font-size:17px}
.sub{font-size:12px;color:#98a0b3}
.bar{margin-top:9px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
button{background:#2f6df6;border:0;color:#fff;padding:7px 14px;border-radius:6px;cursor:pointer;font-size:13px}
button.g{background:#2a2f3d}
#st{font-size:12px;color:#7fd88f}
table{border-collapse:collapse;width:100%}
th{background:#1b1e26;position:sticky;top:96px;z-index:8;font-size:11px;text-transform:uppercase;
   letter-spacing:.5px;color:#98a0b3;padding:8px 9px;text-align:left;border-bottom:1px solid #2c3140}
td{border-bottom:1px solid #232733;padding:9px;vertical-align:top}
tr:hover{background:#171a22}
.n{width:52px;color:#7d879c;font-size:12px;text-align:center}
.t{font-size:10px;color:#5e6779;margin-top:3px;line-height:1.25}
.say{width:20%;font-size:12.5px;color:#98a0b3;font-style:italic}
.cap{background:#0d0f14;border:1px solid #2c3140;border-radius:5px;padding:6px 8px;
     font-weight:600;letter-spacing:.3px;min-height:30px;min-width:190px}
.cap:focus{outline:2px solid #2f6df6;background:#0a0c10}
.l2{margin-top:4px;opacity:.9}
.var{margin-top:5px;width:100%;background:#0d0f14;color:#e8eaf0;border:1px solid #2c3140;
     border-radius:5px;padding:4px;font-size:12px}
.var.warning{border-color:#d62828;color:#ff8a8a}
.var.positive{border-color:#157a3f;color:#7fd88f}
.var.product{border-color:#b8860b;color:#e8c05a}
.var.cta{border-color:#2f6df6;color:#8fb4ff}
.pv{width:340px}
.pv img{width:320px;border-radius:5px;display:block;background:#000}
.none{width:320px;height:96px;border:1px dashed #333a4a;border-radius:5px;color:#5e6779;
      display:flex;align-items:center;justify-content:center;font-size:12px}
.fn{font-size:10.5px;color:#6b7488;margin-top:4px;word-break:break-all;max-width:320px}
.path,.note{background:#0d0f14;border:1px solid #2c3140;border-radius:5px;padding:6px 8px;
     font-size:11px;min-height:30px;word-break:break-all}
.path{min-width:200px;color:#8fb4ff}
.note{min-width:150px;color:#d9c98f}
select[data-f=sfx]{background:#0d0f14;color:#e8eaf0;border:1px solid #2c3140;border-radius:5px;
     padding:5px;font-size:11.5px;max-width:180px}
</style>
<header>
<h1>__TITLE__ — bảng duyệt</h1>
<div class="sub">Sụn Nano Premium + Gluchongel · giọng văn A · __N__ caption, __NB__ có B-roll (__PC__%)
 &nbsp;|&nbsp; Sửa trực tiếp vào ô. Để trống <b>cả 2 dòng chữ</b> = bỏ caption. Dán đường dẫn khác vào ô B-roll để đổi clip.</div>
<div class="bar"><button onclick="dl()">⬇ Tải quyết định (JSON)</button>
<button class="g" onclick="if(confirm('Xoá hết chỉnh sửa đã lưu?')){localStorage.removeItem(K);location.reload()}">Đặt lại</button>
<span id="st"></span></div>
</header>
<table><thead><tr><th>#</th><th>Lời thoại gốc</th><th>Chữ hiện trên video + màu</th>
<th>B-roll (ảnh đúng khung sẽ render)</th><th>Đổi B-roll — dán đường dẫn</th><th>Sound effect</th><th>Ghi chú</th>
</tr></thead><tbody>
__ROWS__
</tbody></table>
<script>
const K='__KEY__';
function cells(){return document.querySelectorAll('[data-f]')}
function save(){const o={};cells().forEach(e=>{const tr=e.closest('tr');
 o[tr.dataset.idx+'|'+e.dataset.f]=(e.tagName=='SELECT'?e.value:e.innerText.trim())});
 localStorage.setItem(K,JSON.stringify(o));
 document.getElementById('st').textContent='đã lưu '+new Date().toLocaleTimeString('vi-VN');}
function load(){const s=localStorage.getItem(K);if(!s)return;const o=JSON.parse(s);
 cells().forEach(e=>{const k=e.closest('tr').dataset.idx+'|'+e.dataset.f;
  if(k in o){if(e.tagName=='SELECT')e.value=o[k];else e.innerText=o[k];}});
 document.querySelectorAll('.var').forEach(s=>s.className='var '+s.value);
 document.getElementById('st').textContent='đã khôi phục bản sửa trước';}
cells().forEach(e=>{e.addEventListener('input',save);e.addEventListener('change',e2=>{
 if(e.classList.contains('var'))e.className='var '+e.value;save();});});
load();
function dl(){const out=[];document.querySelectorAll('tbody tr').forEach(tr=>{
 const g=f=>{const e=tr.querySelector('[data-f='+f+']');return e?(e.tagName=='SELECT'?e.value:e.innerText.trim()):''};
 out.push({idx:+tr.dataset.idx,d1:g('d1'),d2:g('d2'),variant:g('variant'),
           path:g('path'),sfx:g('sfx'),note:g('note')});});
 const b=new Blob([JSON.stringify(out,null,1)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(b);
 a.download='__KEY__-da-sua.json';a.click();}
</script>"""

nb = sum(1 for r in rows if r["path"])
HTML = (HTML.replace("__ROWS__", "\n".join(TR)).replace("__N__", str(len(rows)))
            .replace("__NB__", str(nb)).replace("__PC__", str(round(nb / len(rows) * 100)))
            .replace("__TITLE__", TITLE).replace("__KEY__", "raydel_" + os.path.basename(HERE) + "_v2026073115"))
out = OUTF
open(out, "w", encoding="utf-8").write(HTML)
print(out, f"{os.path.getsize(out)/1048576:.1f} MB")

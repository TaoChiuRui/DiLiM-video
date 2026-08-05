# -*- coding: utf-8 -*-
"""Bang duyet GOP — caption + B-roll + doi chieu timestamp.

    python3 make_table.py

Ra edit/bang_duyet.html — mo bang trinh duyet, sua truc tiep, bam
"TAI JSON VE" roi gui lai file do.

Moi dong co 3 anh:
  - FRAME GOC  : frame cua video A-roll tai DUNG giay caption bat dau
                 -> de kiem timestamp co khop loi noi khong
  - B-ROLL     : frame cua clip B-roll tai DUNG giay se dung
  - (neu trong): o nhap path de nguoi dung tu gan
"""
import base64, html, io, json, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import argparse as _ap
import sys as _sys

def _job_dir():
    """Thu muc job — truyen bang --job. Moi script trong pipeline nay deu
    dung chung, khong con chep sang tung job nua."""
    _p = _ap.ArgumentParser(add_help=False)
    _p.add_argument("--job", help="duong dan (04-du-an/<ten>) HOAC ten job")
    _a, _ = _p.parse_known_args()
    if "--help" in _sys.argv or "-h" in _sys.argv:
        print(__doc__ or "");  raise SystemExit(0)
    import job_path                      # giai ca 3 dang, xem job_path.py
    return job_path.job_dir(_a.job)


HERE = _job_dir()
PIPE = os.path.dirname(os.path.abspath(__file__))
SRC = next((p for p in (os.path.join(HERE, "edit/final.mp4"),
                        os.path.join(HERE, "source.mp4"),
                        os.path.join(HERE, "source.MOV")) if os.path.exists(p)), "")
ROWS = json.load(open(os.path.join(HERE, "edit/plan.json"), encoding="utf-8"))
IMG_EXT = (".jpg", ".jpeg", ".png", ".JPG", ".PNG")

VARIANTS = {
    "warning":  ("Đỏ — ý tiêu cực",      "#D62828", "#FFFFFF", "#FFEA00"),
    "positive": ("Xanh — ý tích cực",    "#FFFFFF", "#157A3F", "#D62828"),
    "product":  ("Trắng — sản phẩm",     "#FFFFFF", "#157A3F", "#B8860B"),
    "cta":      ("CTA — kết video",      "#157A3F", "#FFFFFF", "#FFEA00"),
    "yellow":   ("Vàng",                 "#FFF000", "#000000", "#D62828"),
    "highlight":("Nhấn",                 "#FFFFFF", "#D62828", "#000000"),
}


def thumb(path, ss, w=150):
    """1 frame tai giay ss, tra ve data-uri base64. '' neu that bai."""
    if not path or not os.path.exists(path):
        return ""
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if not path.endswith(IMG_EXT):
        cmd += ["-ss", str(ss)]
    cmd += ["-i", path, "-frames:v", "1", "-vf", f"scale={w}:-1",
            "-f", "image2", "-c:v", "mjpeg", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode or not r.stdout:
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(r.stdout).decode()


def caption_preview(d1, d2, variant):
    """Ve lai caption bang HTML theo dung mau cua caption_style.py bo Tinh."""
    _, bg, fg, kw = VARIANTS.get(variant, VARIANTS["warning"])
    out = []
    for line in (d1, d2):
        if not line:
            continue
        parts, bold = line.split("*"), False
        spans = []
        for p in parts:
            if p:
                col = kw if bold else fg
                spans.append(f'<span style="color:{col}">{html.escape(p)}</span>')
            bold = not bold
        out.append(f'<div class="capline" style="background:{bg}">{"".join(spans)}</div>')
    return "".join(out)


def main():
    print(f"trich {len(ROWS)} frame goc + {sum(1 for r in ROWS if r['path'])} frame B-roll ...")
    body = []
    for r in ROWS:
        src_img = thumb(SRC, r["t"], w=68)   # A-roll doc 9:16 -> de nho keo dong xuong
        bimg = thumb(r["path"], r["src_start"]) if r["path"] else ""
        vlabel = VARIANTS.get(r["variant"], ("?",))[0]
        blank = "" if r["path"] else " blank"
        bcell = (f'<img src="{bimg}">' if bimg else
                 '<div class="noclip">CHƯA CÓ CLIP</div>')
        body.append(f"""
<tr class="row{blank}" data-idx="{r['idx']}">
  <td class="num">{r['idx']}</td>
  <td class="time">
      <input class="tt" data-f="t" value="{r['t']:.2f}">
      <input class="tt" data-f="t_end" value="{r['t_end']:.2f}">
      <div class="dur">{r['t_end']-r['t']:.2f}s</div>
      <div class="orig" data-t0="{r['t']:.2f}" data-t1="{r['t_end']:.2f}">gốc {r['t']:.2f}→{r['t_end']:.2f}</div>
      <div class="nudge">
        <button class="nb" onclick="nudge(this,-0.30)">−.30</button><button class="nb" onclick="nudge(this,-0.15)">−.15</button>
        <button class="nb" onclick="nudge(this,0.15)">+.15</button><button class="nb" onclick="nudge(this,0.30)">+.30</button>
      </div></td>
  <td class="said">{html.escape(r['said'])}
      <div class="anchor">neo: <b>{html.escape(str(r.get('anchor_word','—')))}</b>
      · nói lúc {r['t']+0.5:.2f}s</div></td>
  <td class="cap">{caption_preview(r['d1'], r['d2'], r['variant'])}
      <div class="vsel"><select data-f="variant">""" +
      "".join(f'<option value="{k}"{" selected" if k==r["variant"] else ""}>{v[0]}</option>'
              for k, v in VARIANTS.items()) + f"""</select></div>
      <textarea data-f="d1" rows="2">{html.escape(r['d1'])}</textarea>
      <textarea data-f="d2" rows="2">{html.escape(r['d2'])}</textarea></td>
  <td class="src">{'<img src="'+src_img+'">' if src_img else ''}</td>
  <td class="broll">{bcell}
      <input data-f="path" value="{html.escape(r['path'])}" placeholder="dán path clip vào đây">
      <label>bắt đầu từ giây <input class="ss" data-f="src_start" value="{r['src_start']}"></label></td>
  <td class="note"><textarea data-f="note" rows="2">{html.escape(r['note'])}</textarea>
      <div class="why-lbl">VÌ SAO đổi? (để tôi học)</div>
      <textarea data-f="vi_sao" rows="3" class="why"
        placeholder="vd: chỗ nói tên sản phẩm thì luôn dùng hộp trên cỏ, đừng dùng tờ thông số"></textarea></td>
</tr>""")

    doc = """<!doctype html><meta charset="utf-8">
<title>Bảng duyệt — Dilim Video test</title>
<style>
*{box-sizing:border-box}
body{font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
     margin:0;padding:20px;background:#14161a;color:#e6e6e6}
h1{font-size:19px;margin:0 0 4px}
.sub{color:#9aa0a6;margin-bottom:16px;font-size:13px}
.bar{position:sticky;top:0;z-index:9;background:#14161a;padding:10px 0 12px;
     border-bottom:1px solid #2a2f36;margin-bottom:12px}
button{background:#157A3F;color:#fff;border:0;padding:9px 18px;border-radius:6px;
       font-size:14px;font-weight:600;cursor:pointer}
button:hover{background:#1a9950}
.grp{margin-left:18px;color:#9aa0a6;font-size:12px}
.nb2{background:#242a31;color:#c3c9d0;border:1px solid #333a42;padding:5px 9px;font-size:11px;font-weight:600;border-radius:4px;margin-left:3px}
.nb2:hover{background:#157A3F;color:#fff}
table{border-collapse:collapse;width:100%}
th{background:#1c1f24;color:#9aa0a6;font-size:11px;text-transform:uppercase;
   letter-spacing:.5px;padding:8px;text-align:left;position:sticky;top:56px;z-index:8}
td{border-top:1px solid #262b31;padding:9px 8px;vertical-align:top}
tr.blank{background:#2a1f14}
.num{color:#6b7280;font-size:12px;width:32px}
.time{font-variant-numeric:tabular-nums;font-size:12px;width:126px;color:#8ab4f8}
.dim{color:#6b7280}.dur{color:#9aa0a6;font-size:11px;margin:2px 0}
.tt{font-variant-numeric:tabular-nums;text-align:center;margin-bottom:3px;
    font-size:13px!important;color:#8ab4f8!important;font-weight:600}
.orig{color:#5d646d;font-size:10px;margin-bottom:4px}
.nudge{display:flex;gap:2px}
.nb{flex:1;background:#242a31;color:#c3c9d0;border:1px solid #333a42;border-radius:3px;
    padding:3px 0;font-size:10px;font-weight:600;cursor:pointer}
.nb:hover{background:#157A3F;color:#fff}
tr.moved .tt{border-color:#c9974a;color:#f0b354!important}
tr.moved .orig{color:#c9974a}
.said{width:200px;color:#b9bec4;font-size:12.5px;font-style:italic}
.cap{width:240px}
.capline{padding:5px 10px;border-radius:14px;font-weight:800;font-size:14px;
         display:inline-block;margin:0 0 3px;letter-spacing:.2px}
.broll img{width:150px;border-radius:5px;display:block;margin-bottom:5px}
.src img{width:68px;border-radius:4px;display:block}
.src{width:76px}.broll{width:275px}
.noclip{width:150px;height:84px;border:2px dashed #6b5330;border-radius:5px;
        display:flex;align-items:center;justify-content:center;color:#c9974a;
        font-size:11px;margin-bottom:5px}
textarea,input,select{width:100%;background:#0f1114;color:#e6e6e6;
   border:1px solid #333a42;border-radius:4px;padding:5px 7px;font:inherit;font-size:12px}
textarea{resize:vertical;margin-bottom:3px}
.broll input{font-size:10px;font-family:ui-monospace,Menlo,monospace}
.ss{width:64px!important;display:inline-block}
label{font-size:11px;color:#9aa0a6}
.note{width:250px}
.anchor{margin-top:5px;color:#8ab4f8;font-size:11px;font-style:normal}
.why-lbl{color:#f0b354;font-size:10px;font-weight:700;margin:6px 0 2px;letter-spacing:.3px}
.why{border-color:#6b5330!important;background:#1d1710!important}
.vsel{margin:5px 0 4px}
</style>
<h1>Bảng duyệt — Dilim Video test · </h1>
<div class="sub">Dòng <b style="color:#c9974a">nền cam</b> = chưa có clip, anh dán path vào ô «B-ROLL».
Cột «LỜI NÓI THẬT» là transcript rơi đúng trong khung giờ đó — dùng để kiểm timestamp có lệch không.
Cột «FRAME GỐC» là hình A-roll tại đúng giây caption bắt đầu.<br><b style="color:#f0b354">Sửa được giờ:</b> gõ thẳng vào ô giây, hoặc bấm nút −/+ để dời cả caption. Dòng đổi giờ sẽ chuyển viền cam. Nếu lệch ĐỀU cả bài thì dùng nút «Dời hết» trên đầu.</div>
<div class="bar"><button onclick="save()">TẢI JSON VỀ</button>
<span class="grp">Lệch ĐỀU cả bài? Dời hết:
<button class="nb2" onclick="nudgeAll(-0.30)">−.30</button>
<button class="nb2" onclick="nudgeAll(-0.15)">−.15</button>
<button class="nb2" onclick="nudgeAll(0.15)">+.15</button>
<button class="nb2" onclick="nudgeAll(0.30)">+.30</button></span>
<span class="grp">đã sửa: <b id="cnt">0</b>/44 caption</span></div>
<table><thead><tr>
<th>#</th><th>Giây</th><th>Lời nói thật + neo</th><th>Caption</th>
<th>Frame gốc</th><th>B-roll</th><th>Ghi chú + vì sao</th></tr></thead>
<tbody>""" + "".join(body) + """</tbody></table>
<script>
// dich ca 2 moc cua 1 caption di `d` giay (khong cho xuong duoi 0)
function shift(tr,d){
  tr.querySelectorAll('.tt').forEach(e=>{
    e.value=Math.max(0,parseFloat(e.value)+d).toFixed(2);
  });
  mark(tr);
}
function nudge(btn,d){ shift(btn.closest('tr'),d); }
// dich TAT CA caption (khi lech deu ca bai)
function nudgeAll(d){ document.querySelectorAll('tr.row').forEach(tr=>shift(tr,d)); }
function mark(tr){
  const o=tr.querySelector('.orig');
  const t=[...tr.querySelectorAll('.tt')].map(e=>e.value);
  const moved = t[0]!==o.dataset.t0 || t[1]!==o.dataset.t1;
  tr.classList.toggle('moved',moved);
  document.getElementById('cnt').textContent =
    document.querySelectorAll('tr.moved').length;
}
document.addEventListener('input',e=>{ if(e.target.classList.contains('tt')) mark(e.target.closest('tr')); });

function save(){
  const out=[...document.querySelectorAll('tr.row')].map(tr=>{
    const o={idx:+tr.dataset.idx};
    tr.querySelectorAll('[data-f]').forEach(e=>o[e.dataset.f]=e.value);
    const g=tr.querySelector('.orig');
    o.t_goc=g.dataset.t0; o.t_end_goc=g.dataset.t1;   // giu moc CU de doi chieu
    return o;
  });
  const b=new Blob([JSON.stringify(out,null,1)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(b);
  a.download='duyet.json';a.click();
}
</script>"""

    # SUA 04/08/2026: ten job va so caption truoc day bi ghi cung "Dilim Video
    # test" / "44" tu job dau tien — moi bang duyet deu hien sai ten.
    doc = (doc.replace("Dilim Video test", os.path.basename(HERE))
              .replace("</b>/44 caption", f"</b>/{len(ROWS)} caption"))

    out = os.path.join(HERE, "edit/bang_duyet.html")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"-> {out}  ({os.path.getsize(out)/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()

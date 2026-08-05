# -*- coding: utf-8 -*-
"""Bang duyet BAN CAT — toan bo transcript theo tung chu, danh dau cho bi bo.

    python3 make_cut_table.py

Ra edit/bang_cat.html: doc het loi noi kem moc gio, doan bi cat gach do.
Bam nut de LAT quyet dinh tung nhat cat, sua moc truc tiep, roi tai JSON ve.
"""
import html, json, os, sys

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
WORDS = os.path.join(HERE, "edit/transcripts_words/audio16k.json")

# Doan BI BO — doc tu <job>/cuts.json (moi job mot file rieng).
#   [{"t0":0.0,"t1":2.38,"why":"cau lac"}, ...]   t1 = null nghia la den het.
_cf = os.path.join(HERE, "cuts.json")
if not os.path.exists(_cf):
    raise SystemExit(f"thieu {_cf}")
CUTS = [(c["t0"], c["t1"] if c["t1"] is not None else 1e9, c.get("why", ""))
        for c in json.load(open(_cf, encoding="utf-8"))]


def mmss(t):
    return f"{int(t//60)}:{t%60:05.2f}"


def main():
    d = json.load(open(WORDS, encoding="utf-8"))
    words = [w for s in d["segments"] for w in s.get("words", [])
             if (w.get("word") or "").strip()]
    total = max(w["end"] for w in words)

    def cut_of(w):
        mid = (w["start"] + w["end"]) / 2
        for i, (a, b, why) in enumerate(CUTS):
            if a <= mid < b:
                return i
        return None

    # gom chu thanh cac KHOI lien tiep cung trang thai (giu / bo cua nhat i)
    blocks = []
    for w in words:
        c = cut_of(w)
        if blocks and blocks[-1]["cut"] == c:
            blocks[-1]["words"].append(w)
        else:
            blocks.append({"cut": c, "words": [w]})

    body = []
    for b in blocks:
        ws = b["words"]
        t0, t1 = ws[0]["start"], ws[-1]["end"]
        txt = " ".join(w["word"].strip() for w in ws)
        if b["cut"] is None:
            body.append(
                f'<div class="blk keep"><span class="tm">{mmss(t0)} → {mmss(t1)}</span>'
                f'<span class="tx">{html.escape(txt)}</span></div>')
        else:
            i = b["cut"]
            why = CUTS[i][2]
            body.append(
                f'<div class="blk cut" data-cut="{i}" data-t0="{CUTS[i][0]}" data-t1="{CUTS[i][1]}">'
                f'<span class="tm">{mmss(t0)} → {mmss(t1)}</span>'
                f'<span class="tx">{html.escape(txt)}</span>'
                f'<span class="why">NHÁT {i+1} · {html.escape(why)} · −{t1-t0:.2f}s</span>'
                f'<button class="tg" onclick="toggle(this)">GIỮ LẠI</button></div>')

    kept = total - sum(min(b, total) - a for a, b, _ in CUTS)
    doc = f"""<!doctype html><meta charset="utf-8">
<title>Bảng duyệt bản cắt — DSCF0894</title>
<style>
*{{box-sizing:border-box}}
body{{font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;
 padding:20px 24px;background:#14161a;color:#e6e6e6;max-width:1000px}}
h1{{font-size:19px;margin:0 0 4px}}
.sub{{color:#9aa0a6;font-size:13px;margin-bottom:14px}}
.bar{{position:sticky;top:0;background:#14161a;padding:10px 0 12px;
 border-bottom:1px solid #2a2f36;margin-bottom:16px;z-index:9}}
button{{background:#157A3F;color:#fff;border:0;padding:9px 18px;border-radius:6px;
 font-size:14px;font-weight:600;cursor:pointer}}
button:hover{{background:#1a9950}}
.stat{{margin-left:16px;color:#9aa0a6;font-size:13px}}
.blk{{padding:7px 10px;border-radius:6px;margin-bottom:3px;position:relative}}
.keep{{background:#181c20}}
.cut{{background:#2a1418;border-left:3px solid #D62828}}
.cut.off{{background:#182018;border-left-color:#157A3F;opacity:.75}}
.tm{{display:inline-block;min-width:118px;color:#8ab4f8;font-size:12px;
 font-variant-numeric:tabular-nums}}
.tx{{color:#dfe3e7}}
.cut .tx{{text-decoration:line-through;color:#c98a90}}
.cut.off .tx{{text-decoration:none;color:#dfe3e7}}
.why{{display:block;margin:5px 0 0 118px;color:#e0757f;font-size:12px}}
.cut.off .why{{color:#6b7280;text-decoration:line-through}}
.tg{{position:absolute;right:10px;top:7px;background:#3a2226;color:#e0757f;
 border:1px solid #5a3038;padding:4px 10px;font-size:11px;border-radius:4px}}
.cut.off .tg{{background:#1d2a1f;color:#6ee7a0;border-color:#2c4a33}}
.tg:hover{{background:#D62828;color:#fff}}
</style>
<h1>Bảng duyệt bản cắt — DSCF0894</h1>
<div class="sub">Đọc hết lời nói kèm mốc giờ. Đoạn <b style="color:#e0757f">gạch đỏ</b> là chỗ tôi định bỏ —
bấm «GIỮ LẠI» để huỷ nhát cắt đó. Muốn cắt thêm chỗ khác thì ghi cho tôi mốc giờ.</div>
<div class="bar"><button onclick="save()">TẢI JSON VỀ</button>
<span class="stat">gốc <b>{mmss(total)}</b> · sau cắt <b id="out">{mmss(kept)}</b>
 · bỏ <b id="rm">{total-kept:.1f}s</b> · nhát đang bật <b id="on">{len(CUTS)}</b>/{len(CUTS)}</span></div>
{''.join(body)}
<script>
const TOTAL={total:.2f};
function toggle(b){{ b.closest('.blk').classList.toggle('off');
  b.textContent = b.closest('.blk').classList.contains('off') ? 'CẮT LẠI' : 'GIỮ LẠI'; upd(); }}
function upd(){{
  let rm=0,n=0;
  document.querySelectorAll('.blk.cut').forEach(e=>{{
    if(!e.classList.contains('off')){{
      rm += Math.min(+e.dataset.t1,TOTAL)-(+e.dataset.t0); n++; }}
  }});
  const k=TOTAL-rm;
  document.getElementById('out').textContent=Math.floor(k/60)+':'+(k%60).toFixed(2).padStart(5,'0');
  document.getElementById('rm').textContent=rm.toFixed(1)+'s';
  document.getElementById('on').textContent=n;
}}
function save(){{
  const cuts=[...document.querySelectorAll('.blk.cut')].map(e=>({{
    nhat:+e.dataset.cut+1, t0:+e.dataset.t0, t1:+e.dataset.t1,
    bat: !e.classList.contains('off')
  }}));
  const b=new Blob([JSON.stringify(cuts,null,1)],{{type:'application/json'}});
  const a=document.createElement('a');a.href=URL.createObjectURL(b);
  a.download='duyet_cat.json';a.click();
}}
</script>"""

    out = os.path.join(HERE, "edit/bang_cat.html")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"goc {mmss(total)}  ->  sau cat {mmss(kept)}   (bo {total-kept:.1f}s)")
    print(f"-> {out}")


if __name__ == "__main__":
    main()

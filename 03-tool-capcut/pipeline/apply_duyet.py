# -*- coding: utf-8 -*-
"""Nhan `duyet.json` anh Thanh tai ve tu bang duyet — CHAM DIEM roi ap vao plan.

    python3 apply_duyet.py --job 04-du-an/<ten>            # chi cham diem
    python3 apply_duyet.py --job 04-du-an/<ten> --apply    # ghi de edit/plan.json

Tim `duyet.json` theo thu tu: --file  ->  <job>/edit/  ->  ~/Downloads/

VI SAO CO BUOC NAY: bang duyet xuat ra duoc `duyet.json` tu 03/08, nhung
KHONG CO GI DOC NO. Anh sua 13/49 dong tren DSCF0894 kem ly do, roi cai ly do
do bay mat. Ket qua: khong ai biet ban nay TOT HON hay TE HON ban truoc.

Hai thu file nay lam:
  1. CHAM DIEM — % dong anh KHONG phai sua. Day la con so backtest that su
     cua tool, do duoc qua tung phien ban. Ghi vao edit/diem.md.
  2. GOM BAI HOC — moi o «VI SAO» anh go vao duoc chep sang 03-tool-capcut/
     BAI_HOC.md kem dong truoc/sau. Doc file do truoc khi dung job moi;
     luat nao lap lai du 2-3 lan thi cai thang vao code (nhu luat chong lap
     da thanh 4b_vary.py).
"""
import argparse
import json
import os
import sys
from datetime import date

FIELDS = ["t", "t_end", "d1", "d2", "variant", "path", "src_start"]
NUM = {"t", "t_end", "src_start"}
NHAN = {"t": "giờ vào", "t_end": "giờ ra", "d1": "dòng 1", "d2": "dòng 2",
        "variant": "màu", "path": "clip", "src_start": "giây bắt đầu clip"}


def cast(field, v):
    if field in NUM:
        try:
            return round(float(str(v).strip() or 0), 2)
        except ValueError:
            return 0.0
    return str(v).strip()


def find_duyet(job, explicit):
    cands = []
    if explicit:
        cands.append(os.path.abspath(os.path.expanduser(explicit)))
    cands.append(os.path.join(job, "edit/duyet.json"))
    cands.append(os.path.expanduser("~/Downloads/duyet.json"))
    for c in cands:
        if os.path.exists(c):
            return c
    sys.exit("khong thay duyet.json — tai ve tu bang duyet roi de o "
             f"{os.path.join(job, 'edit/')} hoac ~/Downloads/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--file", help="duong dan duyet.json")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    job = os.path.abspath(os.path.expanduser(a.job))
    if not os.path.isdir(job):
        sys.exit(f"khong thay job: {job}")
    P = os.path.join(job, "edit/plan.json")
    plan = json.load(open(P, encoding="utf-8"))
    dpath = find_duyet(job, a.file)
    duyet = {int(r["idx"]): r for r in json.load(open(dpath, encoding="utf-8"))}
    print(f"bang duyet : {dpath}")

    per_field = {f: 0 for f in FIELDS}
    dirty, lessons, missing = [], [], []
    for r in plan:
        d = duyet.get(r["idx"])
        if d is None:
            missing.append(r["idx"])
            continue
        diffs = []
        for f in FIELDS:
            if f not in d:
                continue
            new = cast(f, d[f])
            old = cast(f, r.get(f, ""))
            if new != old:
                per_field[f] += 1
                diffs.append((f, old, new))
        why = str(d.get("vi_sao", "")).strip()
        if diffs:
            dirty.append((r["idx"], diffs, why, r["text"]))
        if why:
            lessons.append((r["idx"], why, diffs, r["text"]))

    n = len(plan) - len(missing)
    ok = n - len(dirty)
    diem = 100.0 * ok / n if n else 0.0

    print(f"caption    : {n}" + (f"  (thieu {len(missing)} dong trong duyet.json)"
                                 if missing else ""))
    print(f"giu nguyen : {ok}")
    print(f"phai sua   : {len(dirty)}")
    print(f"\nDIEM       : {diem:.1f}%  (% dong anh khong phai sua)\n")
    for f in FIELDS:
        if per_field[f]:
            print(f"   {NHAN[f]:18} {per_field[f]:3} dong")
    if lessons:
        print(f"\n{len(lessons)} dong co ghi VI SAO — se chep sang BAI_HOC.md")

    # ---- edit/diem.md ----
    md = [f"# Điểm — {os.path.basename(job)}",
          f"\nNgày chấm: {date.today().isoformat()} · nguồn: `{os.path.basename(dpath)}`\n",
          f"\n**{diem:.1f}%** — {ok}/{n} caption anh không phải sửa.\n",
          "\n| Sửa gì | Bao nhiêu dòng |\n|---|---|"]
    for f in FIELDS:
        if per_field[f]:
            md.append(f"| {NHAN[f]} | {per_field[f]} |")
    if dirty:
        md.append("\n## Từng dòng đã sửa\n")
        for idx, diffs, why, text in dirty:
            md.append(f"\n**#{idx}** — {text.replace(chr(10), ' / ')}\n")
            for f, old, new in diffs:
                so = os.path.basename(str(old)) if f == "path" else old
                sn = os.path.basename(str(new)) if f == "path" else new
                md.append(f"- {NHAN[f]}: `{so}` → `{sn}`")
            if why:
                md.append(f"- **vì sao:** {why}")
    out = os.path.join(job, "edit/diem.md")
    open(out, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"\n-> {out}")

    # ---- BAI_HOC.md (gom qua moi job) ----
    if lessons:
        root = os.path.abspath(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), ".."))
        bh = os.path.join(root, "BAI_HOC.md")
        new = not os.path.exists(bh)
        head = f"## {os.path.basename(job)} — {date.today().isoformat()}"
        if not new and head in open(bh, encoding="utf-8").read():
            print(f"-> {bh}  (job nay da ghi hom nay, khong chep lai)")
            lessons = []
    if lessons:
        with open(bh, "a", encoding="utf-8") as f:
            if new:
                f.write("# Bài học từ bảng duyệt\n\n"
                        "Mỗi mục là một ô «VÌ SAO» anh Thành gõ vào bảng duyệt.\n"
                        "Đọc file này TRƯỚC khi soạn `plan.py` cho job mới.\n"
                        "Luật nào lặp lại 2–3 lần thì cài thẳng vào code, rồi "
                        "ghi chú `[đã cài: <file>.py]` vào đây.\n")
            f.write(f"\n{head} — điểm {diem:.1f}%\n")
            for idx, why, diffs, text in lessons:
                f.write(f"\n**#{idx}** {text.replace(chr(10), ' / ')}\n\n")
                for fl, old, new in diffs:
                    so = os.path.basename(str(old)) if fl == "path" else old
                    sn = os.path.basename(str(new)) if fl == "path" else new
                    f.write(f"- {NHAN[fl]}: `{so}` → `{sn}`\n")
                f.write(f"- **vì sao:** {why}\n")
        print(f"-> {bh}  (+{len(lessons)} bài học)")

    # ---- ap vao plan.json ----
    if not a.apply:
        print("\n(chi cham diem — them --apply de ghi de plan.json)")
        return

    words = None
    wp = os.path.join(job, "edit/words_cut.json")
    if os.path.exists(wp):
        words = json.load(open(wp, encoding="utf-8"))

    for r in plan:
        d = duyet.get(r["idx"])
        if d is None:
            continue
        for f in FIELDS:
            if f in d:
                r[f] = cast(f, d[f])
        if "note" in d:
            r["note"] = str(d["note"]).strip()
        why = str(d.get("vi_sao", "")).strip()
        if why:
            r["vi_sao"] = why
        r["text"] = r["d1"] + ("\n" + r["d2"] if r["d2"] else "")
        if words:
            r["said"] = " ".join(w["w"] for w in words
                                 if r["t"] - 0.05 <= w["s"] < r["t_end"] - 0.05)
    json.dump(plan, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n-> da ghi de {P}")
    print("   chay lai: 5_render_captions.py  roi  6_to_capcut.py")


if __name__ == "__main__":
    main()

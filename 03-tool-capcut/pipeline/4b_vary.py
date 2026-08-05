# -*- coding: utf-8 -*-
"""Chong lap B-roll — xoay vong trong ho clip thay vi lap lai dung mot file.

VAN DE (anh Thanh chi ra 04/08/2026, "test hiếu 1" doan 2:33): kich ban ban
hang tu lap y — anh Hieu noi "mach mau thong thoang, phong ngua dot quy" 4
lan trong mot bai. Lap y ma gap kho it clip thi ra LAP HINH, xem chan.

CACH SUA: moi clip thuoc mot HO (clips.FAMILIES). Neu mot clip sap duoc dung
lai trong vong COOLDOWN giay, doi sang clip KHAC cung ho chua dung gan day.
Het lua chon thi giu nguyen (tha lap con hon dung clip sai y).

    python3 4b_vary.py --job <job>            # xem truoc
    python3 4b_vary.py --job <job> --apply
"""
import argparse, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C

COOLDOWN = 25.0        # giay — trong khoang nay khong dung lai cung mot clip

# HAI NGOAI LE — them 04/08/2026 sau khi buoc nay pha bai "natto hoat huyet".
#
# 1. CAPTION LIEN NHAU CUNG CLIP LA CO Y (luat 1 anh Thanh day 03/08: "2 cai
#    lien tiep la chay het cai nay den cai kia"). 6_to_capcut.py gop chung
#    thanh MOT doan B-roll chay lien mach. Buoc nay truoc day thay "lap sau
#    4.0s" roi doi mat — dung cai ma buoc sau dang co gop lai.
# 2. B-ROLL SAN PHAM MIEN TRU (chon-broll.md da ghi, code chua cai). Ho
#    `san_pham` chi co 4 file va lan trong do co `richnatto-01.mp4` = HAI HOP
#    chung; xoay trung vao no giua doan bao gia 6 hop Natto la doi san pham
#    giua chung. Tha lap anh san pham con hon.
SKIP_FAM = {"san_pham", "san_pham_rich"}

_dur = {}


def dur(p):
    """do dai clip (giay); anh -> vo han"""
    if p.endswith(C.IMG_EXT):
        return 1e9
    if p not in _dur:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", p],
                           capture_output=True, text=True)
        try:
            _dur[p] = float(r.stdout.strip())
        except ValueError:
            _dur[p] = 0.0
    return _dur[p]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    job = os.path.abspath(os.path.expanduser(a.job))
    P = os.path.join(job, "edit/plan.json")
    plan = json.load(open(P, encoding="utf-8"))

    # clip -> ho
    fam_of = {}
    for fam, lst in C.FAMILIES.items():
        for c in lst:
            fam_of.setdefault(c, fam)

    last = {}          # clip -> lan cuoi dung
    last_idx = {}      # clip -> idx caption dung lan cuoi
    changed = []
    for r in plan:
        p = (r.get("path") or "").strip().strip("'\"")
        if not p:
            continue
        t = r["t"]
        prev = last.get(p)
        # ngoai le 1: caption ngay truoc cung dung clip nay -> co y cho chay lien mach
        lien_mach = last_idx.get(p) == r["idx"] - 1
        if prev is not None and t - prev < COOLDOWN and not lien_mach:
            fam = fam_of.get(p)
            if fam in SKIP_FAM:      # ngoai le 2: san pham mien tru
                fam = None
            if fam:
                # chon clip cung ho, chua dung hoac dung lau nhat
                pool = [c for c in C.FAMILIES[fam] if os.path.exists(c)]
                need = r["t_end"] - r["t"]
                # chi doi sang clip DU DAI (tinh ca moc bat dau toi thieu)
                free = [c for c in pool
                        if t - last.get(c, -1e9) >= COOLDOWN
                        and dur(c) - C.MIN_START.get(c, 0) >= need]
                if free:
                    new = min(free, key=lambda c: last.get(c, -1e9))
                    changed.append((r["idx"], os.path.basename(p),
                                    os.path.basename(new), t - prev))
                    r["path"] = new
                    r["src_start"] = C.MIN_START.get(new, 0)
                    p = new
        last[p] = t
        last_idx[p] = r["idx"]

    print(f"caption co B-roll : {sum(1 for r in plan if r['path'])}")
    print(f"doi de khoi lap   : {len(changed)}")
    for i, o, n, gap in changed:
        print(f"   #{i:2}  {o[:26]:26} -> {n[:30]:30} (lap sau {gap:.1f}s)")

    import collections
    c = collections.Counter(os.path.basename(r["path"]) for r in plan if r["path"])
    print("\nlap nhieu nhat sau khi sua:")
    for f, k in c.most_common(4):
        print(f"   {k}x  {f}")

    if a.apply:
        json.dump(plan, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\n-> da ghi {P}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""LUONG 2 — caption ve san bang engine cua bo Tinh, dua vao CapCut dang PNG.

Khac luong 1 (to_capcut.py): caption KHONG con la text layer cua CapCut nua
(xau, khong dung style DiLiM) ma la 44 anh PNG trong suot do
pipeline/caption_style.py cua bo Tinh ve ra — dung font Anton, dung 3 ho mau
xoay deterministic, dung khoi nen bo goc.

B-roll giu y nguyen cach cat cua luong 1, chi doi sang bo so mask anh da chot.

    python3 render_captions.py          # ve PNG truoc
    python3 to_capcut_v2.py             # dung draft
    python3 to_capcut_v2.py --install   # + chep vao CapCut
"""
import json, os, re, shutil, subprocess, sys, time, uuid
from PIL import Image

VECT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../VectCutAPI"))
sys.path.insert(0, VECT)
import sfx as _sfx                                                        # noqa: E402
from pyJianYingDraft import (Script_file, Video_material, Video_segment,   # noqa: E402
                             Clip_settings, Timerange, Track_type,
                             CapCut_Mask_type, CapCut_Intro_type,
                             Audio_material, Audio_segment)
from pyJianYingDraft.audio_segment import Audio_fade                      # noqa: E402

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
PLAN = os.path.join(HERE, "edit/plan.json")
SRC = next((p for p in (os.path.join(HERE, "edit/final.mp4"),
                        os.path.join(HERE, "source.mp4"),
                        os.path.join(HERE, "source.MOV")) if os.path.exists(p)), "")

# ---- A-ROLL: THA NHIEU DOAN LEN TIMELINE (anh Thanh chot 04/08/2026 toi) ----
# Anh: "cai ma cho han vao timeline cut roi toi de dang keo tha chinh sua thi
# tien cho toi hon".
#
# Truoc day tha DUY NHAT `final.mp4` (da cat san) -> anh khong keo lai duoc moi
# cat, vi phan bi bo da khong con trong file. Gio tha THANG file nguon, moi
# doan giu la mot segment. Ba cai loi ra them:
#   - khong encode lai (nguon HEVC giu nguyen chat, bot ~1 phut moi video)
#   - anh keo duoc tung moi cat, phan bi bo van nam trong nguon de keo lai
#   - `edl.json` da co san danh sach doan giu, khong phai tinh lai
# Doi lai: caption dang neo theo dong thoi gian SAU khi cat. Anh keo moi cat
# thi chu KHONG tu chay theo — lech dung bang phan anh keo.
GOC = next((p for p in (os.path.join(HERE, "source.mp4"),
                        os.path.join(HERE, "source.MOV"),
                        os.path.join(HERE, "source.mov")) if os.path.exists(p)), "")
EDL = os.path.join(HERE, "edit/edl.json")
FADE_US = 30_000        # 30ms moi moi noi — chong tieng "bup", bang 2_cut.py
PNG_DIR = os.path.join(HERE, "edit/captions_png")
# ten project CapCut: mac dinh theo ten thu muc job, doi bang --name "..."
def _name():
    if "--name" in sys.argv:
        return sys.argv[sys.argv.index("--name") + 1]
    return "DiLiM - " + os.path.basename(HERE)


NAME = _name()
CAPCUT_DRAFTS = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")

W, H, US = 1080, 1920, 1_000_000


def us(t):
    """giay -> micro giay, LAM TRON.

    LOI THAT 04/08/2026: dung int() thi 8.04*1e6 ra 8039999 (so thuc khong
    bieu dien chinh xac), trong khi doan truoc ket thuc o 2860000+5180000 =
    8040000 -> doan sau bat dau SOM 1us -> CapCut bao SegmentOverlap.
    Moi moc phai qua ham nay, va do dai = us(t_end) - us(t0), KHONG nhan
    hieu hai so thuc.
    """
    return int(round(t * US))

# bo so mask anh Thanh da chot 03/08 (29/31 clip) — xem memory dilim-broll-band-mask
BROLL_TRANSFORM_Y = 0.6834
BROLL_SCALE = 1.0
MASK_W, MASK_H = 0.28, 0.0
# SUA 04/08/2026 (toi): anh Thanh keo dai B-roll LEN CAO hon trong draft magie —
# "position mask cua broll van bi thap qua nen no lo vien".
#   centerY  -0.842027 -> -0.705959   (bot am = dai len cao, che het vien duoi)
#   centerX  -0.107572 -> -0.107502   (chenh 0.00007 — CapCut lam tron khi anh keo,
#                                      chep y nguyen cho khoi lech dan qua cac lan)
MASK_CENTER_X, MASK_CENTER_Y = -0.107502, -0.705959
MASK_FEATHER, MASK_ROUND, MASK_ROT = 0.283066, 0.0, 0.0

# ---- NORMALIZE LOUDNESS cho A-roll (anh Thanh yeu cau 04/08/2026) ----
# Doc tu draft magie sau khi anh tick tay: 13 muc `loudnesses` co
# `enable: true, target_loudness: -14.0` — dung bang so doan A-roll.
# Co toan cuc `normalize_loudness` VAN LA false, tuc day la thiet lap THEO
# TUNG DOAN, khong phai mot cong tac chung. Thu vien khong co API cho no nen
# phai nhet thang vao JSON o buoc hau ky (giong cach lam voi Audio_fade).
LOUDNESS_TARGET = -14.0

# ---- ANIMATION VAO CHU ----
# Ban Remotion cua bo Dr Son xoay vong 5 kieu theo i % 5
# (remotion-video/src/Captions.tsx:211 — "pop","up","left","down","right").
#
# SUA 03/08/2026 theo yeu cau cua anh Thanh: TEP KHACH LA NGUOI CO TUOI,
# chuyen dong lien tuc va dai lam moi mat, kho bam theo chu. Nen:
#   - BO HAN 4 kieu truot (Slide_*) — dich chuyen ngang/doc la kieu met nhat
#     khi vua phai doc vua phai bam theo.
#   - Chi con 2 kieu, gan theo Y NGHIA caption chu khong xoay vong may moc.
#   - Rut thoi luong 0.5s -> 0.25/0.30s de chu doc duoc som hon.
ANIM_BY_VARIANT = {
    # nghiem trong: trieu chung, tac nghen, nguy co -> tien nhe ve phia truoc,
    # tao nhan ma khong keo mat di dau
    "warning":   (CapCut_Intro_type.Zoom_In, 0.30),
    # giai thich / giai phap / san pham / cau hoi / CTA -> chi hien len,
    # KHONG dich chuyen. CTA co so dien thoai nen tuyet doi khong nhuc nhich.
    "positive":  (CapCut_Intro_type.Fade_In, 0.25),
    "product":   (CapCut_Intro_type.Fade_In, 0.25),
    "yellow":    (CapCut_Intro_type.Fade_In, 0.25),
    "cta":       (CapCut_Intro_type.Fade_In, 0.25),
    "highlight": (CapCut_Intro_type.Fade_In, 0.25),
}
ANIM_MAX_RATIO = 1 / 3   # animation khong duoc dai qua 1/3 do dai caption

# ---- VI TRI CAPTION ----
# PNG do caption_style.py ve la khung DAY DU 1080x1920, chu da nam san o vi tri
# "ngay duoi dai B-roll". Mac dinh transform_y = 0 (dat nguyen khung).
# SUA 03/08/2026: anh keo len cao hon tren draft "DiLiM - DSCF0894" —
# ca 49 caption deu ve +0.154523 (o UI CapCut hien Y = 297; 297/1920 = 0.154523).
CAP_TRANSFORM_Y = 0.154523

# ---- LOGO ----
# SUA 04/08/2026 (toi): DOC THANG tu draft "DiLiM - 05-2026-08-04-natto-hoat-huyet"
# sau khi anh Thanh keo tay. Khong con phep quy doi nao o giua.
#   truoc: scale 0.37      x -0.694444    y 0.931771   (toi tu quy doi tu panel)
#   nay  : scale 0.332886  x -0.667114    y 0.866834   (anh keo — logo NHO hon,
#                                                       dich vao trong va xuong)
LOGO_SCALE = 0.332886472806674
LOGO_X = -0.667113527193326
LOGO_Y = 0.8668341708542714

# Anh Thanh con dat MASK cho logo — bo goc tron, cat bot vien anh PNG.
# Doc thang tu draft cua anh (materials.common_mask, cai ten "Rectangle";
# 43 cai "Split" con lai la mask dai B-roll, khong phai cua logo).
#   config: width 0.8142613002232143 · height 0.466552734375
#           centerX/Y 0 · feather 0 · roundCorner 0.5065625
# `add_mask` nhan feather/round_corner theo THANG 0-100 roi tu chia 100,
# nen round_corner phai truyen 50.65625 moi ra 0.5065625.
LOGO_MASK_W = 0.8142613002232143     # rect_width — ti le theo CHIEU RONG khung
LOGO_MASK_H = 0.466552734375         # size      — ti le theo CHIEU CAO khung
LOGO_MASK_ROUND = 50.65625           # -> roundCorner 0.5065625

import clips as _clips                                                    # noqa: E402
# doi bang --logo <duong dan> khi can (vd logo chien dich rieng)
LOGO_PATH = (sys.argv[sys.argv.index("--logo") + 1] if "--logo" in sys.argv
             else _clips.LOGO)    # T7/05 Finish part/dilim logo .png


def photo_material(path, dur_s):
    """Video_material cho anh — BAT BUOC truyen width/height.

    LOI THAT 03/08/2026: thu vien do duoc kich thuoc VIDEO nhung KHONG do
    duoc ANH, de width=height=0. CapCut coi material co kich thuoc 0 la
    chua link duoc -> bat hien hop thoai "Link media" cho ca 53 anh du
    duong dan hoan toan dung.
    """
    w, h = Image.open(path).size
    m = Video_material(material_type="photo", path=path)
    # BUG THU VIEN (local_materials.py:126): nhanh "photo" gan cung
    # width=height=0 roi `return` NGAY, bo qua tham so truyen vao.
    # Nen phai ghi de sau khi tao.
    m.width, m.height = w, h
    m.duration = int(dur_s * 1_000_000)
    return m


def probe_fps(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    t = re.sub(r"[^0-9/]", "", r.stdout.strip().splitlines()[0]) if r.stdout.strip() else "30/1"
    a, _, b = t.partition("/")
    return float(a) / float(b or 1)


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    if not os.path.isdir(PNG_DIR) or not os.listdir(PNG_DIR):
        sys.exit("chua co caption PNG — chay `python3 render_captions.py` truoc")

    _fps_src = GOC if (GOC and os.path.exists(EDL)) else SRC
    _f = probe_fps(_fps_src)
    FPS = 30 if _f > 60 else round(_f)      # nguon iPhone 120fps -> ha ve 30
    print(f"fps doc tu file: {_f:.3f} -> dung {FPS}")
    s = Script_file(W, H, FPS)
    s.add_track(Track_type.video, "aroll", relative_index=0)
    s.add_track(Track_type.video, "broll", relative_index=1)
    s.add_track(Track_type.video, "caption", relative_index=2)
    s.add_track(Track_type.video, "logo", relative_index=3)
    s.add_track(Track_type.audio, "sfx")

    # ---- A-roll ----
    end = max(p["t_end"] for p in plan)
    keeps = []
    if GOC and os.path.exists(EDL):
        try:
            keeps = json.load(open(EDL, encoding="utf-8")).get("keeps", [])
        except Exception:
            keeps = []

    if keeps:
        # nhieu doan tu FILE NGUON — anh keo lai duoc tung moi cat
        mat = Video_material(material_type="video", path=GOC)
        pos = 0
        for a, b in keeps:
            d = us(b) - us(a)               # do dai = hieu HAI MOC DA LAM TRON
            if d <= 0:
                continue
            seg = Video_segment(mat, Timerange(pos, d),
                                source_timerange=Timerange(us(a), d))
            fade = Audio_fade(min(FADE_US, d // 2), min(FADE_US, d // 2))
            s.materials.audio_fades.append(fade)
            seg.extra_material_refs.append(fade.fade_id)
            s.add_segment(seg, "aroll")
            pos += d
        a_dur = pos
    else:
        # duong lui: mot mieng `final.mp4` da cat san
        a_dur = int(min(probe(SRC), end + 0.5) * US)
        s.add_segment(Video_segment(Video_material(material_type="video", path=SRC),
                                    Timerange(0, a_dur),
                                    source_timerange=Timerange(0, a_dur)),
                      "aroll")

    # ---- KEP DUOI: A-ROLL HET LA MOI THU HET THEO ----
    # LUAT ANH THANH 05/08/2026 (duyet job 07-dji0485):
    #   "doan ket, b-roll du ra so voi a-roll... a-roll het la b-roll phai het luon"
    # `plan_build.py` keo caption cuoi toi `t + thoi luong uoc luong`, no KHONG
    # biet A-roll dai bao nhieu. Job 07 lech 0.52s -> nua giay cuoi chi con dai
    # B-roll troi tren nen trong, nhin nhu loi render.
    # Kep o DAY chu khong o plan_build.py: chi den buoc nay moi biet do dai THAT
    # cua A-roll (tong cac doan keeps, sau khi da lam tron tung moc ve frame).
    a_end = a_dur / US
    _tail = [p["idx"] for p in plan if p["t_end"] > a_end + 1 / 30]
    for p in plan:
        p["t_end"] = min(p["t_end"], a_end)
        if "cap_end" in p:
            p["cap_end"] = min(p["cap_end"], a_end)
    _bo = [p["idx"] for p in plan if p["t"] >= a_end - 0.05]
    plan = [p for p in plan if p["t"] < a_end - 0.05]
    if _tail:
        print(f"kep duoi : A-roll het o {a_end:.2f}s -> xen {len(_tail)} caption "
              f"({', '.join('#' + str(i) for i in _tail[:6])}"
              f"{'...' if len(_tail) > 6 else ''})")
    if _bo:
        print(f"           bo han {len(_bo)} caption bat dau sau khi A-roll da het: "
              f"{', '.join('#' + str(i) for i in _bo)}")

    # ---- B-roll ----
    # LUAT ANH THANH DAY 03/08/2026 (bang duyet DSCF0894, caption #12 va #30):
    #   "2 cai lien tiep la chay het cai nay den cai kia"
    #   "van giu tiep clip ben tren kia chay thoi"
    # => Caption LIEN TIEP dung CUNG mot clip thi B-roll phai chay LIEN MACH,
    #    KHONG cat, KHONG restart ve src_start. Gop thanh 1 doan duy nhat trai
    #    dai ca cum, bat dau tu src_start cua caption dau cum.
    groups, cur, missing, portrait = [], None, [], []
    for p in plan:
        path = (p.get("path") or "").strip().strip("'\"").strip()
        if not path:
            cur = None
            continue
        if not os.path.exists(path):
            # KHONG bo qua im lang nua — anh doi ten kho giua chung thi phai biet
            missing.append(f"caption {p['idx']}: {os.path.basename(path)}")
            cur = None
            continue
        # CLIP DOC khong dung cho dai B-roll: dai la 1080x672 NGANG, tha clip
        # doc vao thi bi cat con mot lat mong, nhin lech han. (anh Thanh 04/08)
        _o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                             "-show_entries", "stream=width,height", "-of",
                             "csv=p=0", path], capture_output=True, text=True).stdout.strip()
        try:
            _w, _h = (int(x) for x in _o.split(",")[:2])
            if _h > _w:
                portrait.append(f"caption {p['idx']}: {os.path.basename(path)} ({_w}x{_h})")
                cur = None
                continue
        except ValueError:
            pass
        if cur and cur["path"] == path and abs(cur["t_end"] - p["t"]) < 0.05:
            cur["t_end"] = p["t_end"]          # noi dai cum
        else:
            cur = {"path": path, "t": p["t"], "t_end": p["t_end"],
                   "src_start": float(p.get("src_start") or 0)}
            groups.append(cur)
    merged = len(plan) - len(groups)

    n_b, hut = 0, []
    for p in groups:
        path = p["path"]
        t0, need = p["t"], p["t_end"] - p["t"]
        is_img = path.lower().endswith((".jpg", ".jpeg", ".png"))
        ss = p["src_start"]

        # SUA 04/08/2026 — LOI THAT trong 3 draft da dung: `plan.py` kiem do dai
        # clip TRUOC khi 4_anchor.py doi moc, roi khong ai kiem lai. Sau khi neo,
        # caption dai ra (va cac caption cung clip con bi GOP lai o tren) nen
        # source_timerange doi vuot qua het file. Truoc day cu the ma ghi ->
        # CapCut dung hinh hoac hong doan do.
        # Gio: lui `ss` neu clip du dai, khong du thi CAT NGAN doan B-roll —
        # tha dai ket som con hon dung hinh giua chung.
        if not is_img:
            dsrc = probe(path)
            if dsrc and ss + need > dsrc + 0.03:
                if dsrc >= need:
                    ss = round(max(0.0, dsrc - need), 2)
                    hut.append(f"#{p['t']:.1f}s lui src_start -> {ss} "
                               f"({os.path.basename(path)})")
                else:
                    need = round(dsrc - ss, 2)
                    p["t_end"] = p["t"] + need
                    hut.append(f"#{p['t']:.1f}s CAT NGAN con {need:.1f}s "
                               f"({os.path.basename(path)} chi {dsrc:.1f}s)")
        seg = Video_segment(
            photo_material(path, need) if is_img
            else Video_material(material_type="video", path=path),
            Timerange(us(t0), us(p["t_end"]) - us(t0)),
            source_timerange=None if is_img else Timerange(us(ss), us(p["t_end"]) - us(t0)),
            volume=0.0,
            clip_settings=Clip_settings(scale_x=BROLL_SCALE, scale_y=BROLL_SCALE,
                                        transform_y=BROLL_TRANSFORM_Y),
        )
        seg.add_mask(s, CapCut_Mask_type.Split,
                     center_x=MASK_CENTER_X * (W / 2), center_y=MASK_CENTER_Y * (H / 2),
                     size=MASK_W * W / H, feather=MASK_FEATHER * 100, rotation=MASK_ROT)
        s.add_segment(seg, "broll")
        n_b += 1

    # ---- caption: PNG trong suot, dat toan khung, khong can can chinh vi tri ----
    n_c, anim_used = 0, {}
    for i, p in enumerate(plan):
        png = os.path.join(PNG_DIR, f"cap_{p['idx']:03d}.png")
        if not os.path.exists(png):
            print(f"  ! thieu {os.path.basename(png)}")
            continue
        # lop CHU tat theo `cap_end` (co the som hon t_end -> chua khoang tho).
        # B-roll o tren van chay theo t_end nen hinh khong bi ngat.
        c_end = min(p.get("cap_end", p["t_end"]), p["t_end"])
        t0, need = p["t"], c_end - p["t"]
        seg = Video_segment(photo_material(png, need),
                            Timerange(us(t0), us(c_end) - us(t0)),
                            clip_settings=Clip_settings(transform_y=CAP_TRANSFORM_Y))
        anim, adur = ANIM_BY_VARIANT.get(p["variant"], ANIM_BY_VARIANT["positive"])
        adur = min(adur, need * ANIM_MAX_RATIO)     # caption ngan thi rut animation
        seg.add_animation(anim, duration=int(adur * US))
        k = f"{anim.name} ({p['variant']})"
        anim_used[k] = anim_used.get(k, 0) + 1
        s.add_segment(seg, "caption")
        n_c += 1

    # ---- LOGO: mot mieng duy nhat, trai suot bai (anh chot 04/08/2026) ----
    logo_ok = False
    if os.path.exists(LOGO_PATH):
        logo_seg = Video_segment(
            photo_material(LOGO_PATH, a_dur / US),
            Timerange(0, a_dur),
            clip_settings=Clip_settings(scale_x=LOGO_SCALE, scale_y=LOGO_SCALE,
                                        transform_x=LOGO_X, transform_y=LOGO_Y),
        )
        logo_seg.add_mask(s, CapCut_Mask_type.Rectangle,
                          center_x=0.0, center_y=0.0,
                          size=LOGO_MASK_H, rect_width=LOGO_MASK_W,
                          rotation=0.0, feather=0.0,
                          round_corner=LOGO_MASK_ROUND)
        s.add_segment(logo_seg, "logo")
        logo_ok = True
    else:
        print(f"  ! KHONG THAY LOGO: {LOGO_PATH} — bo qua (cam o T7 chua?)")

    # ---- SFX: 1 cue moi caption, luat anh chot 15/07/2026 (xem sfx.py) ----
    cues = _sfx.derive_cues(plan)
    vol = _sfx.volume_linear()
    import collections as _c
    npool = _c.Counter(p for _, _, p in cues)
    for t, f, _p in cues:
        m = Audio_material(path=f)
        d_us = min(m.duration, int(1.2 * US))          # cat bot neu sfx qua dai
        seg = Audio_segment(m, Timerange(us(t), d_us),
                            source_timerange=Timerange(0, d_us), volume=vol)
        seg.add_fade(0, "0.05s")                        # tranh cach tach o duoi
        s.add_segment(seg, "sfx")

    # ---- ghi ra dia ----
    out_dir = os.path.join(HERE, "edit/capcut_draft_v2")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(os.path.join(VECT, "template"), out_dir)
    for junk in ("draft_info.json.bak", "template-2.tmp", "template.tmp"):
        f = os.path.join(out_dir, junk)
        if os.path.exists(f):
            os.remove(f)

    content = json.loads(s.dumps())
    for v in content["materials"]["videos"]:
        if v.get("type") == "photo":
            v["has_audio"] = False
    # add_mask() suy width tu size -> patch lai cho dung so anh chot.
    #
    # LOI THAT 04/08/2026 (toi): vong nay truoc day chay tren MOI mask. Hoi do
    # chi dai B-roll co mask nen khong sao. Toi vua them mask cho LOGO thi no
    # de luon — logo ra mask hinh Split cua dai B-roll (width 0.28, height 0,
    # tam lech xuong -0.842). Chi patch mask cua DAI B-ROLL.
    # ---- NORMALIZE LOUDNESS cho tung doan A-roll ----
    # Thu vien khong co API; nhet thang vao JSON. Doc tu draft anh Thanh da tick
    # tay: moi doan A-roll co mot material `loudness` rieng, enable=true,
    # target_loudness=-14.0. Co toan cuc `normalize_loudness` van la false.
    ld = content["materials"].setdefault("loudnesses", [])
    n_ld = 0
    for tr in content["tracks"]:
        if tr.get("name") != "aroll":
            continue
        for sg in tr.get("segments", []):
            lid = uuid.uuid4().hex.upper()
            ld.append({"id": lid, "enable": True, "time_range": None,
                       "file_id": "", "target_loudness": LOUDNESS_TARGET,
                       "loudness_param": None})
            sg.setdefault("extra_material_refs", []).append(lid)
            n_ld += 1

    for m in content["materials"].get("common_mask", []):
        if m.get("name") != "Split":
            continue                      # mask logo (Rectangle) — de nguyen
        c = m["config"]
        c["width"], c["height"] = MASK_W, MASK_H
        c["centerX"], c["centerY"] = MASK_CENTER_X, MASK_CENTER_Y
        c["feather"], c["roundCorner"], c["rotation"] = MASK_FEATHER, MASK_ROUND, MASK_ROT
    json.dump(content, open(os.path.join(out_dir, "draft_info.json"), "w", encoding="utf-8"),
              ensure_ascii=False)

    png_mb = sum(os.path.getsize(os.path.join(PNG_DIR, f))
                 for f in os.listdir(PNG_DIR)) / 1024 / 1024
    print(f"A-roll  : {len(keeps) if keeps else 1} doan ({a_dur/US:.1f}s)"
          + ("  [tu FILE NGUON — keo lai moi cat duoc]" if keeps else "  [final.mp4 da cat san]"))
    print(f"logo    : {f'co, goc tren trai, {LOGO_SCALE*100:.1f}%, mask bo goc' if logo_ok else 'KHONG CO'}")
    print(f"loudness: normalize {LOUDNESS_TARGET:.0f} LUFS tren {n_ld} doan A-roll")
    print(f"B-roll  : {n_b} doan  (gop {merged} caption dung chung clip -> chay lien mach)")
    if hut:
        print(f"          {len(hut)} doan doi qua het clip, da chinh:")
        for x in hut:
            print(f"            {x}")
    for x in missing:
        print(f"   ! MAT FILE  {x}")
    for x in portrait:
        print(f"   ! CLIP DOC (bo qua, dai can clip ngang)  {x}")
    print(f"caption : {n_c} PNG   (tong {png_mb:.2f} MB)")
    print(f"          animation: " + ", ".join(f"{k} x{v}" for k,v in anim_used.items()))
    print(f"SFX     : {len(cues)}/{len(plan)} cue  ({dict(npool)})  {_sfx.SFX_DB:.0f} dB")
    print(f"-> {out_dir}")

    if "--install" in sys.argv:
        dest = os.path.join(CAPCUT_DRAFTS, NAME)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(out_dir, dest)
        meta_p = os.path.join(dest, "draft_meta_info.json")
        meta = json.load(open(meta_p, encoding="utf-8"))
        now = int(time.time() * US)
        meta.update({"draft_name": NAME, "draft_fold_path": dest,
                     "draft_root_path": CAPCUT_DRAFTS,
                     "draft_id": str(uuid.uuid4()).upper(),
                     "tm_draft_create": now, "tm_draft_modified": now,
                     "tm_duration": content["duration"]})
        json.dump(meta, open(meta_p, "w", encoding="utf-8"), ensure_ascii=False)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", SRC,
                        "-frames:v", "1", "-vf", "scale=360:-1",
                        os.path.join(dest, "draft_cover.jpg")], capture_output=True)
        # ---- NHET MEDIA VAO TRONG THU MUC DRAFT ----
        # CapCut chay trong sandbox. macOS chan Desktop / Documents / Downloads
        # va o ngoai; ~/Movies thi KHONG chan. Ghi thang duong dan Desktop hay
        # /Volumes vao JSON thi CapCut co dia chi nhung khong co "ve" truy cap
        # -> hien "File not accessible" + bat Link media.
        # Cach go: chep media vao chinh thu muc draft (nam trong ~/Movies) roi
        # tro duong dan kieu container — dung dang CapCut tu dung cho material
        # cua no (User Data/Cache/onlineMaterial/...).
        media = os.path.join(dest, "dilim_media")
        os.makedirs(media, exist_ok=True)
        CONT = os.path.expanduser("~/Library/Containers/com.lemon.lvoverseas/Data/Movies")
        MOV = os.path.expanduser("~/Movies")

        moved, cloned, copied = {}, 0, 0
        # LOI 03/08: vong nay truoc chi chay tren "videos" -> file SFX nam
        # tren Desktop khong duoc nhung, dinh dung loi sandbox. Phai gom ca
        # "audios" (va bat ky loai material nao co `path`).
        mats = content["materials"]["videos"] + content["materials"].get("audios", [])
        for v in mats:
            src_p = v.get("path")
            if not src_p or not os.path.exists(src_p):
                continue
            if src_p not in moved:
                name = f"{len(moved):03d}_{os.path.basename(src_p)}"
                dst = os.path.join(media, name)
                # cung o APFS -> `cp -c` clone, ton 0 byte. Khac o -> chep that.
                r = subprocess.run(["cp", "-c", src_p, dst], capture_output=True)
                if r.returncode:
                    shutil.copy2(src_p, dst); copied += 1
                else:
                    cloned += 1
                moved[src_p] = CONT + dst[len(MOV):]
            v["path"] = moved[src_p]

        json.dump(content, open(os.path.join(dest, "draft_info.json"), "w",
                                encoding="utf-8"), ensure_ascii=False)
        sz = sum(os.path.getsize(os.path.join(media, f)) for f in os.listdir(media))
        print(f"  media nhung : {len(moved)} file, {sz/1048576:.0f} MB "
              f"({cloned} clone 0-byte, {copied} chep that)")

        print(f"\nDA CHEP VAO CAPCUT: {dest}")
        print("Thoat han CapCut (Cmd+Q) roi mo lai.")


if __name__ == "__main__":
    main()

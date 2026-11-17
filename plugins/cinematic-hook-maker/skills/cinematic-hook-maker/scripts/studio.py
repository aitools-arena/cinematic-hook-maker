#!/usr/bin/env python3
"""Cinematic Hook Maker production helper (multi-shot work).

hookmaker.py handles a single hook; studio.py handles everything with more than one shot:
multi-shot hooks, one-takes, VFX on existing footage, dialogue scenes, and whole films or episodes.
Keeps one project.json per production and turns it into a storyboard board, a shot list,
an edit list, a cost report, a handoff brief and (with ffmpeg) a rough cut.
Standard library only. Run `python studio.py --help`.
"""
import argparse
import csv
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film_kb as KB  # noqa: E402
import hook_kb as HK  # noqa: E402

MODES = {
    "t2v": "text to video",
    "i2v": "first frame",
    "frames": "first and last frame",
    "keys": "keyframes",
    "r2v": "image references",
    "v2v": "video reference",
}
RATIOS = ["16:9", "9:16", "1:1", "21:9"]
STILL_RATIOS = ["16:9", "9:16", "1:1", "2:3", "3:4", "4:3", "3:2"]
# Limits read from the Artlist connector on 2026-11-17. get_model_config is the authority.
LIMITS = {
    "full": {"min": 3, "max": 30, "end_frame": True, "keys": True, "res": ["720p", "1080p"]},
    "flash": {"min": 3, "max": 20, "end_frame": False, "keys": False, "res": ["720p"]},
    "images": 10,
    "videos": 5,
    "keyframes": 10,
    "prompt": 11000,
}
WORDS_PER_SECOND = 2.5
STAGES = ["still", "draft", "final", "fix"]


# ---------- project file ----------
def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "project"


def find_project(path):
    if path:
        return path if path.endswith(".json") else os.path.join(path, "project.json")
    if os.path.exists("project.json"):
        return "project.json"
    hits = [os.path.join(d, "project.json") for d in sorted(os.listdir(".")) if os.path.isfile(os.path.join(d, "project.json"))]
    if len(hits) == 1:
        return hits[0]
    if hits:
        sys.exit("Several projects found. Pass --project <folder>: " + ", ".join(os.path.dirname(h) for h in hits))
    sys.exit("No project.json found. Run: studio.py init \"Title\"")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, p):
    p["updated"] = now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def get_shot(p, sid):
    for s in p["shots"]:
        if s["id"].lower() == sid.lower():
            return s
    sys.exit(f"No shot {sid}. Shots: " + ", ".join(s["id"] for s in p["shots"]))


def approved_version(s):
    for v in s["versions"]:
        if v["n"] == s.get("approved"):
            return v
    return None


def latest(s, key=None):
    for v in reversed(s["versions"]):
        if key is None or v.get(key):
            return v
    return None


def is_flash(s):
    return "flash" in (s.get("model") or "").lower()


def credits_total(p):
    return sum(v.get("credits") or 0 for s in p["shots"] for v in s["versions"]) + sum(a.get("credits") or 0 for a in p.get("extras", []))


# ---------- commands ----------
def cmd_init(a):
    slug = slugify(a.title)
    folder = a.dir or slug
    os.makedirs(os.path.join(folder, "exports"), exist_ok=True)
    path = os.path.join(folder, "project.json")
    if os.path.exists(path) and not a.force:
        sys.exit(f"{path} already exists. Use --force to replace it.")
    if a.ratio not in RATIOS:
        sys.exit("Ratio must be one of " + ", ".join(RATIOS))
    p = {
        "title": a.title, "slug": slug, "format": a.format, "ratio": a.ratio, "target_seconds": a.length,
        "logline": a.logline or "", "look": a.look or "", "languages": a.languages or [],
        "bible": {"world": "", "threads": [], "episodes": []},
        "cast": [], "locations": [], "style_kit": "", "artlist_folder": "",
        "preferences": {}, "shots": [], "extras": [], "created": now(),
        "genre": "", "lock": {}, "audience": "", "music": "", "style_note": "",
    }
    save(path, p)
    print(f"Created {path}")
    if a.ratio == "21:9":
        print("Note: GPT Image 2.5 has no 21:9. Make stills at 16:9 and crop with: studio.py fit <image> --ratio 21:9")


def cmd_set(a):
    path = find_project(a.project); p = load(path)
    for pair in a.pairs:
        if "=" not in pair:
            sys.exit(f"Use key=value, got: {pair}")
        k, v = pair.split("=", 1)
        if k.startswith("pref."):
            p["preferences"][k[5:]] = v
        elif k.startswith("bible."):
            sub = k[6:]
            if sub in ("threads", "episodes"):
                p["bible"][sub].append(v)
            else:
                p["bible"][sub] = v
        elif k == "target_seconds":
            p[k] = int(v)
        elif k == "hook_no":
            t, line = HK.line_no(int(v))
            if not t:
                sys.exit(f"hook_no must be 1-{HK.count()}; see `studio.py hooks <type>`.")
            p["hook_no"], p["hook_source"], p["story_type"] = int(v), line, t["id"]
            print(f"Library line {v} ({t['id']}): {line}")
        elif k in ("title", "format", "ratio", "logline", "look", "style_kit", "artlist_folder", "audience", "music", "style_note", "genre", "story_type", "hook"):
            p[k] = v
            if k == "hook" and not p.get("hook_no"):
                print("WARNING: set hook_no=<library number> too; a spoken hook must come from references/lines.md.")
        else:
            sys.exit(f"Unknown key {k}. Use title, format, ratio, logline, look, style_kit, artlist_folder, audience, music, style_note, genre, story_type, hook, hook_no, target_seconds, pref.<name>, bible.world, bible.threads, bible.episodes")
    save(path, p); print("Saved.")


def cmd_cast(a):
    path = find_project(a.project); p = load(path)
    kind = "locations" if a.location else "cast"
    entry = {"name": a.name, "role": a.role or "", "traits": a.traits or "", "ref": a.ref or "", "thumb": a.thumb or ""}
    p[kind] = [c for c in p[kind] if c["name"].lower() != a.name.lower()] + [entry]
    save(path, p); print(f"Saved {a.name} to {kind}.")


def cmd_add_shot(a):
    path = find_project(a.project); p = load(path)
    if a.mode not in MODES:
        sys.exit("Mode must be one of " + ", ".join(MODES))
    prompt = a.prompt or ""
    if a.prompt_file:
        with open(a.prompt_file, encoding="utf-8") as f:
            prompt = f.read().strip()
    existing = next((s for s in p["shots"] if s["id"].lower() == a.id.lower()), None)
    shot = existing or {"id": a.id, "versions": [], "approved": None, "status": "planned"}
    shot.update({
        "dur": a.dur, "mode": a.mode, "beat": a.beat or shot.get("beat", ""), "picture": a.picture or shot.get("picture", ""),
        "sound": a.sound or shot.get("sound", ""), "prompt": prompt or shot.get("prompt", ""),
        "model": a.model or shot.get("model", "Kling 4.0"), "images": a.images, "videos": a.videos,
        "keys": a.keys, "end_frame": bool(a.end_frame or a.mode in ("frames", "keys")),
        "variant_of": a.variant_of or shot.get("variant_of", ""), "language": a.language or shot.get("language", ""),
    })
    for key in ("frame", "action", "dialogue", "text"):
        val = getattr(a, key, None)
        if val is not None:
            shot[key] = val
    cam = shot.setdefault("camera", {})
    for key in KB.SHOT_KEYS:
        val = getattr(a, key, None)
        if val is None:
            continue
        cat = "atmo" if key == "atmo" else key
        if val and not KB.find(cat, val):
            sys.exit(f"Unknown {key} '{val}'. See: studio.py vocab {cat}")
        cam[key] = val
    if not existing:
        if a.after:
            idx = next((i for i, s in enumerate(p["shots"]) if s["id"].lower() == a.after.lower()), len(p["shots"]) - 1)
            p["shots"].insert(idx + 1, shot)
        else:
            p["shots"].append(shot)
    save(path, p)
    print(("Updated " if existing else "Added ") + a.id)


def cmd_remove_shot(a):
    path = find_project(a.project); p = load(path)
    s = get_shot(p, a.id)
    if s["versions"] and not a.force:
        sys.exit(f"{a.id} has {len(s['versions'])} logged version(s). Use --force to remove it anyway.")
    p["shots"].remove(s); save(path, p); print(f"Removed {a.id}")


def spoken_words(prompt):
    quoted = re.findall(r'["“«]([^"”»]{2,})["”»]', prompt or "")
    return sum(len(q.split()) for q in quoted)


def validate(p):
    errors, warnings, notes = [], [], []
    if p["ratio"] not in RATIOS:
        errors.append(f"Project ratio {p['ratio']} is not available. Use one of {', '.join(RATIOS)}.")
    for s in p["shots"]:
        sid = s["id"]; lim = LIMITS["flash" if is_flash(s) else "full"]; name = "Kling 4.0 Flash" if is_flash(s) else "Kling 4.0"
        d = s.get("dur")
        if not isinstance(d, int) or d < lim["min"] or d > lim["max"]:
            errors.append(f"{sid}: {d} s is outside {name}'s range of {lim['min']}–{lim['max']} whole seconds.")
        if s["mode"] in ("frames", "keys") or s.get("end_frame"):
            if not lim["end_frame"]:
                errors.append(f"{sid}: {name} takes a first frame only. Use Kling 4.0 for end frames or keyframes.")
        if s.get("images", 0) > LIMITS["images"]:
            errors.append(f"{sid}: {s['images']} reference images. The limit is {LIMITS['images']}.")
        if s.get("videos", 0) > LIMITS["videos"]:
            errors.append(f"{sid}: {s['videos']} reference videos. The limit is {LIMITS['videos']}.")
        if s["mode"] == "r2v" and not s.get("images"):
            errors.append(f"{sid}: mode r2v needs at least one reference image (--images N).")
        if s["mode"] == "v2v" and not s.get("videos"):
            errors.append(f"{sid}: mode v2v needs at least one reference video (--videos N).")
        if s["mode"] == "keys":
            k = s.get("keys") or 0
            if k < 3 or k > LIMITS["keyframes"]:
                errors.append(f"{sid}: keyframe shots take 3 to {LIMITS['keyframes']} keyframes including first and last (--keys N).")
            elif isinstance(d, int) and d < (k - 1) * 3:
                errors.append(f"{sid}: {k} keyframes are rendered as {k - 1} segments of 3 s or more, so the take needs at least {(k - 1) * 3} s. Use fewer keyframes or a longer take.")
            else:
                notes.append(f"{sid}: rendered as {k - 1} start/end-frame segments joined on shared frames (studio.py keyplan --dur {d} --keys {k}).")
        if s.get("images", 0) > 6:
            warnings.append(f"{sid}: {s['images']} reference images. Identities start to blend past six; send only what this shot needs.")
        prompt = s.get("prompt", "")
        if not prompt.strip():
            warnings.append(f"{sid}: no prompt yet.")
        if len(prompt) > LIMITS["prompt"]:
            errors.append(f"{sid}: prompt is {len(prompt)} characters. The limit is {LIMITS['prompt']}.")
        cam = s.get("camera", {})
        for key, val in cam.items():
            if val and not KB.find(key, val):
                errors.append(f"{sid}: unknown {key} '{val}' (studio.py vocab {key}).")
        if s.get("dialogue") and not prompt.strip():
            dw = spoken_words(s["dialogue"]) or len(s["dialogue"].split())
            if isinstance(d, int) and dw / WORDS_PER_SECOND + 1 > d:
                warnings.append(f"{sid}: the dialogue has {dw} words and needs about {dw / WORDS_PER_SECOND + 1:.0f} s; the shot is {d} s.")
        if cam.get("size") == "ecu" and cam.get("intent") == "establish":
            warnings.append(f"{sid}: an extreme close-up cannot establish a space. Use a wide or medium shot.")
        if cam.get("transition") == "handoff" and is_flash(s):
            notes.append(f"{sid}: a hand-off into the next shot works on Flash only as the next shot's first frame; this shot's last frame is not controllable on Flash.")
        words = spoken_words(prompt)
        if words and isinstance(d, int):
            need = words / WORDS_PER_SECOND + 1
            if need > d:
                warnings.append(f"{sid}: {words} spoken words need about {need:.0f} s but the shot is {d} s. Shorten the line or lengthen the shot.")
        if prompt and "subtitle" not in prompt.lower():
            notes.append(f"{sid}: add \"no subtitles\" unless captions are wanted.")
        if prompt and "music" not in prompt.lower():
            notes.append(f"{sid}: say \"no background music\" if the film is scored in the edit.")
        if s["mode"] in ("i2v", "frames", "keys") and p["ratio"] == "21:9":
            notes.append(f"{sid}: framed shots follow the first frame. Crop the still to 21:9 first (studio.py fit).")
    main = [s for s in p["shots"] if not s.get("variant_of")]
    for prev, cur in zip(main, main[1:]):
        a_, b_ = prev.get("camera") or {}, cur.get("camera") or {}
        if a_.get("size") and a_.get("size") == b_.get("size") and a_.get("angle", "eye") == b_.get("angle", "eye"):
            warnings.append(f"{prev['id']} and {cur['id']}: same size and angle back to back reads as a jump cut. Change one (directing.md, section 1).")
    total = sum(s["dur"] for s in p["shots"] if isinstance(s.get("dur"), int) and not s.get("variant_of"))
    target = p.get("target_seconds")
    if target and p["shots"] and abs(total - target) > max(3, target * 0.15):
        warnings.append(f"Shots add up to {total} s; the target is {target} s.")
    sizes = [s for s in p["shots"] if not s.get("variant_of")]
    if len(sizes) >= 4 and len({s["dur"] for s in sizes}) == 1:
        notes.append("Every shot has the same length. Vary the rhythm (see directing.md, section 7).")
    if p.get("hook"):
        hn = p.get("hook_no")
        lang = ((p.get("languages") or ["English"])[0] or "English").lower()
        if not hn and not p.get("preferences", {}).get("hook_custom"):
            errors.append("The hook line has no library number. Choose one from references/lines.md and run `studio.py set hook_no=N`; never write your own line unless the user approved it (`studio.py set pref.hook_custom=yes`).")
        elif hn:
            t, src = HK.line_no(int(hn))
            if t and lang.startswith("en") and not HK.matches(src, p["hook"]):
                errors.append(f"The hook changes more than the [slots] of library line {hn}: \"{src}\".")
            elif t and not lang.startswith("en"):
                notes.append(f"Show library line {hn} \"{src}\" beside the translated hook so the user can see it is faithful.")
    return errors, warnings, notes, total


def cmd_validate(a):
    p = load(find_project(a.project))
    errors, warnings, notes, total = validate(p)
    for label, items in (("ERROR", errors), ("WARNING", warnings), ("NOTE", notes if not a.quiet else [])):
        for it in items:
            print(f"{label}: {it}")
    print(f"{len(p['shots'])} shots, {total} s, {len(errors)} errors, {len(warnings)} warnings.")
    if errors:
        sys.exit(1)


def cmd_log(a):
    path = find_project(a.project); p = load(path)
    s = get_shot(p, a.id)
    if a.version:
        v = next((v for v in s["versions"] if v["n"] == a.version), None)
        if not v:
            sys.exit(f"{a.id} has no version {a.version}.")
    else:
        if a.stage not in STAGES:
            sys.exit("Stage must be one of " + ", ".join(STAGES))
        v = {"n": (s["versions"][-1]["n"] + 1) if s["versions"] else 1, "stage": a.stage, "at": now()}
        s["versions"].append(v)
    for key, val in (("gen", a.gen), ("model", a.model), ("credits", a.credits), ("thumb", a.thumb), ("file", a.file), ("note", a.note)):
        if val is not None:
            v[key] = val
    if a.stage and a.version:
        v["stage"] = a.stage
    if s["status"] in ("planned", "still"):
        s["status"] = "still" if v.get("stage") == "still" else "rendered"
    save(path, p)
    print(f"{a.id} v{v['n']} ({v.get('stage')}) logged. Project total: {credits_total(p):g} credits.")


def cmd_review(a):
    path = find_project(a.project); p = load(path)
    s = get_shot(p, a.id)
    v = next((v for v in s["versions"] if v["n"] == a.version), None) if a.version else latest(s)
    if not v:
        sys.exit(f"{a.id} has no versions to review.")
    v["verdict"] = a.verdict; v["note"] = a.note or v.get("note", "")
    if a.verdict == "approve":
        s["approved"] = v["n"]; s["status"] = "approved"
    elif s.get("approved") != v["n"]:
        s["status"] = "needs fix"
    save(path, p); print(f"{a.id} v{v['n']}: {a.verdict}")


def cmd_approve(a):
    a.verdict = "approve"; a.note = None
    cmd_review(a)


def cmd_log_extra(a):
    path = find_project(a.project); p = load(path)
    p.setdefault("extras", []).append({"kind": a.kind, "label": a.label, "gen": a.gen or "", "credits": a.credits or 0, "file": a.file or "", "at": now()})
    save(path, p); print(f"Logged {a.kind}: {a.label}")


def cmd_status(a):
    p = load(find_project(a.project))
    print(f"{p['title']} · {p['format']} · {p['ratio']} · {len(p['shots'])} shots · {credits_total(p):g} credits")
    for s in p["shots"]:
        v = approved_version(s) or latest(s)
        ver = f"v{v['n']} {v.get('stage', '')}" if v else "-"
        print(f"  {s['id']:<8}{s['dur']:>3} s  {s['mode']:<7}{s['status']:<10}{ver:<12}{s.get('beat', '')[:60]}")


def cmd_keyplan(a):
    """Keyframe times and the start/end-frame segments that join them."""
    if a.keys < 2 or a.keys > LIMITS["keyframes"]:
        sys.exit(f"Use 2 to {LIMITS['keyframes']} keyframes.")
    if a.dur < 3 or a.dur > 30:
        sys.exit("Duration must be 3 to 30 seconds.")
    segs = a.keys - 1
    if a.dur < segs * 3:
        sys.exit(f"{a.keys} keyframes need {segs} segments of 3 s or more, so at least {segs * 3} s. Use fewer keyframes or a longer take.")
    base, extra = divmod(a.dur, segs)
    lengths = [base + (1 if i < extra else 0) for i in range(segs)]
    print(f"{a.keys} keyframes over {a.dur} s as {segs} segment(s): " + ", ".join(f"{n} s" for n in lengths))
    t = 0
    for i, n in enumerate(lengths):
        print(f"  segment {i + 1}: start frame = keyframe {i + 1} (at {t} s), end frame = keyframe {i + 2} (at {t + n} s), duration {n} s")
        t += n
    print("Send the segments together with generate_batch, then join them with: studio.py assemble")


# ---------- exports ----------
def timeline(p):
    t = 0
    for s in p["shots"]:
        if s.get("variant_of"):
            continue
        yield s, t, t + s["dur"]
        t += s["dur"]


def clock(sec):
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


def cmd_export(a):
    path = find_project(a.project); p = load(path)
    out = os.path.join(os.path.dirname(path) or ".", "exports"); os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "shotlist.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "seconds", "job", "picture", "action", "camera", "transition", "dialogue", "on_screen_text", "mode", "model", "status", "approved_version", "generation_id", "file", "sound", "image_prompt", "prompt"])
        for s in p["shots"]:
            v = approved_version(s) or latest(s) or {}
            w.writerow([s["id"], s["dur"], s.get("beat", ""), s.get("frame") or s.get("picture", ""), s.get("action", ""), cam_label(s), (s.get("camera") or {}).get("transition", ""), s.get("dialogue", ""), s.get("text", ""), MODES[s["mode"]], s.get("model", ""), s["status"], s.get("approved") or "", v.get("gen", ""), v.get("file", ""), s.get("sound", ""), s.get("image_prompt", ""), s.get("prompt", "")])
    lines = [f"# Edit list: {p['title']}", "", f"{p['format']} · {p['ratio']} · {clock(sum(s['dur'] for s, _, _ in timeline(p)))} total", "", "| # | Shot | In | Out | Sec | Version | File or generation | Sound |", "|---|---|---|---|---|---|---|---|"]
    for i, (s, t0, t1) in enumerate(timeline(p), 1):
        v = approved_version(s)
        src = (v.get("file") or v.get("gen") or "") if v else "NOT APPROVED"
        lines.append(f"| {i} | {s['id']} | {clock(t0)} | {clock(t1)} | {s['dur']} | {'v' + str(v['n']) if v else '-'} | {src} | {s.get('sound', '')} |")
    variants = [s for s in p["shots"] if s.get("variant_of")]
    if variants:
        lines += ["", "## Language and alternate versions", ""] + [f"- {s['id']} replaces {s['variant_of']}" + (f" ({s['language']})" if s.get("language") else "") for s in variants]
    if p.get("extras"):
        lines += ["", "## Music, voice-over and effects", ""] + [f"- {e['kind']}: {e['label']}" + (f" — {e['file'] or e['gen']}" if e.get("file") or e.get("gen") else "") for e in p["extras"]]
    with open(os.path.join(out, "edit-list.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    by_stage = {}
    rows = []
    for s in p["shots"]:
        spent = sum(v.get("credits") or 0 for v in s["versions"])
        for v in s["versions"]:
            by_stage[v.get("stage", "?")] = by_stage.get(v.get("stage", "?"), 0) + (v.get("credits") or 0)
        rows.append(f"| {s['id']} | {len(s['versions'])} | {'yes' if s.get('approved') else 'no'} | {spent:g} |")
    extra = sum(e.get("credits") or 0 for e in p.get("extras", []))
    attempts = sum(len(s["versions"]) for s in p["shots"]); ok = sum(1 for s in p["shots"] if s.get("approved"))
    cost = [f"# Cost report: {p['title']}", "", f"Total logged: **{credits_total(p):g} credits** across {attempts} generations; {ok} of {len(p['shots'])} shots approved.", "",
            "This counts what was logged in the project. The Artlist usage page is the final word on charges.", "", "## By stage", ""]
    cost += [f"- {k}: {v:g}" for k, v in by_stage.items()] + ([f"- music, voice-over, effects: {extra:g}"] if extra else [])
    cost += ["", "## By shot", "", "| Shot | Attempts | Approved | Credits |", "|---|---|---|---|"] + rows
    with open(os.path.join(out, "cost-report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cost) + "\n")
    print(f"Wrote shotlist.csv, edit-list.md and cost-report.md to {out}")


def cmd_handoff(a):
    path = find_project(a.project); p = load(path)
    L = [f"# Production handoff: {p['title']}", "", "Read this first, confirm in one line what you are continuing, then carry on without asking me to re-explain.", "",
         f"- Format: {p['format']} · {p['ratio']} · target {p.get('target_seconds') or '?'} s", f"- Logline: {p.get('logline') or '-'}", f"- Look: {p.get('look') or '-'}", f"- Story type and hook: {p.get('story_type') or '-'} · {p.get('hook') or '-'}",
         f"- Style kit: {p.get('style_kit') or '-'}", f"- Artlist folder: {p.get('artlist_folder') or '-'}", f"- Languages: {', '.join(p.get('languages') or []) or '-'}", "", "## World", "", p["bible"].get("world") or "-", "", "## Cast", ""]
    L += [f"- **{c['name']}** ({c.get('role') or 'role not set'}): {c.get('traits') or '-'} — reference: {c.get('ref') or 'not saved'}" for c in p["cast"]] or ["-"]
    L += ["", "## Locations", ""] + ([f"- **{c['name']}**: {c.get('traits') or '-'} — reference: {c.get('ref') or 'not saved'}" for c in p.get("locations", [])] or ["-"])
    L += ["", "## How I like to work", ""] + ([f"- {k}: {v}" for k, v in p["preferences"].items()] or ["- nothing recorded yet"])
    L += ["", "## Story so far", ""] + ([f"- {e}" for e in p["bible"].get("episodes", [])] or ["-"])
    L += ["", "## Open threads", ""] + ([f"- {e}" for e in p["bible"].get("threads", [])] or ["-"])
    L += ["", "## Where production stopped", "", "| Shot | Sec | Mode | Status | Approved | Job |", "|---|---|---|---|---|---|"]
    for s in p["shots"]:
        v = approved_version(s)
        L.append(f"| {s['id']} | {s['dur']} | {s['mode']} | {s['status']} | {('v%d %s' % (v['n'], v.get('gen', ''))) if v else '-'} | {s.get('beat', '')} |")
    L += ["", f"Credits logged so far: {credits_total(p):g}"]
    text = "\n".join(L) + "\n"
    out = os.path.join(os.path.dirname(path) or ".", "exports", "handoff.md"); os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text); print(f"(saved to {out})")


# ---------- directing: genre presets, style lock, vocabulary, prompt builder ----------
def word(cat, key):
    item = KB.find(cat, key) if key else None
    return item["words"] if item else ""


def cmd_direct(a):
    path = find_project(a.project); p = load(path)
    if a.list or not a.genre:
        for gid, g in KB.GENRES.items():
            print(f"  {gid:<12}{g['name']:<26}" + " · ".join(f"{k}={g[k]}" for k in ("style", "colour", "light", "move", "lens")))
        return
    g = KB.GENRES.get(a.genre)
    if not g:
        sys.exit("Unknown genre. Choose one of: " + ", ".join(KB.GENRES))
    p["genre"] = a.genre
    p["lock"] = {k: g[k] for k in KB.LOCK_KEYS}
    ids = None if a.shots in (None, "all") else {x.strip().lower() for x in a.shots.split(",")}
    filled = 0
    for sh in p["shots"]:
        if ids is not None and sh["id"].lower() not in ids:
            continue
        cam = sh.setdefault("camera", {})
        for k in ("angle", "move", "pace", "intent"):
            if a.force or not cam.get(k):
                cam[k] = g[k]; filled += 1
    save(path, p)
    print(f"Quick Director: {g['name']}. Style Lock set to " + ", ".join(f"{k}={v}" for k, v in p["lock"].items()) + f". Filled {filled} empty camera fields.")
    print("Shot size is left to each shot's job (the preset's opener is size=" + g["size"] + "). These are starting points; validate flags repeated sizes and angles.")


def cmd_lock(a):
    path = find_project(a.project); p = load(path)
    if a.off:
        p["lock"] = {}; save(path, p); print("Style Lock off."); return
    for pair in a.pairs or []:
        k, _, v = pair.partition("=")
        if k not in KB.LOCK_KEYS:
            sys.exit(f"Style Lock holds {', '.join(KB.LOCK_KEYS)}; camera choices stay per shot.")
        if v and not KB.find(k, v):
            sys.exit(f"Unknown {k} '{v}'. See: studio.py vocab {k}")
        if v:
            p.setdefault("lock", {})[k] = v
        else:
            p.setdefault("lock", {}).pop(k, None)
    save(path, p)
    lk = p.get("lock") or {}
    print("Style Lock: " + (", ".join(f"{k}={v} ({KB.find(k, v)['name']})" for k, v in lk.items()) or "off"))


def cmd_vocab(a):
    cats = [a.category] if a.category else list(KB.LIBRARY)
    for c in cats:
        if c not in KB.LIBRARY:
            sys.exit("Categories: " + ", ".join(KB.LIBRARY))
    if a.write:
        L = ["# Film language library", "",
             f"{KB.count()} techniques. Each has a use (when to choose it) and the words that go into the prompt. "
             "Choose by the shot's job, not by taste. The ids work with `studio.py add-shot`, `lock`, `direct` and `compose`.", "",
             "Generated from `scripts/film_kb.py` by `studio.py vocab --write`. Edit that file, not this one.", "", "## Contents", ""]
        L += [f"{i}. {KB.LIBRARY[c][0]}" for i, c in enumerate(KB.LIBRARY, 1)]
        L += [f"{len(KB.LIBRARY) + 1}. Quick Director presets", f"{len(KB.LIBRARY) + 2}. Scene starters"]
        for c in KB.LIBRARY:
            title, items = KB.LIBRARY[c]
            L += ["", f"## {title}", "", f"Key: `{c}`", ""]
            if c == "atmo":
                L += ["| id | Name | Use it for | In a still | In a video |", "|---|---|---|---|---|"]
                L += [f"| `{x['id']}` | {x['name']} | {x['use']} | {x['still'] or '-'} | {x['motion'] or '-'} |" for x in items]
            else:
                L += ["| id | Name | Use it for | Prompt words |", "|---|---|---|---|"]
                L += [f"| `{x['id']}` | {x['name']} | {x['use']} | {x['words'] or '-'} |" for x in items]
        L += ["", "## Quick Director presets", "", "Starting points per genre (`studio.py direct --genre <id>`). Review every shot afterwards.", "",
              "| genre | style | colour | size | angle | move | light | atmo | lens | pace | intent |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        L += [f"| `{gid}` {g['name']} | " + " | ".join(g[k] for k in ("style", "colour", "size", "angle", "move", "light", "atmo", "lens", "pace", "intent")) + " |" for gid, g in KB.GENRES.items()]
        L += ["", "## Scene starters", "", "One-line scenes for a quick demo, or when the user has no idea yet (`studio.py recipes`).", "", "| Genre | Title | Scene |", "|---|---|---|"]
        L += [f"| {g} | {t} | {d} |" for g, t, d in KB.RECIPES]
        out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "film-language.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
        print(f"Wrote {out}"); return
    for c in cats:
        title, items = KB.LIBRARY[c]
        print(f"\n{title}  [{c}]")
        for x in items:
            print(f"  {x['id']:<13}{x['name']:<22}{x['use']}")


def cmd_hooks(a):
    if a.write:
        sys.exit("references/lines.md is generated by `hookmaker.py write-refs` (one library for both helpers).")
    types = [HK.find(a.type)] if a.type else HK.TYPES
    if a.type and not types[0]:
        sys.exit("Story types: " + ", ".join(t["id"] for t in HK.TYPES))
    nums = {}
    for n, t, line in HK.numbered():
        nums.setdefault(t["id"], []).append((n, line))
    for t in types:
        print(f"\n{t['name']}  [{t['id']}]  {t['use']}")
        if a.type:
            print("  Beats: " + " → ".join(t["beats"]))
            print("  Pictures: " + " | ".join(t["visual"]))
            print("  In fiction: " + t["fiction"])
            for n, line in nums[t["id"]]:
                print(f"  {n}. {line}")


def cmd_recipes(a):
    for g, t, d in KB.RECIPES:
        if not a.genre or a.genre == g:
            print(f"  {g:<12}{t:<20}{d}")


def cast_lines(p, text):
    low = (text or "").lower()
    return [f"{c['name']}: {c['traits']}" for c in p.get("cast", []) + p.get("locations", []) if c["name"].lower() in low and c.get("traits")]


def sentence(x):
    x = (x or "").strip()
    if not x:
        return ""
    x = x[0].upper() + x[1:]
    return x if x[-1] in ".!?\"”" else x + "."


def compose(p, sh):
    lk = p.get("lock") or {}
    cam = dict(sh.get("camera") or {})
    for k in ("light", "atmo", "lens"):
        if not cam.get(k):
            cam[k] = lk.get(k, "")
    look = p.get("look", "")
    # A written look already states medium and colour; the lock's style and colour words would repeat it.
    style, colour = ("", "") if look else (word("style", lk.get("style")), word("colour", lk.get("colour")))
    frame = sh.get("frame") or sh.get("picture") or ""
    action = sh.get("action") or sh.get("beat") or ""
    atmo = KB.find("atmo", cam.get("atmo")) if cam.get("atmo") else None
    framing = ", ".join(x for x in (word("size", cam.get("size")), word("angle", cam.get("angle")), word("lens", cam.get("lens"))) if x)
    light = ("Light: " + word("light", cam.get("light"))) if cam.get("light") else ""
    cont = cast_lines(p, frame + " " + action)
    image = None
    if sh["mode"] in ("i2v", "frames", "keys"):
        parts = [frame, framing, light,
                 ", ".join(x for x in (style, colour, atmo["still"] if atmo else "") if x),
                 ("Look: " + look) if look else "",
                 ("Continuity: " + "; ".join(cont)) if cont else "",
                 "One frozen moment, composed with room for the coming movement; faces and hands unobstructed. No text, no watermark"]
        image = "\n\n".join(sentence(x) for x in parts if x and x.strip())
    sound = [x for x in (sh.get("dialogue"), sh.get("sound")) if x] + ["no background music, no subtitles"]
    text = f'On-screen text: "{sh["text"]}", exactly as written, legible, holding until the end' if sh.get("text") else ""
    move = word("move", cam.get("move"))
    if sh["mode"] in ("i2v", "frames", "keys"):
        lead = "Keep the faces, clothing, set and light of the first frame exactly"
        if sh["mode"] != "i2v":
            lead += "; end exactly on the last frame"
        parts = [lead, action, (move + ", one camera move only") if move else "", word("pace", cam.get("pace")),
                 word("intent", cam.get("intent")), atmo["motion"] if atmo else "", text, "Sound: " + " / ".join(sound)]
    else:
        parts = [frame, action, framing, move, light,
                 ", ".join(x for x in (style, colour, atmo["words"] if atmo else "") if x), ("Look: " + look) if look else "",
                 ("Continuity: " + "; ".join(cont)) if cont else "",
                 word("pace", cam.get("pace")), word("intent", cam.get("intent")), text, "Sound: " + " / ".join(sound)]
    video = "\n\n".join(sentence(x) for x in parts if x and x.strip())
    return image, video


def cmd_compose(a):
    path = find_project(a.project); p = load(path)
    folder = os.path.join(os.path.dirname(path) or ".", "prompts"); os.makedirs(folder, exist_ok=True)
    shots = p["shots"] if a.id == "all" else [get_shot(p, a.id)]
    for sh in shots:
        image, video = compose(p, sh)
        if image:
            with open(os.path.join(folder, f"{sh['id']}-image.txt"), "w", encoding="utf-8") as f:
                f.write(image + "\n")
            if a.apply and (a.force or not sh.get("image_prompt")):
                sh["image_prompt"] = image
        with open(os.path.join(folder, f"{sh['id']}-video.txt"), "w", encoding="utf-8") as f:
            f.write(video + "\n")
        if a.apply and (a.force or not sh.get("prompt")):
            sh["prompt"] = video
        if not a.quiet:
            print(f"===== {sh['id']} · {sh['dur']} s · {MODES[sh['mode']]}")
            if image:
                print("--- first frame (GPT Image 2.5)\n" + image)
            print("--- motion (Kling 4.0)\n" + video + "\n")
    if a.apply:
        save(path, p)
    print(f"Prompt pack written to {folder}" + (" and stored on the shots." if a.apply else ". Add --apply to store them on the shots."))
    print("This is a draft: read each prompt against kling-4.md section 10 and gpt-image-2-5.md section 2 before spending credits.")


# ---------- board ----------
BOARD_CSS = """
:root{--bg:#f6f2ea;--paper:#fffdf9;--card:#fff;--ink:#16181b;--mute:#626973;--line:#e3dccf;--accent:#a8742a;--ok:#1f7a4d;--warn:#9a6a00;--fix:#b8431f;--chip:#efe9de}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#101214;--paper:#15181b;--card:#1b1f23;--ink:#eef0f2;--mute:#a2a9b2;--line:#2b3036;--accent:#e0b36a;--ok:#6fd39c;--warn:#f0c15a;--fix:#ff8a5c;--chip:#23282d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1180px;margin:24px auto;padding:32px 24px 40px;background:var(--paper);border:1px solid var(--line);border-radius:18px}
header{display:grid;gap:8px;border-bottom:1px solid var(--line);padding-bottom:20px}
.kicker{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}
h1{font:600 40px/1.1 "Iowan Old Style","Palatino Linotype",Georgia,serif;margin:0;letter-spacing:-.01em}
.sub{color:var(--mute);max-width:760px}
.info{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-top:12px}
.info div{background:var(--card);padding:10px 14px}.info span{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}.info b{font-weight:600}
.why{margin:20px 0 0;background:var(--chip);border-radius:14px;padding:14px 18px}.why h2{margin:0 0 4px}
h2{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--mute);margin:28px 0 12px;font-weight:600}
.grid{display:grid;gap:16px}.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 1px 2px rgba(0,0,0,.04),0 6px 18px rgba(0,0,0,.05)}
.thumb{position:relative;background:var(--chip);display:flex;align-items:center;justify-content:center;color:var(--mute);font-size:13px;overflow:hidden}.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.num{position:absolute;top:10px;left:10px;width:30px;height:30px;border-radius:50%;border:1.5px solid #fff;color:#fff;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.dur{position:absolute;top:10px;right:10px;background:rgba(0,0,0,.55);color:#fff;border-radius:999px;padding:2px 9px;font-size:12px;font-weight:600}
.body{padding:12px 14px 14px;display:grid;gap:6px}.row{display:flex;justify-content:space-between;gap:8px;align-items:baseline}.id{font-weight:700}.meta{color:var(--mute);font-size:13px}
.st{font-size:12px;font-weight:600;border-radius:999px;padding:2px 10px;background:var(--chip)}.st.approved{color:var(--ok)}.st.fix{color:var(--fix)}.st.rendered,.st.still{color:var(--warn)}
.beat{font-weight:600}.f{font-size:13px}.f b{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);font-weight:600;margin-right:4px}
.line{font-style:italic}.tr{font-size:12px;color:var(--accent);font-weight:600}a{color:var(--accent)}details{font-size:13px}summary{cursor:pointer;color:var(--mute)}pre{white-space:pre-wrap;font:12px/1.5 ui-monospace,Menlo,monospace;margin:8px 0 0}
.cast{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}.person{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;gap:4px}.person img{width:100%;border-radius:8px;display:block}
footer{margin-top:28px;border-top:1px solid var(--line);padding-top:14px;display:flex;flex-wrap:wrap;gap:18px;color:var(--mute);font-size:13px}footer b{color:var(--ink)}
@media (max-width:600px){main{margin:0;border-radius:0;padding:20px 16px}h1{font-size:30px}}
@media print{@page{size:A4 portrait;margin:10mm}body{background:#fff}main{margin:0;border:0;padding:0;max-width:none}.card{break-inside:avoid;box-shadow:none}details{display:none}.grid{grid-template-columns:repeat(4,1fr)!important;gap:8px}.f,.meta{font-size:10px}}
"""


def esc(x):
    return html.escape(str(x or ""))


def link(v):
    src = v.get("file") or ""
    if src:
        return f'<a href="{esc(src)}">open clip</a>'
    return f'<span class="meta">gen {esc(v.get("gen", "")[:8])}…</span>' if v.get("gen") else ""


def cam_label(sh):
    cam = sh.get("camera") or {}
    return " · ".join(KB.find(k, cam[k])["name"] for k in ("size", "angle", "move", "lens") if cam.get(k) and KB.find(k, cam[k]))


def style_label(p, sep):
    lk = p.get("lock") or {}
    return sep.join(KB.find(k, lk[k])["name"] for k in ("style", "colour", "light") if lk.get(k) and KB.find(k, lk[k])) or (p.get("look") or "-")


def board_card(i, s, w, h):
    v = approved_version(s) or latest(s) or {}
    thumb = (approved_version(s) or {}).get("thumb") or (latest(s, "thumb") or {}).get("thumb")
    cls = "approved" if s["status"] == "approved" else "fix" if s["status"] == "needs fix" else s["status"].split()[0]
    pic = f'<img src="{esc(thumb)}" alt="{esc(s["id"])} frame" loading="lazy">' if thumb else "no frame yet"
    tr = (s.get("camera") or {}).get("transition")
    rows = "".join(f'<div class="f"><b>{k}</b>{esc(val)}</div>' for k, val in (("Camera", cam_label(s)), ("Picture", s.get("frame") or s.get("picture")), ("Action", s.get("action"))) if val)
    if s.get("dialogue"):
        rows += f'<div class="f line"><b>Line</b>{esc(s["dialogue"])}</div>'
    if s.get("text"):
        rows += f'<div class="f"><b>Text</b>“{esc(s["text"])}”</div>'
    if s.get("sound"):
        rows += f'<div class="f"><b>Sound</b>{esc(s["sound"])}</div>'
    trans = f'<div class="tr">→ {esc(KB.find("transition", tr)["name"])}</div>' if tr and KB.find("transition", tr) else ""
    ver = (" · v%d of %d" % (v["n"], len(s["versions"]))) if v else ""
    note = f'<div class="meta">Note: {esc(v.get("note"))}</div>' if v.get("note") else ""
    prompts = "\n\n".join(x for x in (s.get("image_prompt"), s.get("prompt")) if x)
    det = f'<details><summary>Prompts</summary><pre>{esc(prompts)}</pre></details>' if prompts else ""
    return (f'<article class="card"><div class="thumb" style="aspect-ratio:{w}/{h}">{pic}<span class="num">{i:02d}</span><span class="dur">{s["dur"]} s</span></div><div class="body">'
            f'<div class="row"><span class="id">{esc(s["id"])}</span><span class="st {cls}">{esc(s["status"])}</span></div>'
            f'<div class="beat">{esc(s.get("beat"))}</div>{rows}{trans}'
            f'<div class="row"><span class="meta">{esc(MODES[s["mode"]])} · {esc(s.get("model"))}{ver}</span>{link(v) if v else ""}</div>{note}{det}</div></article>')


def cmd_board(a):
    path = find_project(a.project); p = load(path)
    w, h = (int(x) for x in p["ratio"].split(":"))
    total = sum(s["dur"] for s, _, _ in timeline(p)); ok = sum(1 for s in p["shots"] if s.get("approved"))
    style_name = style_label(p, " / ")
    cards = "".join(board_card(i, s, w, h) for i, s in enumerate(p["shots"], 1))
    people = ""
    for c in p["cast"] + p.get("locations", []):
        img = f'<img src="{esc(c["thumb"])}" alt="{esc(c["name"])}">' if c.get("thumb") else ""
        people += f'<div class="person">{img}<b>{esc(c["name"])}</b><span class="meta">{esc(c.get("role"))}</span><span class="f">{esc(c.get("traits"))}</span></div>'
    info = [("Duration", clock(total)), ("Format", f'{p["format"]} · {p["ratio"]}'), ("Style", style_name), ("Audience", p.get("audience") or "-"),
            ("Music", p.get("music") or "-")] + ([("Hook", p["hook"])] if p.get("hook") else []) + [("Progress", f"{ok}/{len(p['shots'])} approved · {credits_total(p):g} credits")]
    info_html = "".join(f"<div><span>{k}</span><b>{esc(v)}</b></div>" for k, v in info)
    why = f'<section class="why"><h2>Why this style works</h2><div>{esc(p["style_note"])}</div></section>' if p.get("style_note") else ""
    cast_html = f'<h2>Cast and locations</h2><div class="cast">{people}</div>' if people else ""
    minw = 190 if h > w else 260
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(p["title"])} board</title><style>{BOARD_CSS}</style></head><body><main>'
            f'<header><div class="kicker">Storyboard · {esc(p["format"])}</div><h1>{esc(p["title"])}</h1><div class="sub">{esc(p.get("logline"))}</div>'
            f'<div class="info">{info_html}</div></header>{why}{cast_html}'
            f'<h2>Shots</h2><div class="grid" style="grid-template-columns:repeat(auto-fill,minmax({minw}px,1fr))">{cards or "<p class=sub>No shots yet.</p>"}</div>'
            f'<footer><span><b>{clock(total)}</b> total</span><span><b>{esc(p["ratio"])}</b> {esc(p["format"])}</span><span>{esc(style_name)}</span>'
            f'<span>Updated {esc(p.get("updated"))} · Director\'s Desk</span></footer></main></body></html>')
    out = os.path.join(os.path.dirname(path) or ".", "board.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Wrote {out}  (print to PDF for an A4 client board)")


def clip(text, n):
    text = (text or "").strip()
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def cmd_pitchboard(a):
    path = find_project(a.project); p = load(path)
    total = sum(s["dur"] for s, _, _ in timeline(p))
    style_name = style_label(p, ", ")
    shots = [s for s in p["shots"] if not s.get("variant_of")][: a.panels]
    cols = 2 if len(shots) <= 8 else 3
    rows = -(-len(shots) // cols)
    panels = []
    for i, s in enumerate(shots, 1):
        bits = [f"Panel {i} ({s['dur']} s): {s.get('frame') or s.get('picture') or s.get('beat')}"]
        if cam_label(s):
            bits.append(f"camera: {cam_label(s)}")
        if s.get("action"):
            bits.append(f"action: {s['action']}")
        if s.get("dialogue"):
            bits.append(f"line: {s['dialogue']}")
        if s.get("text"):
            bits.append(f'on-screen text: "{s["text"]}"')
        tr = (s.get("camera") or {}).get("transition")
        if tr and KB.find("transition", tr):
            bits.append(f"transition: {KB.find('transition', tr)['name']}")
        panels.append("; ".join(b.strip().rstrip(".") for b in bits) + ".")
    refs = ("The input images are the approved character sheets and keyframes: use them for every face, costume and set so the panels match the film. " if a.with_refs else "")
    why = f' Beside it, a small rounded box headed "WHY THIS STYLE WORKS" with one sentence: "{clip(p["style_note"], 160)}".' if p.get("style_note") else ""
    lines = [
        f"A single-page storyboard presentation board, A4 portrait, laid out like a printed pitch document from a film production company. {refs}",
        f'Layout: warm off-white paper with a thin beige border and generous, equal margins. At the top, a large elegant serif title "{p["title"]}" and one line beneath it: "{clip(p.get("logline"), 160)}". Under the title, a slim information bar with four labelled cells: "DURATION {clock(total)}", "STYLE {clip(style_name, 44)}", "AUDIENCE {clip(p.get("audience") or "General", 30)}", "MUSIC {clip(p.get("music") or "Score in the edit", 30)}".{why}',
        f"Below, {len(shots)} storyboard panels in a {cols} by {rows} grid of white rounded cards with soft shadows. Each card has a {p['ratio']} picture on top showing the panel's moment as a realistic film frame, a scene number in a small white outlined circle at the picture's top-left, a duration badge at its top-right, and two or three short lines of small clean sans-serif text under the picture: camera, action, and any line of dialogue.",
        "\n".join(panels),
        f'Footer: a thin rule, then small text: "{clock(total)} · {p["ratio"]} · {p["format"]}".',
        "The pictures in the panels are realistic photographs from the film: one physical light source per scene, natural skin texture, neutral colour, the same faces and costumes in every panel. Typography is crisp and correctly spelled. No extra logos, no watermark.",
    ]
    prompt = "\n\n".join(lines)
    out = os.path.join(os.path.dirname(path) or ".", "exports", "pitchboard-prompt.txt"); os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(prompt + "\n")
    print(prompt); print(f"\n(saved to {out})")
    print("Render with GPT Image 2.5 at 3:4 or 2:3, quality high, 2K. Small text can come out wrong: check the spelling before sharing; board.html is the exact version.")


# ---------- media helpers ----------
def need(tool):
    if not shutil.which(tool):
        sys.exit(f"{tool} is not installed, so this step can't run here. Use the edit list instead, or install {tool}.")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("Command failed: " + " ".join(cmd[:3]) + " …\n" + r.stderr[-600:])
    return r.stdout


def cmd_fit(a):
    w, h = (float(x) for x in a.ratio.split(":"))
    target = w / h
    root, ext = os.path.splitext(a.image)
    out = a.out or f"{root}_{a.ratio.replace(':', 'x')}{ext or '.png'}"
    try:
        from PIL import Image  # optional
        im = Image.open(a.image); iw, ih = im.size
        if iw / ih > target:
            nw = round(ih * target); x = round((iw - nw) * a.x); box = (x, 0, x + nw, ih)
        else:
            nh = round(iw / target); y = round((ih - nh) * a.y); box = (0, y, iw, y + nh)
        im.crop(box).save(out)
    except ImportError:
        need("ffmpeg")
        vf = f"crop='if(gt(iw/ih,{target}),ih*{target},iw)':'if(gt(iw/ih,{target}),ih,iw/{target})':'(iw-ow)*{a.x}':'(ih-oh)*{a.y}'"
        run(["ffmpeg", "-y", "-i", a.image, "-vf", vf, "-frames:v", "1", out])
    print(f"Wrote {out}")


def cmd_trim(a):
    need("ffmpeg")
    root, ext = os.path.splitext(a.video)
    out = a.out or f"{root}_trim{ext or '.mp4'}"
    run(["ffmpeg", "-y", "-ss", str(a.start), "-i", a.video, "-t", str(a.dur), "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", out])
    print(f"Wrote {out} ({a.dur} s from {a.start} s)")


def cmd_assemble(a):
    need("ffmpeg")
    path = find_project(a.project); p = load(path)
    base = os.path.dirname(path) or "."
    clips, missing = [], []
    for s, _, _ in timeline(p):
        v = approved_version(s)
        f = v.get("file") if v else None
        full = f if f and os.path.isabs(f) else os.path.join(base, f) if f else None
        (clips if full and os.path.exists(full) else missing).append(full or s["id"])
    if missing:
        sys.exit("These shots have no approved local clip (download them and log with --file): " + ", ".join(os.path.basename(m) for m in missing))
    size = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080), "21:9": (2520, 1080)}[p["ratio"]]
    out_dir = os.path.join(base, "exports"); os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "cut.mp4")
    cmd = ["ffmpeg", "-y"]
    for c in clips:
        cmd += ["-i", c]
    n = len(clips)
    # Keep the clips' own frame rate; converting it makes joined takes judder.
    rate = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", clips[0]]).strip().split("\n")[0] or "24"
    num, _, den = rate.partition("/")
    fps = float(num) / float(den or 1)
    lengths = [float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", c]).strip() or 0) for c in clips]
    keep = a.keep_audio or not a.music
    has_audio = [bool(run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", c]).strip()) for c in clips] if keep else []
    parts = []
    for i in range(n):
        # In a chained take each clip starts on the frame the previous one ended on; drop that repeat.
        cutv = "trim=start_frame=1,setpts=PTS-STARTPTS," if a.chain and i else ""
        cuta = f"atrim=start={1 / fps:.5f},asetpts=PTS-STARTPTS," if a.chain and i else ""
        parts.append(f"[{i}:v]{cutv}scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease,pad={size[0]}:{size[1]}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={rate},format=yuv420p[v{i}]")
        if keep:
            parts.append((f"[{i}:a]{cuta}aresample=48000,aformat=channel_layouts=stereo[a{i}]") if has_audio[i] else f"anullsrc=r=48000:cl=stereo,atrim=0:{lengths[i]}[a{i}]")
    if keep:
        parts.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][dia]")
    else:
        parts.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]")
    maps = ["-map", "[v]"]
    if a.music:
        cmd += ["-i", a.music]
        if keep:
            parts.append(f"[{n}:a]volume=0.25[mus];[dia][mus]amix=inputs=2:duration=first:dropout_transition=0[a]")
        else:
            parts.append(f"[{n}:a]volume=0.9[a]")
        maps += ["-map", "[a]", "-shortest"]
    elif keep:
        maps += ["-map", "[dia]"]
    cmd += ["-filter_complex", ";".join(parts)] + maps + ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    run(cmd)
    print(f"Wrote {out} — a rough cut with straight cuts, {n} shots, {sum(lengths):.1f} s at {rate} fps.")


# ---------- cli ----------
def main():
    ap = argparse.ArgumentParser(description="Cinematic Hook Maker production helper (multi-shot)")
    ap.add_argument("--project", help="project folder or project.json (default: found automatically)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="start a project"); s.add_argument("title")
    s.add_argument("--format", default="short film"); s.add_argument("--ratio", default="16:9"); s.add_argument("--length", type=int, help="target seconds")
    s.add_argument("--logline"); s.add_argument("--look"); s.add_argument("--languages", nargs="*"); s.add_argument("--dir"); s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_init)

    s = sub.add_parser("set", help="set project fields: key=value …"); s.add_argument("pairs", nargs="+"); s.set_defaults(fn=cmd_set)

    s = sub.add_parser("cast", help="save a character or location"); s.add_argument("name"); s.add_argument("--role"); s.add_argument("--traits"); s.add_argument("--ref", help="Artlist saved reference or generation ID")
    s.add_argument("--thumb"); s.add_argument("--location", action="store_true"); s.set_defaults(fn=cmd_cast)

    s = sub.add_parser("add-shot", help="add or update a shot"); s.add_argument("--id", required=True); s.add_argument("--dur", type=int, required=True); s.add_argument("--mode", default="i2v")
    s.add_argument("--beat"); s.add_argument("--picture"); s.add_argument("--sound"); s.add_argument("--prompt"); s.add_argument("--prompt-file"); s.add_argument("--model")
    s.add_argument("--images", type=int, default=0); s.add_argument("--videos", type=int, default=0); s.add_argument("--keys", type=int, default=0); s.add_argument("--end-frame", action="store_true")
    s.add_argument("--variant-of"); s.add_argument("--language"); s.add_argument("--after")
    s.add_argument("--frame", help="what the first frame shows, before any action"); s.add_argument("--action", help="what happens, in order")
    s.add_argument("--dialogue", help="speaker, voice and the line in quotes"); s.add_argument("--text", help="on-screen text, exact words")
    for k in KB.SHOT_KEYS:
        s.add_argument("--" + k, help=f"id from: studio.py vocab {k}")
    s.set_defaults(fn=cmd_add_shot)
    s = sub.add_parser("direct", help="Quick Director: genre preset for Style Lock and empty camera fields"); s.add_argument("--genre"); s.add_argument("--shots", help="all (default) or S01,S03")
    s.add_argument("--force", action="store_true", help="overwrite camera fields already set"); s.add_argument("--list", action="store_true"); s.set_defaults(fn=cmd_direct)
    s = sub.add_parser("lock", help="Style Lock: hold style, colour, light, atmosphere and lens across shots"); s.add_argument("pairs", nargs="*"); s.add_argument("--off", action="store_true"); s.set_defaults(fn=cmd_lock)
    s = sub.add_parser("vocab", help="film-language library"); s.add_argument("category", nargs="?"); s.add_argument("--write", action="store_true", help="regenerate references/film-language.md"); s.set_defaults(fn=cmd_vocab)
    s = sub.add_parser("hooks", help="story types and opening hooks"); s.add_argument("type", nargs="?"); s.add_argument("--write", action="store_true", help="(moved to hookmaker.py write-refs)"); s.set_defaults(fn=cmd_hooks)
    s = sub.add_parser("recipes", help="one-line scene starters"); s.add_argument("--genre"); s.set_defaults(fn=cmd_recipes)
    s = sub.add_parser("compose", help="build first-frame and motion prompts from the shot card"); s.add_argument("id", help="shot id or all"); s.add_argument("--apply", action="store_true", help="store on the shots")
    s.add_argument("--force", action="store_true"); s.add_argument("--quiet", action="store_true"); s.set_defaults(fn=cmd_compose)
    s = sub.add_parser("pitchboard", help="GPT Image prompt for a one-page A4 storyboard presentation"); s.add_argument("--panels", type=int, default=8)
    s.add_argument("--with-refs", action="store_true", help="the render will receive approved sheets and keyframes as input images"); s.set_defaults(fn=cmd_pitchboard)

    s = sub.add_parser("remove-shot"); s.add_argument("id"); s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_remove_shot)
    s = sub.add_parser("validate", help="check every shot against model limits"); s.add_argument("--quiet", action="store_true"); s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("log", help="record a generation against a shot"); s.add_argument("id"); s.add_argument("--stage", help="still, draft, final or fix"); s.add_argument("--gen"); s.add_argument("--model")
    s.add_argument("--credits", type=float); s.add_argument("--thumb"); s.add_argument("--file"); s.add_argument("--note"); s.add_argument("--version", type=int, help="update this version instead of adding one"); s.set_defaults(fn=cmd_log)

    s = sub.add_parser("review"); s.add_argument("id"); s.add_argument("--version", type=int); s.add_argument("--verdict", required=True, choices=["approve", "fix", "reject"]); s.add_argument("--note"); s.set_defaults(fn=cmd_review)
    s = sub.add_parser("approve"); s.add_argument("id"); s.add_argument("--version", type=int); s.set_defaults(fn=cmd_approve)
    s = sub.add_parser("log-extra", help="record music, voice-over or an effect"); s.add_argument("kind", choices=["music", "voiceover", "sfx", "other"]); s.add_argument("label"); s.add_argument("--gen"); s.add_argument("--credits", type=float); s.add_argument("--file"); s.set_defaults(fn=cmd_log_extra)
    s = sub.add_parser("status"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("keyplan", help="even keyframe timing for a long take"); s.add_argument("--dur", type=int, required=True); s.add_argument("--keys", type=int, required=True); s.set_defaults(fn=cmd_keyplan)
    s = sub.add_parser("board", help="write board.html"); s.set_defaults(fn=cmd_board)
    s = sub.add_parser("export", help="write shot list, edit list and cost report"); s.set_defaults(fn=cmd_export)
    s = sub.add_parser("handoff", help="brief for the next episode or conversation"); s.set_defaults(fn=cmd_handoff)
    s = sub.add_parser("fit", help="crop a still to a ratio"); s.add_argument("image"); s.add_argument("--ratio", required=True); s.add_argument("--x", type=float, default=0.5); s.add_argument("--y", type=float, default=0.5); s.add_argument("--out"); s.set_defaults(fn=cmd_fit)
    s = sub.add_parser("trim", help="cut a reference clip (ffmpeg)"); s.add_argument("video"); s.add_argument("--start", type=float, default=0); s.add_argument("--dur", type=float, required=True); s.add_argument("--out"); s.set_defaults(fn=cmd_trim)
    s = sub.add_parser("assemble", help="join approved clips into a rough cut (ffmpeg)"); s.add_argument("--music"); s.add_argument("--keep-audio", action="store_true"); s.add_argument("--chain", action="store_true", help="clips are segments of one take that share frames: drop the repeated frame at each join"); s.set_defaults(fn=cmd_assemble)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

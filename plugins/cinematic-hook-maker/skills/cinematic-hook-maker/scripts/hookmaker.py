#!/usr/bin/env python3
"""The Hook Maker helper.

Keeps one hook.json per video: the brief, the hook concepts, the prompts, every
generation, and the chosen hook. Builds prompts, checks timing and safe zones,
burns accurate on-screen text into a clip, crops for feed ratios and exports a
hook pack. Standard library only; ffmpeg and a Chrome-family browser are optional.
Run `python hookmaker.py --help`.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_data as HD  # noqa: E402
import story_types as ST  # noqa: E402

WPS = 2.5  # spoken words per second
LIMITS = {"flash": (3, 20), "full": (3, 30)}
KLING_RATIOS = ["16:9", "9:16", "1:1", "21:9"]
STILL_RATIO = {"9:16": "9:16", "16:9": "16:9", "1:1": "1:1", "21:9": "16:9"}
REALISM = ("Unretouched photograph from a real camera, written as a picture that was actually taken: "
           "one named physical light source with real shadows; a person in frame is attractive and well groomed "
           "(concrete features, groomed brows, light makeup when it fits) with the face in open shade or bounced light; "
           "fine skin texture with pores visible up close, a faint natural sheen on the nose and cheekbones, a few flyaway hairs, tiny natural asymmetry; "
           "natural fabric creases, real worn surfaces; relaxed and unposed, lips softly closed, calm confident expression, no posed model smile; "
           "neutral true-to-life colour, no colour grading, highlights slightly clipped on the brightest skin, soft natural contrast. No text, no watermark.")


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "hook"


def find(path):
    if path:
        return path if path.endswith(".json") else os.path.join(path, "hook.json")
    if os.path.exists("hook.json"):
        return "hook.json"
    hits = [os.path.join(d, "hook.json") for d in sorted(os.listdir(".")) if os.path.isfile(os.path.join(d, "hook.json"))]
    if len(hits) == 1:
        return hits[0]
    sys.exit("Pass --project <folder>." if hits else 'No hook.json here. Run: hookmaker.py start "Video title" --platform tiktok --type tutorial')


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, h):
    h["updated"] = now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(h, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def concept(h, cid):
    for c in h["concepts"]:
        if c["id"].lower() == cid.lower():
            return c
    sys.exit(f"No concept {cid}. Concepts: " + (", ".join(c["id"] for c in h["concepts"]) or "none"))


def words(text):
    return len(re.findall(r"[\w'’-]+", text or ""))


def credits(h):
    return sum(v.get("credits") or 0 for c in h["concepts"] for v in c["versions"]) + sum(x.get("credits") or 0 for x in h.get("extras", []))


# ---------- start and browse ----------
def cmd_start(a):
    if a.platform and a.platform not in HD.PLATFORMS:
        sys.exit("Platform: " + ", ".join(HD.PLATFORMS))
    if a.type and a.type not in HD.GENRES:
        sys.exit("Type: " + ", ".join(HD.GENRES))
    folder = a.dir or slug(a.title)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "hook.json")
    if os.path.exists(path) and not a.force:
        sys.exit(f"{path} exists. Use --force to replace it.")
    pf = HD.PLATFORMS.get(a.platform or "")
    h = {"title": a.title, "platform": a.platform or "", "type": a.type or "", "about": a.about or "", "audience": a.audience or "",
         "language": a.language or "", "presenter": a.presenter or "", "product": a.product or "", "cta": a.cta or "",
         "ratio": a.ratio or (pf["render"] if pf else ""), "deliver": pf["deliver"] if pf else "", "look": a.look or "", "artlist_folder": "",
         "concepts": [], "chosen": "", "extras": [], "guide": {"done": []}, "created": now()}
    h["chat_language"] = a.chat_language or ""
    lm = HD.market_for_language(a.language or a.chat_language)
    if lm:
        h["market"], h["market_source"] = lm, f"language ({a.language or a.chat_language})"
    else:
        h["market"], h["market_source"] = detect_market(load_prefs(path))
    for k in ("platform", "type", "language", "presenter", "look"):  # "about" is always confirmed in the guide
        if getattr(a, k):
            h["guide"]["done"].append(GUIDE_KEY.get(k, k))
    if h["ratio"] and h["ratio"] not in KLING_RATIOS:
        sys.exit("Render ratio must be one of " + ", ".join(KLING_RATIOS))
    save(path, h)
    print(f"Created {path}")
    if not (pf and a.type):
        print("Brief not finished. Next: hookmaker.py guide")
        return
    g = HD.GENRES[a.type]
    print(f"{pf['name']} · render {h['ratio']} · deliver {pf['deliver']} · hook window {pf['window']}")
    print(f"Hook job for {g['name']}: {g['job']}")
    print("Start with story types: " + ", ".join(g["stories"]) + "\nVisual formats: " + ", ".join(g["formats"]))
    print("Care: " + g["care"])


SET_KEYS = ("title", "about", "audience", "language", "presenter", "product", "cta", "look", "look_id", "artlist_folder", "ratio",
            "platform", "type", "direction", "text_style", "text_pos", "sound", "dur", "plan", "photos",
            "market", "audience_gender", "audience_age", "model_gender", "model_look")


def apply_value(h, k, v):
    if k not in SET_KEYS:
        sys.exit("Keys: " + ", ".join(SET_KEYS))
    if k == "platform":
        if v not in HD.PLATFORMS:
            sys.exit("Platform: " + ", ".join(HD.PLATFORMS))
        h["ratio"], h["deliver"] = HD.PLATFORMS[v]["render"], HD.PLATFORMS[v]["deliver"]
    if k == "type" and v not in HD.GENRES:
        sys.exit("Type: " + ", ".join(HD.GENRES))
    if k == "ratio" and v not in KLING_RATIOS:
        sys.exit("Render ratio must be one of " + ", ".join(KLING_RATIOS))
    if k == "presenter" and v not in PRESENTERS:
        sys.exit("Presenter: " + ", ".join(PRESENTERS))
    if k == "look_id":
        if v not in HD.LOOKS:
            sys.exit("Looks: " + ", ".join(HD.LOOKS))
        h["look"] = HD.LOOKS[v]["look"]
    if k == "direction" and v != "auto" and not HD.fmt(v):
        sys.exit("Direction: auto or a format id: " + ", ".join(f["id"] for f in HD.FORMATS))
    if k == "text_style" and v not in HD.TEXT_STYLES:
        sys.exit("Text style: " + ", ".join(HD.TEXT_STYLES))
    if k == "text_pos" and v not in ("top", "middle", "bottom"):
        sys.exit("Text position: top, middle, bottom")
    if k == "sound" and v not in HD.SOUNDS:
        sys.exit("Sound: " + ", ".join(HD.SOUNDS))
    if k == "plan" and v not in HD.PLANS:
        sys.exit("Plan: " + ", ".join(HD.PLANS))
    if k == "market":
        v = v.upper()
        if v == "?":
            sys.exit("Markets: " + ", ".join(f"{c} ({m['name']})" for c, m in HD.MARKETS.items()))
        if v not in HD.MARKETS:
            sys.exit("Market: " + ", ".join(HD.MARKETS))
        h["market_source"] = "chosen"
    if k in ("audience_gender", "model_gender") and v not in [g for g, _ in HD.GENDERS]:
        sys.exit("Gender: female, male, all")
    if k == "model_gender" and v == "all":
        sys.exit("A model is one person: female or male")
    if k == "audience_age" and v not in [a for a, _ in HD.AGES]:
        sys.exit("Age: " + ", ".join(a for a, _ in HD.AGES))
    if k == "language" and h.get("market_source") != "chosen" and HD.market_for_language(v):
        h["market"], h["market_source"] = HD.market_for_language(v), f"language ({v})"
    if k == "model_look" and v not in HD.RACES:
        sys.exit("Looks: " + ", ".join(HD.RACES))
    if k == "dur":
        try:
            v = int(v)
        except ValueError:
            sys.exit("dur is whole seconds, 3–8 for a hook")
        if not 3 <= v <= 30:
            sys.exit("dur must be 3–30 s (hooks land in 3–6 s)")
    h[k] = v
    if k in ("audience_gender", "audience_age", "market") and h.get("audience_gender"):
        gname = dict(HD.GENDERS)[h["audience_gender"]]
        h["audience"] = f"{gname if h['audience_gender'] != 'all' else 'Men and women'} {h.get('audience_age') or ''} in {HD.market(h.get('market'))['name']}".replace("  ", " ")
    if k in ("model_gender", "model_look") and h.get("model_gender") and h.get("model_look"):
        look = HD.RACES.get(h["model_look"], (h["model_look"], ""))
        age = {"18-24": "early twenties", "25-34": "late twenties", "35-44": "late thirties", "45+": "late forties"}.get(h.get("audience_age") or "", "early twenties")
        h["casting"] = (f"New AI model: {look[0]} {'woman' if h['model_gender'] == 'female' else 'man'} in their {age}"
                        + (f", {look[1]}" if look[1] else "") + "; casting photo then character sheet before the hook")
    done = h.setdefault("guide", {"done": []})["done"]
    step = GUIDE_KEY.get(k)
    if step and step not in done:
        done.append(step)


def cmd_set(a):
    path = find(a.project); h = load(path)
    for pair in a.pairs:
        k, _, v = pair.partition("=")
        apply_value(h, k, v)
    save(path, h); print("Saved.")
    if guide_next(h):
        print("Next: hookmaker.py guide")


# ---------- guided brief ----------
PRESENTERS = ("none", "user", "ai", "product", "user+product", "ai+product")
PREFS = "hookmaker-prefs.json"
PREF_KEYS = ("platform", "language", "audience_gender", "audience_age", "model_gender", "model_look", "look_id", "text_style", "text_pos", "sound", "plan", "dur", "presenter")
# step id, title, the hook.json keys it fills
GUIDE = [
    ("platform", "Format (aspect ratio)", ["platform"]),
    ("type", "Video type", ["type"]),
    ("about", "What the video delivers", ["about"]),
    ("language", "Language", ["language"]),
    ("audience", "Audience", ["audience_gender", "audience_age"]),
    ("people", "Who or what is on screen", ["presenter", "product", "photos"]),
    ("model", "AI model", ["model_gender", "model_look"]),
    ("look", "Look", ["look_id"]),
    ("direction", "Hook direction", ["direction"]),
    ("text", "On-screen text", ["text_style", "text_pos"]),
    ("sound", "Sound", ["sound"]),
    ("render", "Length and render plan", ["dur", "plan"]),
]
GUIDE_KEY = {keys[0]: sid for sid, _, keys in GUIDE}  # only a step's main key closes it
GUIDE_KEY["look"] = "look"


def prefs_path(path):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), PREFS)


def load_prefs(path):
    try:
        return load(prefs_path(path))
    except (OSError, ValueError):
        return {}


def detect_market(prefs=None):
    """The target market follows where the user is: a saved choice, else this device's region."""
    if os.environ.get("HOOK_MARKET"):
        return os.environ["HOOK_MARKET"].upper(), "HOOK_MARKET"
    if (prefs or {}).get("market"):
        return prefs["market"], "saved choice"
    try:
        loc = subprocess.run(["defaults", "read", "-g", "AppleLocale"], capture_output=True, text=True, timeout=3).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        loc = ""
    loc = loc or os.environ.get("LC_ALL") or os.environ.get("LANG") or ""
    m = re.search(r"[_-]([A-Z]{2})\b", loc)
    if m and m.group(1) in HD.MARKETS:
        return m.group(1), f"device region ({loc})"
    try:
        tz = os.path.realpath("/etc/localtime").split("zoneinfo/")[-1]
    except OSError:
        tz = ""
    if tz in HD.TZ_MARKET:
        return HD.TZ_MARKET[tz], f"device time zone ({tz})"
    if tz.startswith("America/"):
        return "US", f"device time zone ({tz})"
    return "GLOBAL", "no region found"


def step_applies(h, sid):
    if sid == "model":
        return "ai" in (h.get("presenter") or "")
    return True


def guide_next(h):
    done = h.get("guide", {}).get("done", [])
    return next((st for st in GUIDE if st[0] not in done and step_applies(h, st[0])), None)


def guide_options(h, sid, prefs):
    """Options as (value, label, what it sets), first one is the default."""
    pf = HD.PLATFORMS.get(h.get("platform") or "")
    vt = h.get("type") or ""
    if sid == "platform":
        opts = [(k, g["name"], g["label"] + f"; render {HD.PLATFORMS[k]['render']}"
                 + (f", delivered {HD.PLATFORMS[k]['deliver']} (cropped)" if HD.PLATFORMS[k]["deliver"] != HD.PLATFORMS[k]["render"] else "")
                 + "; text kept clear of every platform's buttons in this group") for k, g in HD.GROUPS.items()]
    elif sid == "type":
        opts = [(k, g["name"], g["job"]) for k, g in HD.GENRES.items()]
    elif sid == "about":
        return [], f"Free text: the content in one or two sentences and its payoff. Current: {h.get('about') or '(empty)'}"
    elif sid == "language":
        mk = HD.market(h.get("market"))
        langs = list(dict.fromkeys(x for x in [h.get("chat_language"), mk["language"], prefs.get("language"), "English"] if x))
        opts = [(l, l, f"spoken line and on-screen text in {l}; target market {HD.market(HD.market_for_language(l) or h.get('market'))['name']}") for l in langs]
        opts.append(("other", "Another language", "name it; Kling 4.0 speaks several languages"))
    elif sid == "audience":
        mk = HD.market(h.get("market"))
        opts = [(g, label, ("viewers of all genders" if g == "all" else f"{label.lower()} viewers") + f" in {mk['name']}") for g, label in HD.GENDERS]
        return opts, "ages: " + ", ".join(a for a, _ in HD.AGES)
    elif sid == "model":
        mk = HD.market(h.get("market"))
        opts = [(r, HD.RACES[r][0], HD.RACES[r][1] or "") for r in HD.races_for(h.get("market"))]
        first = "male" if h.get("audience_gender") == "male" else "female"
        return opts, f"gender: {first}, {'female' if first == 'male' else 'male'} · looks ordered for {mk['name']}, all {len(HD.RACES)} always available"
    elif sid == "people":
        opts = [("ai+product", "AI model + your product", "casting photo first (section 6), product from your photo"),
                ("product", "Product only", "the product from your photo, no person"),
                ("user", "You on camera", "send 2–3 clear photos of your face"),
                ("user+product", "You + your product", "your photos and the product photo"),
                ("ai", "AI presenter or character", "casting photo first, saved for later hooks"),
                ("none", "Nobody, a scene or object", "pure visual hook")]
        if vt in ("tutorial", "explainer", "commentary", "podcast", "vlog", "story"):
            opts.sort(key=lambda o: o[0] not in ("user", "ai", "none"))
    elif sid == "look":
        opts = [(k, HD.LOOKS[k]["name"], HD.LOOKS[k]["look"]) for k in HD.looks_for(vt)]
    elif sid == "direction":
        g = HD.GENRES.get(vt)
        fav = g["formats"] if g else []
        opts = [("auto", "Let the director propose 3 concepts", "three different approaches, scored, you pick one")]
        opts += [(f["id"], f["name"], f["what"]) for f in sorted(HD.FORMATS, key=lambda f: f["id"] not in fav)[:6]]
    elif sid == "text":
        opts = [("box/top", "Box, top", HD.TEXT_STYLES["box"] + ", one line in the upper safe zone, clear of the face"),
                ("outline/top", "Outline, top", HD.TEXT_STYLES["outline"] + ", upper safe zone"),
                ("box/middle", "Box, middle", HD.TEXT_STYLES["box"] + ", centre of the frame"),
                ("none/top", "No text", "picture and sound only" + (" (viewers watching muted miss the hook)" if pf and "muted" in pf["sound"].lower() else ""))]
    elif sid == "sound":
        order = ["spoken", "voiceover", "music", "silent"]
        if pf and "muted" in pf["sound"].lower():
            order = ["spoken", "music", "voiceover", "silent"]
        opts = [(k, k.capitalize(), HD.SOUNDS[k]) for k in order]
    elif sid == "render":
        opts = [("4/draft-final", "4 s · draft then final", HD.PLANS["draft-final"]),
                ("3/draft-final", "3 s · draft then final", "shortest hook; " + HD.PLANS["draft-final"]),
                ("6/draft-final", "6 s · draft then final", "room for a transformation or a reveal"),
                ("4/draft-only", "4 s · draft only", HD.PLANS["draft-only"])]
    else:
        opts = []
    # the user's usual choice goes first
    keys = next(st[2] for st in GUIDE if st[0] == sid)
    usual = "/".join(str(prefs.get(k)) for k in keys if prefs.get(k) is not None)
    if sid == "people":
        usual = prefs.get("presenter") or ""
    if sid == "render" and prefs.get("dur") and prefs.get("plan"):
        usual = f"{prefs['dur']}/{prefs['plan']}"
    if sid == "text" and prefs.get("text_style"):
        usual = f"{prefs['text_style']}/{prefs.get('text_pos', 'top')}"
    if sid == "language":
        usual = prefs.get("language") or ""
    if sid == "audience":
        usual = prefs.get("audience_gender") or ""
    if sid == "model":
        usual = prefs.get("model_look") or ""
    if sid == "platform" and usual in HD.PLATFORMS and not HD.PLATFORMS[usual].get("group"):
        usual = next((g for g, v in HD.GROUPS.items() if usual in v["members"]), usual)
    for i, o in enumerate(opts):
        if usual and o[0] == usual:
            opts.insert(0, (o[0], o[1] + " (usual)", o[2])); del opts[i + 1]; break
    return opts, ""


def answer(h, sid, value):
    """Apply an option value to the step's keys."""
    if sid == "text":
        st, _, pos = value.partition("/")
        apply_value(h, "text_style", st); apply_value(h, "text_pos", pos or "top")
    elif sid == "render":
        d, _, plan = value.partition("/")
        apply_value(h, "dur", d); apply_value(h, "plan", plan or "draft-final")
    elif sid == "people":
        apply_value(h, "presenter", value)
    elif sid == "look":
        apply_value(h, "look_id", value)
    elif sid == "language":
        apply_value(h, "language", value)
    elif sid == "audience":
        g, _, age = value.partition("/")
        apply_value(h, "audience_gender", g); apply_value(h, "audience_age", age or "18-24")
    elif sid == "model":
        g, _, look = value.partition("/")
        apply_value(h, "model_gender", g); apply_value(h, "model_look", look)
    else:
        apply_value(h, next(st[2] for st in GUIDE if st[0] == sid)[0], value)


def summary(h):
    pf = HD.PLATFORMS.get(h.get("platform") or "", {}); g = HD.GENRES.get(h.get("type") or "", {})
    lk = HD.LOOKS.get(h.get("look_id") or "", {})
    d = h.get("direction") or "auto"
    rows = [("Platform", f"{pf.get('name', '-')} · render {h.get('ratio') or '-'}, deliver {h.get('deliver') or '-'}"),
            ("Video type", g.get("name", "-")), ("Video delivers", h.get("about") or "-"),
            ("Market", f"{HD.market(h.get('market'))['name']} ({h.get('market_source') or '-'})"),
            ("Language / audience", f"{h.get('language') or '-'} / {h.get('audience') or '-'}"),
            ("On screen", f"{h.get('presenter') or '-'}" + (f" · product: {h['product']}" if h.get("product") else "") + (f" · photos: {h['photos']}" if h.get("photos") else "")),
            ("AI model", h.get("casting") or "-") if "ai" in (h.get("presenter") or "") else ("AI model", "none"),
            ("Look", lk.get("name") or h.get("look") or "-"),
            ("Direction", "3 concepts from the director" if d == "auto" else (HD.fmt(d) or {}).get("name", d)),
            ("Text", f"{h.get('text_style') or '-'}, {h.get('text_pos') or '-'}"), ("Sound", h.get("sound") or "-"),
            ("Length / plan", f"{h.get('dur') or '-'} s · {HD.PLANS.get(h.get('plan') or '', '-')}")]
    return rows


def cmd_guide(a):
    path = find(a.project); h = load(path)
    prefs = load_prefs(path)
    if not h.get("market"):
        h["market"], h["market_source"] = detect_market(prefs); save(path, h)
    done = h.setdefault("guide", {"done": []})["done"]
    if a.back:
        if done:
            done.pop()
        save(path, h)
    if a.answer is not None or a.accept:
        st = guide_next(h)
        if not st:
            sys.exit("The brief is complete. Change a step with: hookmaker.py set key=value")
        if a.accept:
            opts, _ = guide_options(h, st[0], prefs)
            if not opts:
                sys.exit(f"Step '{st[0]}' needs the user's own words: hookmaker.py guide --answer \"…\"")
            answer(h, st[0], opts[0][0])
        else:
            answer(h, st[0], a.answer)
        save(path, h)
    if a.remember:
        p = {k: h.get(k) for k in PREF_KEYS if h.get(k)}
        save(prefs_path(path), {**prefs, **p}); print(f"Saved as your usual choices: {prefs_path(path)}")
    if a.json:
        st = guide_next(h)
        if not st:
            print(json.dumps({"complete": True, "recap": summary(h)}, ensure_ascii=False)); return
        opts, free = guide_options(h, st[0], prefs)
        out = {"step": st[0], "title": st[1], "options": [{"value": v, "label": l, "detail": d} for v, l, d in opts], "note": free}
        if st[0] == "audience":
            out["ages"] = [{"value": v, "label": l} for v, l in HD.AGES]
        if st[0] == "model":
            out["genders"] = [{"value": "female", "label": "Woman"}, {"value": "male", "label": "Man"}]
        print(json.dumps(out, ensure_ascii=False)); return
    if a.all:
        for i, (sid, title, _) in enumerate(GUIDE, 1):
            opts, free = guide_options(h, sid, prefs)
            print(f"{i}. {title}{' (done)' if sid in done else ''}: " + (free or " | ".join(f"{v} = {l}" for v, l, _ in opts)))
        return
    st = guide_next(h)
    n = len(done)
    if not st:
        print("BRIEF COMPLETE. Show this recap, ask for one 'go', then write concepts (or the chosen direction).")
        for k, v in summary(h):
            print(f"  {k:<20}{v}")
        print("Change any line: hookmaker.py set key=value · go back one step: hookmaker.py guide --back · keep as defaults: hookmaker.py guide --remember")
        return
    sid, title, keys = st
    live = [x[0] for x in GUIDE if step_applies(h, x[0])]
    print(f"STEP {live.index(sid) + 1}/{len(live)} · {title}   ({n} answered)")
    opts, free = guide_options(h, sid, prefs)
    if free:
        print("  " + free)
        if sid == "about" and h.get("about"):
            print("  Show the current text and ask to confirm or sharpen it (add the payoff).")
    for j, (v, label, what) in enumerate(opts, 1):
        print(f"  {j}. [{v}] {label}" + (f": {what}" if what else ""))
    print("Record: hookmaker.py guide --answer <value>   · first option: --accept   · back: --back")
    if sid == "people":
        print("Then ask for the photos it needs and record them: hookmaker.py set product=\"…\" photos=\"path1, path2\"")
    if sid == "audience":
        print("Ask gender and age together (two questions). Record: hookmaker.py guide --answer female/18-24")
    if sid == "model":
        print("Ask gender and look together; the look list is long, so use a dropdown card (see SKILL.md). Record: hookmaker.py guide --answer female/japanese")
    if sid in ("language", "audience", "model"):
        print(f"Market: {HD.market(h.get('market'))['name']} ({h.get('market_source') or 'not set'}); change with: hookmaker.py set market=US")


def brief(h):
    """Platform and type must be known before concepts and prompts."""
    if not (h.get("platform") in HD.PLATFORMS and h.get("type") in HD.GENRES):
        sys.exit("The brief is not finished (platform and video type). Run: hookmaker.py guide")
    return HD.PLATFORMS[h["platform"]]


def cmd_platforms(a):
    for k, p in HD.PLATFORMS.items():
        s = p["safe"]
        print(f"  {k:<9}{p['name']:<22}render {p['render']:<5} deliver {p['deliver']:<5} hook {p['window']:<12}"
              f"keep clear: top {s['top']:.0%} bottom {s['bottom']:.0%} right {s['right']:.0%}")
        if a.verbose:
            print(f"           {p['sound']} {p['cover']} {p['notes']}")


def cmd_types(a):
    for k, g in HD.GENRES.items():
        print(f"  {k:<12}{g['name']:<40}{g['job']}")


def cmd_formats(a):
    pick = HD.GENRES[a.type]["formats"] if a.type else None
    if a.type and a.type not in HD.GENRES:
        sys.exit("Type: " + ", ".join(HD.GENRES))
    for f in HD.FORMATS:
        if pick and f["id"] not in pick:
            continue
        print(f"  {f['id']:<20}{f['name']:<24}{f['what']}")
        if a.verbose or pick:
            print(f"  {'':<20}first frame: {f['frame']}\n  {'':<20}motion: {f['motion']} ({f['mode']}, ~{f['dur']} s)")


def cmd_lines(a):
    types = [ST.find(a.story)] if a.story else ST.TYPES
    if a.story and not types[0]:
        sys.exit("Story types: " + ", ".join(t["id"] for t in ST.TYPES))
    for t in types:
        print(f"\n{t['name']}  [{t['id']}]  {t['use']}")
        if a.story:
            print("  Opening pictures: " + " | ".join(t["visual"]))
            print("  In a scripted film: " + t["fiction"])
            for n, tt, line in ST.numbered():
                if tt is t:
                    print(f"  {n}. {line}")
    if not a.story:
        print("\nShow a type's numbered lines: hookmaker.py lines <type>. Use the number with concept --line-no.")


def english(h):
    return (h.get("language") or "English").strip().lower() in ("", "english", "en")


def line_issues(h, c):
    """The rule that every spoken line comes from the library. Returns [(level, message)]."""
    cid = c["id"]
    if c.get("custom_line"):
        return [("WARNING", f"{cid}: custom line, not from the library. Approved by the user: {c['custom_line']}")]
    if not c.get("line_no"):
        return [("ERROR", f"{cid}: no library line. Pick one from references/lines.md and record it with --line-no N "
                          "(or, only after the user approves a line of their own, --custom-line \"why\").")]
    t, src = ST.line_no(c["line_no"])
    if not t:
        return [("ERROR", f"{cid}: line {c['line_no']} does not exist (1–{ST.count()}).")]
    out = []
    if c.get("story") and c["story"] != t["id"]:
        out.append(("ERROR", f"{cid}: line {c['line_no']} is a {t['name']} line, but the story type is {c['story']}."))
    if not c.get("line"):
        out.append(("ERROR", f"{cid}: line {c['line_no']} chosen but the spoken line (--line) is empty."))
    elif english(h):
        if not ST.matches(src, c["line"]):
            out.append(("ERROR", f"{cid}: the line changes library line {c['line_no']}. Only fill its [slots]. Library: “{src}”"))
    else:
        out.append(("NOTE", f"{cid}: show the user library line {c['line_no']} “{src}” beside the {h.get('language')} line, "
                            "so they can see it is a faithful translation with only the slots filled."))
    return out


# ---------- concepts ----------
def cmd_concept(a):
    path = find(a.project); h = load(path)
    brief(h)
    if a.story and not ST.find(a.story):
        sys.exit("Story types: " + ", ".join(t["id"] for t in ST.TYPES))
    if a.format and not HD.fmt(a.format):
        sys.exit("Formats: " + ", ".join(f["id"] for f in HD.FORMATS))
    c = next((x for x in h["concepts"] if x["id"].lower() == a.id.lower()), None)
    new = c is None
    if new:
        c = {"id": a.id, "versions": [], "created": now()}
        h["concepts"].append(c)
    f = HD.fmt(a.format or c.get("format")) if (a.format or c.get("format")) else None
    if a.line_no is not None:
        t, src = ST.line_no(a.line_no)
        if not t:
            sys.exit(f"Line {a.line_no} does not exist. Lines are numbered 1–{ST.count()}: hookmaker.py lines <type>")
        if a.story and a.story != t["id"]:
            sys.exit(f"Line {a.line_no} is a {t['name']} line ({t['id']}), not {a.story}.")
        c["line_no"] = a.line_no; c["line_source"] = src; c["story"] = t["id"]; c.pop("custom_line", None)
    if a.custom_line is not None:
        c["custom_line"] = a.custom_line; c.pop("line_no", None); c.pop("line_source", None)
    for k in ("story", "format", "line", "text", "picture", "motion", "sound", "speaker", "note"):
        v = getattr(a, k)
        if v is not None:
            c[k] = v
    c["dur"] = a.dur or c.get("dur") or h.get("dur") or (f["dur"] if f else 4)
    c["mode"] = a.mode or c.get("mode") or "i2v"
    c["model"] = a.model or c.get("model") or ("Kling 4.0" if h.get("plan") == "final-only" else "Kling 4.0 Flash")
    if a.score:
        try:
            s, cl, p = (int(x) for x in a.score.split("/"))
        except ValueError:
            sys.exit("Score as stop/clarity/payoff, each 1–5, e.g. 5/4/4")
        c["score"] = {"stop": s, "clarity": cl, "payoff": p, "total": s + cl + p}
    save(path, h); print(("Added " if new else "Updated ") + c["id"])


def check(h):
    out = []
    pf = brief(h)
    if h["ratio"] not in KLING_RATIOS:
        out.append(("ERROR", f"Render ratio {h['ratio']} is not offered by Kling 4.0."))
    if h["deliver"] != h["ratio"]:
        out.append(("NOTE", f"{pf['name']} prefers {h['deliver']}: render {h['ratio']}, keep the subject centred, then crop (hookmaker.py crop)."))
    for c in h["concepts"]:
        cid = c["id"]; d = c.get("dur", 4)
        lo, hi = LIMITS["flash" if "flash" in c.get("model", "").lower() else "full"]
        if d < lo or d > hi:
            out.append(("ERROR", f"{cid}: {d} s is outside {c.get('model')}'s {lo}–{hi} s."))
        if c.get("mode") == "frames" and "flash" in c.get("model", "").lower():
            out.append(("ERROR", f"{cid}: Kling 4.0 Flash takes a first frame only. Use Kling 4.0 for start and end frames."))
        if d > 8:
            out.append(("WARNING", f"{cid}: {d} s is long for a hook. Hooks land in 3–6 s; the rest belongs to the video."))
        w = words(c.get("line"))
        if w and w / WPS + 0.5 > d:
            out.append(("WARNING", f"{cid}: the line has {w} words and needs about {w / WPS + 0.5:.1f} s; the clip is {d} s. Cut words."))
        if w > 12:
            out.append(("WARNING", f"{cid}: {w} words is a sentence, not a hook. Aim for seven or fewer."))
        tw = words(c.get("text"))
        if tw > 7 or len(c.get("text") or "") > 42:
            out.append(("WARNING", f"{cid}: on-screen text is {tw} words / {len(c.get('text') or '')} characters. Keep it to about six words so it reads in one glance."))
        if c.get("text") and c.get("line") and c["text"].strip().lower() == c["line"].strip().lower():
            out.append(("WARNING", f"{cid}: the text repeats the spoken line. Make the text the short promise and the line the voice."))
        if "[" in (c.get("line") or "") + (c.get("text") or ""):
            out.append(("ERROR", f"{cid}: an unfilled [slot] is still in the line or text."))
        out += line_issues(h, c)
        if not c.get("picture"):
            out.append(("WARNING", f"{cid}: no first-frame picture written yet."))
        if not c.get("score"):
            out.append(("NOTE", f"{cid}: not scored yet (stop/clarity/payoff)."))
    if len(h["concepts"]) < 2:
        out.append(("NOTE", "Offer two or three concepts so the user can choose."))
    return out


def cmd_check(a):
    h = load(find(a.project))
    res = check(h)
    for lvl, msg in res:
        print(f"{lvl}: {msg}")
    errs = sum(1 for lvl, _ in res if lvl == "ERROR")
    print(f"{len(h['concepts'])} concepts, {errs} errors.")
    if errs:
        sys.exit(1)


def cmd_list(a):
    h = load(find(a.project))
    pf = brief(h)
    print(f"{h['title']} · {pf['name']} · {HD.GENRES[h['type']]['name']} · {h['ratio']} · {credits(h):g} credits")
    rows = sorted(h["concepts"], key=lambda c: -(c.get("score") or {}).get("total", 0))
    for c in rows:
        sc = c.get("score") or {}
        mark = "*" if h.get("chosen") == c["id"] else " "
        print(f" {mark}{c['id']:<5}{sc.get('total', '-'):>3}  {c.get('story', '-'):<15}{c.get('format', '-'):<20}{c.get('dur')} s  “{c.get('line', '')}”  [{c.get('text', '')}]")


# ---------- prompts ----------
def sent(x):
    x = (x or "").strip()
    return x if not x or x[-1] in ".!?\"”" else x + "."


def prompts(h, c):
    f = HD.fmt(c.get("format")) if c.get("format") else None
    pf = brief(h)
    safe = pf["safe"]
    room = ""
    if c.get("text"):
        room = (f"Leave clean, uncluttered space in the upper third of the frame (below the top {safe['top']:.0%}) for a text caption; "
                f"keep the subject's face and the key object away from the bottom {safe['bottom']:.0%} and the right {safe['right']:.0%}.")
    look = h.get("look") or ""
    image = "\n\n".join(x for x in [
        sent(c.get("picture") or (f["frame"] if f else "")),
        "The first frame of a social video: it must be striking and readable as a still, even as a small thumbnail. One clear subject.",
        room,
        ("Look: " + look) if look else "",
        REALISM,
    ] if x)
    motion_line = sent(c.get("motion") or (f["motion"] if f else ""))
    sound = []
    if c.get("line"):
        who = c.get("speaker") or "A clear, natural voice"
        if h.get("sound") in (None, "", "spoken"):
            sound.append(f'{who} says in {h.get("language") or "English"}: "{c["line"]}"')
        else:
            sound.append("no speech, lips closed or not visible (the line is added later as a voice-over)" if h.get("sound") == "voiceover" else "no speech")
    if c.get("sound"):
        sound.append(c["sound"])
    sound.append("no background music, no subtitles")
    video = "\n\n".join(x for x in [
        "Keep the faces, clothing, product, set and light of the first frame exactly." if c.get("mode", "i2v") in ("i2v", "frames") else "",
        "The action is already underway in the very first frame: no slow build, no fade in. Something visibly changes within the first second.",
        motion_line,
        "One camera move only, starting immediately. End on a clean beat that can cut straight into the main video.",
        "Sound: " + " / ".join(sound) + ".",
    ] if x)
    return image, video


def cmd_prompt(a):
    path = find(a.project); h = load(path)
    folder = os.path.join(os.path.dirname(path) or ".", "prompts"); os.makedirs(folder, exist_ok=True)
    targets = h["concepts"] if a.id == "all" else [concept(h, a.id)]
    for c in targets:
        image, video = prompts(h, c)
        c["image_prompt"], c["video_prompt"] = image, video
        for kind, text in (("image", image), ("video", video)):
            with open(os.path.join(folder, f"{c['id']}-{kind}.txt"), "w", encoding="utf-8") as f:
                f.write(text + "\n")
        if not a.quiet:
            print(f"===== {c['id']} · {c.get('dur')} s · {c.get('model')}\n--- first frame (GPT Image 2.5, {STILL_RATIO.get(h['ratio'], h['ratio'])})\n{image}\n--- motion (Kling 4.0)\n{video}\n")
    save(path, h)
    print(f"Prompts written to {folder}. Drafts: read each against references/look.md before spending credits.")


# ---------- generations ----------
def cmd_log(a):
    path = find(a.project); h = load(path)
    c = concept(h, a.id)
    v = {"n": len(c["versions"]) + 1, "stage": a.stage, "at": now()}
    for k in ("gen", "model", "credits", "file", "thumb", "note"):
        val = getattr(a, k)
        if val is not None:
            v[k] = val
    c["versions"].append(v)
    save(path, h); print(f"{c['id']} v{v['n']} ({a.stage}) logged. Total {credits(h):g} credits.")


def cmd_extra(a):
    path = find(a.project); h = load(path)
    h.setdefault("extras", []).append({"label": a.label, "gen": a.gen or "", "credits": a.credits or 0, "file": a.file or "", "at": now()})
    save(path, h); print(f"Logged: {a.label}")


def cmd_pick(a):
    path = find(a.project); h = load(path)
    c = concept(h, a.id)
    errs = [m for lvl, m in line_issues(h, c) if lvl == "ERROR"]
    if errs:
        sys.exit("Cannot pick " + c["id"] + ":\n" + "\n".join(errs))
    h["chosen"] = c["id"]; save(path, h); print(f"Chosen hook: {h['chosen']}")


# ---------- media ----------
def need(tool):
    p = shutil.which(tool)
    if not p:
        sys.exit(f"{tool} is not installed, so this step can't run here. Give the user the overlay spec from `hookmaker.py pack` instead.")
    return p


def probe(path):
    need("ffprobe")
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    if not out:
        sys.exit(f"Could not read {path}")
    w, hh = out.split(",")[:2]
    return int(w), int(hh)


def browser():
    for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge", "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"):
        if os.path.exists(c):
            return c
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
        if shutil.which(n):
            return shutil.which(n)
    return None


def text_layer(w, hh, text, platform, pos, size, style, out_png):
    sf = HD.PLATFORMS[platform]["safe"]
    left, right = sf["left"] * w, sf["right"] * w
    top = sf["top"] * hh + 0.03 * hh
    fs = int((size or (0.075 if w < hh else 0.042)) * w)
    vpos = {"top": f"top:{top:.0f}px", "middle": "top:50%;transform:translateY(-50%)", "bottom": f"bottom:{sf['bottom'] * hh + 0.02 * hh:.0f}px"}[pos]
    if style == "box":
        deco = "background:#fff;color:#111;padding:.18em .45em;border-radius:.22em;box-decoration-break:clone;-webkit-box-decoration-break:clone"
    else:
        deco = "color:#fff;-webkit-text-stroke:%dpx #000;paint-order:stroke fill;text-shadow:0 %dpx %dpx rgba(0,0,0,.6)" % (max(4, fs // 7), max(2, fs // 16), max(6, fs // 5))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{w}px;height:{hh}px;background:transparent;overflow:hidden}}
.t{{text-wrap:balance;position:absolute;left:{left:.0f}px;right:{right:.0f}px;{vpos};text-align:center;font:800 {fs}px/1.15 "SF Pro Display","Helvetica Neue",Arial,sans-serif;letter-spacing:-.01em}}
.t span{{{deco}}}</style></head><body><div class="t"><span>{html.escape(text)}</span></div></body></html>"""
    b = browser()
    if not b:
        sys.exit("No Chrome-family browser found to draw the text layer. Give the user the overlay spec from `hookmaker.py pack` for their editor.")
    with tempfile.TemporaryDirectory() as td:
        page_path = os.path.join(td, "t.html")
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page)
        subprocess.run([b, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={w},{hh}",
                        "--default-background-color=00000000", f"--screenshot={out_png}", "file://" + page_path], capture_output=True, timeout=60)
    if not os.path.exists(out_png):
        sys.exit("The text layer could not be drawn. Use the overlay spec instead.")


def cmd_overlay(a):
    need("ffmpeg")
    h = None
    try:
        h = load(find(a.project))
    except SystemExit:
        pass
    platform = a.platform or (h or {}).get("platform") or "tiktok"
    w, hh = probe(a.clip)
    out = a.out or re.sub(r"(\.\w+)$", r"_text\1", a.clip)
    png = out + ".text.png"
    pos = a.pos or (h or {}).get("text_pos") or "top"; style = a.style or (h or {}).get("text_style") or "outline"
    if style == "none":
        style = "outline"
    text_layer(w, hh, a.text, platform, pos, a.size, style, png)
    end = f"between(t,{a.start},{a.end})" if a.end else f"gte(t,{a.start})"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.clip, "-i", png, "-filter_complex", f"[0:v][1:v]overlay=0:0:enable='{end}'[v]",
                        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "copy", out], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip()[-600:])
    os.remove(png)
    print(f"Wrote {out} (text inside the {HD.PLATFORMS[platform]['name']} safe zone, {pos})")


def cmd_crop(a):
    need("ffmpeg")
    rw, rh = (int(x) for x in a.ratio.split(":"))
    w, hh = probe(a.file)
    if w / hh > rw / rh:
        cw, ch = int(hh * rw / rh) // 2 * 2, hh
    else:
        cw, ch = w, int(w * rh / rw) // 2 * 2
    x = int((w - cw) * a.x); y = int((hh - ch) * a.y)
    out = a.out or re.sub(r"(\.\w+)$", f"_{rw}x{rh}" + r"\1", a.file)
    is_img = a.file.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", a.file, "-vf", f"crop={cw}:{ch}:{x}:{y}"]
    if not is_img:
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "copy"]
    r = subprocess.run(cmd + [out], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip()[-600:])
    print(f"Wrote {out} ({cw}x{ch})")


# ---------- hook pack ----------
CSS = """
:root{--bg:#f5f2ec;--card:#fff;--ink:#15171a;--mute:#646b74;--line:#e2dccf;--accent:#c2410c;--chip:#efe9de}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#101214;--card:#1a1d21;--ink:#eef0f2;--mute:#a1a8b1;--line:#2b3036;--accent:#fb8a4c;--chip:#23282d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1100px;margin:0 auto;padding:28px 16px 56px}h1{font:700 34px/1.1 Georgia,"Iowan Old Style",serif;margin:4px 0}
.k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700}.sub{color:var(--mute)}
.info{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:16px 0}
.info div{background:var(--card);padding:10px 14px}.info span{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
h2{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:28px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}.card.chosen{outline:2px solid var(--accent)}
.pic{background:var(--chip);display:flex;align-items:center;justify-content:center;color:var(--mute);font-size:13px;position:relative}.pic img{width:100%;height:100%;object-fit:cover}
.badge{position:absolute;top:10px;left:10px;background:var(--accent);color:#fff;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:700}
.b{padding:12px 14px;display:grid;gap:6px}.line{font:600 18px/1.3 Georgia,serif}.txt{display:inline-block;background:var(--ink);color:var(--card);padding:2px 8px;border-radius:6px;font-weight:700;font-size:13px}
.m{color:var(--mute);font-size:13px}.sc{display:flex;gap:6px;flex-wrap:wrap}.sc span{background:var(--chip);border-radius:999px;padding:2px 9px;font-size:12px}
details{font-size:13px}summary{cursor:pointer;color:var(--mute)}pre{white-space:pre-wrap;font:12px/1.5 ui-monospace,Menlo,monospace}a{color:var(--accent)}
"""


def cmd_pack(a):
    path = find(a.project); h = load(path)
    base = os.path.dirname(path) or "."
    pf = brief(h); g = HD.GENRES[h["type"]]
    rw, rh = (int(x) for x in h["ratio"].split(":"))
    cards = []
    md = [f"# Hook pack: {h['title']}", "", f"{pf['name']} · {g['name']} · render {h['ratio']}, deliver {h['deliver']} · {credits(h):g} credits logged", "",
          f"About: {h.get('about') or '-'}  ", f"Audience: {h.get('audience') or '-'}  ", f"Hook window: {pf['window']}. {pf['sound']} {pf['cover']}", ""]
    for c in sorted(h["concepts"], key=lambda c: (h.get("chosen") != c["id"], -(c.get("score") or {}).get("total", 0))):
        st = ST.find(c.get("story")) if c.get("story") else None
        f = HD.fmt(c.get("format")) if c.get("format") else None
        thumb = next((v.get("thumb") for v in reversed(c["versions"]) if v.get("thumb")), "")
        clip = next((v.get("file") or v.get("gen") for v in reversed(c["versions"]) if v.get("stage") in ("draft", "final")), "")
        sc = c.get("score") or {}
        chosen = h.get("chosen") == c["id"]
        pic = f'<img src="{html.escape(thumb)}" alt="{html.escape(c["id"])} first frame">' if thumb else "first frame not made yet"
        cards.append(f'''<article class="card{' chosen' if chosen else ''}"><div class="pic" style="aspect-ratio:{rw}/{rh}">{pic}<span class="badge">{html.escape(c['id'])}{' · chosen' if chosen else ''}</span></div><div class="b">
<div class="line">“{html.escape(c.get('line') or '')}”</div><div class="m">{html.escape(f"Library line {c['line_no']}: “{c.get('line_source', '')}”" if c.get('line_no') else ("Custom line, approved: " + c['custom_line'] if c.get('custom_line') else "No library line recorded"))}</div>{f'<div><span class="txt">{html.escape(c["text"])}</span></div>' if c.get('text') else ''}
<div class="m">{html.escape(st['name'] if st else '-')} · {html.escape(f['name'] if f else '-')} · {c.get('dur')} s · {html.escape(c.get('model', ''))}</div>
<div class="m"><b>Picture:</b> {html.escape(c.get('picture') or (f['frame'] if f else ''))}</div><div class="m"><b>Motion:</b> {html.escape(c.get('motion') or (f['motion'] if f else ''))}</div>
{f'<div class="sc"><span>stop {sc["stop"]}</span><span>clarity {sc["clarity"]}</span><span>payoff {sc["payoff"]}</span><span><b>{sc["total"]}/15</b></span></div>' if sc else ''}
{f'<div class="m">Clip: {html.escape(str(clip))}</div>' if clip else ''}
<details><summary>Prompts</summary><pre>{html.escape((c.get('image_prompt') or '') + chr(10) * 2 + (c.get('video_prompt') or ''))}</pre></details></div></article>''')
        md += [f"## {c['id']}{' (chosen)' if chosen else ''}", "", f"- Line: “{c.get('line') or ''}”",
               f"- Library line: {c['line_no']}. “{c.get('line_source', '')}”" if c.get("line_no") else f"- Library line: none ({'custom, approved: ' + c['custom_line'] if c.get('custom_line') else 'not recorded'})",
f"- On-screen text: {c.get('text') or '-'}",
               f"- Story type / format: {st['name'] if st else '-'} / {f['name'] if f else '-'}", f"- Length and model: {c.get('dur')} s, {c.get('model')}",
               f"- Picture: {c.get('picture') or (f['frame'] if f else '')}", f"- Motion: {c.get('motion') or (f['motion'] if f else '')}"]
        if sc:
            md.append(f"- Score: stop {sc['stop']}, clarity {sc['clarity']}, payoff {sc['payoff']} = {sc['total']}/15")
        if c["versions"]:
            md.append("- Generations: " + "; ".join(f"v{v['n']} {v['stage']} {v.get('gen', '')} {v.get('file', '')}".strip() for v in c["versions"]))
        md.append("")
    s = pf["safe"]
    spec = (f"Overlay spec for an editor: text in the upper third, at least {s['top']:.0%} from the top, {s['bottom']:.0%} clear at the bottom, "
            f"{s['right']:.0%} clear on the right; bold sans-serif, white with a dark outline or a white box with dark text; visible from 0.2 s to the end of the hook.")
    md += ["## Overlay spec", "", spec, ""]
    info = [("Platform", pf["name"]), ("Video type", g["name"]), ("Ratio", f"render {h['ratio']} · deliver {h['deliver']}"), ("Hook window", pf["window"]),
            ("Audience", h.get("audience") or "-"), ("Credits", f"{credits(h):g}")]
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(h["title"])} hooks</title><style>{CSS}</style></head><body><main>'
            f'<div class="k">Hook pack · The Hook Maker</div><h1>{html.escape(h["title"])}</h1><div class="sub">{html.escape(h.get("about") or "")}</div>'
            f'<div class="info">{"".join(f"<div><span>{k}</span><b>{html.escape(str(v))}</b></div>" for k, v in info)}</div>'
            f'<div class="m">{html.escape(g["job"])} {html.escape(pf["sound"])} {html.escape(pf["cover"])}</div>'
            f'<h2>Concepts</h2><div class="grid">{"".join(cards) or "<p class=sub>No concepts yet.</p>"}</div>'
            f'<h2>Overlay spec</h2><p class="m">{html.escape(spec)}</p><p class="m">Updated {html.escape(h.get("updated", ""))}</p></main></body></html>')
    with open(os.path.join(base, "hook-pack.html"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(base, "hook-pack.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Wrote {os.path.join(base, 'hook-pack.html')} and hook-pack.md")


# ---------- references ----------
def cmd_write_refs(a):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    L = ["# Hook lines", "", f"{len(ST.TYPES)} story types and {ST.count()} original opening lines. Choose the story type first (it shapes the rest of the video), "
         "then a line, then fill every [slot] with the project's specifics. An empty slot is a template, not a hook.", "",
         "Generated from `scripts/story_types.py` by `hookmaker.py write-refs`. Edit that file, not this one.", "", "## Contents", ""]
    L += [f"{i}. {t['name']} (`{t['id']}`)" for i, t in enumerate(ST.TYPES, 1)]
    n = 0
    for t in ST.TYPES:
        L += ["", f"## {t['name']}", "", f"Key: `{t['id']}`. {t['use']}", "", "**Beats of the video that follows:** " + " → ".join(t["beats"]) + ".", "",
              "**Opening pictures:**", ""] + [f"- {v}" for v in t["visual"]] + ["", f"**In a scripted film:** {t['fiction']}", "", "**Lines:**", ""]
        for line in t["lines"]:
            n += 1
            L.append(f"{n}. {line}")
    with open(os.path.join(root, "references", "lines.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    F = ["# Visual formats, platforms and video types", "", "The picture-and-motion half of a hook, where it is posted, and what the hook must do for each kind of video.",
         "Generated from `scripts/hook_data.py` by `hookmaker.py write-refs`.", "", "## Contents", "", "1. Visual formats", "2. Platforms", "3. Video types", "", "## 1. Visual formats", "",
         "| id | Format | What it is | First frame | Motion | Mode, length |", "|---|---|---|---|---|---|"]
    F += [f"| `{f['id']}` | {f['name']} | {f['what']} | {f['frame']} | {f['motion']} | {f['mode']}, ~{f['dur']} s |" for f in HD.FORMATS]
    F += ["", "## 2. Platforms", "", "Safe zones are approximate fractions of the frame that buttons and captions cover. Interfaces change; treat them as margins.", "",
          "| id | Platform | Render | Deliver | Hook window | Keep clear (top / bottom / left / right) | Sound | Cover |", "|---|---|---|---|---|---|---|---|"]
    for k, p in HD.PLATFORMS.items():
        s = p["safe"]
        F.append(f"| `{k}` | {p['name']} | {p['render']} | {p['deliver']} | {p['window']} | {s['top']:.0%} / {s['bottom']:.0%} / {s['left']:.0%} / {s['right']:.0%} | {p['sound']} | {p['cover']} {p['notes']} |")
    F += ["", "## 3. Video types", "", "| id | Type | The hook's job | Story types to try | Formats to try | Take care |", "|---|---|---|---|---|---|"]
    F += [f"| `{k}` | {g['name']} | {g['job']} | {', '.join(g['stories'])} | {', '.join(g['formats'])} | {g['care']} |" for k, g in HD.GENRES.items()]
    with open(os.path.join(root, "references", "formats.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(F) + "\n")
    print("Wrote references/lines.md and references/formats.md")


def main():
    ap = argparse.ArgumentParser(description="The Hook Maker helper")
    ap.add_argument("--project", help="hook folder or hook.json (default: found automatically)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start", help="start a hook project from the brief"); s.add_argument("title")
    s.add_argument("--platform", help=", ".join(HD.PLATFORMS)); s.add_argument("--type", help=", ".join(HD.GENRES))
    s.add_argument("--about"); s.add_argument("--audience"); s.add_argument("--language"); s.add_argument("--presenter", choices=list(PRESENTERS))
    s.add_argument("--chat-language", help="the language the user writes in; sets the default market and model look");
    s.add_argument("--product", help="product name if one must appear"); s.add_argument("--cta"); s.add_argument("--ratio"); s.add_argument("--look"); s.add_argument("--dir"); s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_start)
    s = sub.add_parser("guide", help="guided brief: one step at a time with options and defaults")
    s.add_argument("--answer", help="value for the current step"); s.add_argument("--accept", action="store_true", help="take the default for the current step")
    s.add_argument("--back", action="store_true", help="reopen the last answered step"); s.add_argument("--all", action="store_true", help="every step at once (fast mode)")
    s.add_argument("--json", action="store_true", help="current step as JSON, for a dropdown card")
    s.add_argument("--remember", action="store_true", help="save this brief's choices as the user's usual defaults"); s.set_defaults(fn=cmd_guide)
    s = sub.add_parser("set", help="change brief fields: key=value"); s.add_argument("pairs", nargs="+"); s.set_defaults(fn=cmd_set)
    s = sub.add_parser("platforms"); s.add_argument("-v", "--verbose", action="store_true"); s.set_defaults(fn=cmd_platforms)
    s = sub.add_parser("types", help="video types"); s.set_defaults(fn=cmd_types)
    s = sub.add_parser("formats", help="visual hook formats"); s.add_argument("--type"); s.add_argument("-v", "--verbose", action="store_true"); s.set_defaults(fn=cmd_formats)
    s = sub.add_parser("lines", help="story types and hook lines"); s.add_argument("story", nargs="?"); s.set_defaults(fn=cmd_lines)
    s = sub.add_parser("concept", help="add or update a hook concept"); s.add_argument("id")
    for k in ("story", "format", "line", "text", "picture", "motion", "sound", "speaker", "note", "mode", "model", "score"):
        s.add_argument("--" + k)
    s.add_argument("--line-no", type=int, help="number of the library line in references/lines.md (required)")
    s.add_argument("--custom-line", help="only after the user approved a line not from the library: say why")
    s.add_argument("--dur", type=int); s.set_defaults(fn=cmd_concept)
    s = sub.add_parser("list", help="concepts ranked by score"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("check", help="timing, text, ratio and model checks"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("prompt", help="first-frame and motion prompts for a concept"); s.add_argument("id"); s.add_argument("--quiet", action="store_true"); s.set_defaults(fn=cmd_prompt)
    s = sub.add_parser("log", help="record a generation"); s.add_argument("id"); s.add_argument("--stage", required=True, choices=["still", "draft", "final", "fix"])
    for k in ("gen", "model", "file", "thumb", "note"):
        s.add_argument("--" + k)
    s.add_argument("--credits", type=float); s.set_defaults(fn=cmd_log)
    s = sub.add_parser("extra", help="record a cover, thumbnail or other generation"); s.add_argument("label"); s.add_argument("--gen"); s.add_argument("--credits", type=float); s.add_argument("--file"); s.set_defaults(fn=cmd_extra)
    s = sub.add_parser("pick", help="mark the chosen concept"); s.add_argument("id"); s.set_defaults(fn=cmd_pick)
    s = sub.add_parser("overlay", help="burn exact on-screen text into a clip, inside the safe zone"); s.add_argument("clip"); s.add_argument("--text", required=True)
    s.add_argument("--platform"); s.add_argument("--pos", choices=["top", "middle", "bottom"]); s.add_argument("--style", choices=["outline", "box"])
    s.add_argument("--size", type=float, help="font size as a fraction of width (default 0.075 vertical, 0.042 wide)"); s.add_argument("--start", type=float, default=0.2); s.add_argument("--end", type=float); s.add_argument("--out"); s.set_defaults(fn=cmd_overlay)
    s = sub.add_parser("crop", help="crop a clip or still to a feed ratio, e.g. 4:5"); s.add_argument("file"); s.add_argument("--ratio", required=True)
    s.add_argument("--x", type=float, default=0.5); s.add_argument("--y", type=float, default=0.5); s.add_argument("--out"); s.set_defaults(fn=cmd_crop)
    s = sub.add_parser("pack", help="write hook-pack.html and hook-pack.md"); s.set_defaults(fn=cmd_pack)
    s = sub.add_parser("write-refs", help="regenerate references/lines.md and formats.md"); s.set_defaults(fn=cmd_write_refs)
    a = ap.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()

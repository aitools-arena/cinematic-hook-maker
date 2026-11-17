"""Platforms, video types and visual hook formats for The Hook Maker.

Safe zones are approximate fractions of the frame that platform buttons and captions
usually cover. Interfaces change; treat them as a margin, not a measurement.
"""

# render: the ratio to ask Kling 4.0 for (it offers 16:9, 9:16, 1:1, 21:9).
# deliver: the ratio the platform prefers; when it differs, crop after rendering.
PLATFORMS = {
    "tiktok": {"name": "TikTok", "deliver": "9:16", "render": "9:16", "window": "1–2 s",
               "safe": {"top": 0.10, "bottom": 0.25, "left": 0.06, "right": 0.16},
               "sound": "Most people watch with sound on, but the first frame must work muted.",
               "cover": "The first frame often becomes the cover. Make it readable as a still.",
               "notes": "Native, fast, slightly raw beats over-produced. Text in the upper-middle third."},
    "reels": {"name": "Instagram Reels", "deliver": "9:16", "render": "9:16", "window": "1–2 s",
              "safe": {"top": 0.12, "bottom": 0.22, "left": 0.06, "right": 0.14},
              "sound": "Many watch muted in feed. Burn the key words in.",
              "cover": "The profile grid crops covers toward a vertical rectangle around 3:4: keep the subject and title centred.",
              "notes": "Aesthetic matters more here. Good-looking, clean light, one clear subject."},
    "shorts": {"name": "YouTube Shorts", "deliver": "9:16", "render": "9:16", "window": "1–2 s",
               "safe": {"top": 0.10, "bottom": 0.22, "left": 0.06, "right": 0.16},
               "sound": "Sound on is common. A spoken line works well.",
               "cover": "The frame chosen as the Short's thumbnail should state the promise on its own.",
               "notes": "Loops count: an ending that flows back into the first frame helps rewatches."},
    "youtube": {"name": "YouTube (long-form)", "deliver": "16:9", "render": "16:9", "window": "first 5–15 s",
                "safe": {"top": 0.06, "bottom": 0.14, "left": 0.05, "right": 0.05},
                "sound": "Sound on. The spoken promise carries the hook; picture proves it.",
                "cover": "The thumbnail is separate: make a 16:9 still from the same first frame with one face or object and three words at most.",
                "notes": "The hook must match the title and thumbnail promise, then preview the payoff."},
    "facebook": {"name": "Facebook feed", "deliver": "4:5", "render": "9:16", "window": "1–3 s",
                 "safe": {"top": 0.08, "bottom": 0.18, "left": 0.06, "right": 0.06},
                 "sound": "Mostly muted autoplay. Burned-in text is essential.",
                 "cover": "Crop from the 9:16 render to 4:5; keep subject and text in the middle.",
                 "notes": "Older, broader audience: clarity over cleverness."},
    "linkedin": {"name": "LinkedIn", "deliver": "1:1", "render": "1:1", "window": "1–3 s",
                 "safe": {"top": 0.08, "bottom": 0.14, "left": 0.06, "right": 0.06},
                 "sound": "Muted autoplay. Text carries it.",
                 "cover": "Square first frame with a clear human face or result.",
                 "notes": "Professional tone: lessons, results, behind the scenes. Avoid clickbait."},
    "x": {"name": "X", "deliver": "16:9", "render": "16:9", "window": "1–2 s",
          "safe": {"top": 0.06, "bottom": 0.12, "left": 0.05, "right": 0.05},
          "sound": "Muted autoplay.", "cover": "First frame shows in the timeline; make it a statement.",
          "notes": "Short, bold, opinion-led. Square (1:1) also works well."},
}

# Ratio groups for the guided brief: platforms that share a ratio are one choice.
# The safe zone is the widest of the group, so the text clears every platform in it.
GROUPS = {
    "vertical": {"name": "9:16 vertical", "members": ["tiktok", "reels", "shorts"], "label": "TikTok, Instagram Reels, YouTube Shorts, Stories"},
    "wide": {"name": "16:9 horizontal", "members": ["youtube", "x"], "label": "YouTube, X, Facebook video, website"},
    "feed": {"name": "4:5 feed", "members": ["facebook"], "label": "Instagram and Facebook feed (rendered 9:16, cropped)"},
    "square": {"name": "1:1 square", "members": ["linkedin"], "label": "LinkedIn, Instagram grid, X"},
}
for _g, _v in GROUPS.items():
    _m = [PLATFORMS[k] for k in _v["members"]]
    PLATFORMS[_g] = {"name": _v["name"] + " (" + _v["label"] + ")", "deliver": _m[0]["deliver"], "render": _m[0]["render"],
                     "window": _m[0]["window"], "safe": {side: max(x["safe"][side] for x in _m) for side in ("top", "bottom", "left", "right")},
                     "sound": " ".join(dict.fromkeys(x["sound"] for x in _m)), "cover": _m[0]["cover"],
                     "notes": " ".join(dict.fromkeys(x["notes"] for x in _m)), "group": True}

# Video types: what the hook has to do for each, and where to look first.
GENRES = {
    "ads": {"name": "Paid ad / brand ad", "job": "Stop the thumb, name the problem or desire, show the product within 3 s.",
            "stories": ["mirror", "before-after", "open-loop"], "formats": ["pattern-interrupt", "result-first", "product-drop", "impossible"],
            "care": "Keep logos and packaging exactly as supplied (edit from the real product photo). Claims must be true; platform ad policies apply."},
    "affiliate": {"name": "Affiliate / product recommendation", "job": "Make the viewer feel the problem, then show the product solving it fast.",
                  "stories": ["mistake", "mirror", "someone-else"], "formats": ["mistake-freeze", "hands-demo", "before-after-cut", "comparison"],
                  "care": "Disclose the affiliate relationship in the caption. Show the real product, not an invented one."},
    "review": {"name": "Product review / comparison", "job": "Promise a verdict and tease it.",
               "stories": ["against-grain", "crossroads", "open-loop"], "formats": ["comparison", "result-first", "reveal-pull"],
               "care": "A review must reflect real use. Never generate fake owners or fake results presented as real."},
    "tutorial": {"name": "Tutorial / how-to", "job": "Show the finished result first, then promise the steps.",
                 "stories": ["before-after", "behind-curtain", "lesson"], "formats": ["result-first", "hands-demo", "before-after-cut", "countdown"],
                 "care": "The result shown must be reachable with the steps taught."},
    "explainer": {"name": "Education / explainer", "job": "Pose a question the viewer suddenly needs answered.",
                  "stories": ["open-loop", "against-grain", "secret"], "formats": ["question-card", "scale-shift", "impossible", "reveal-pull"],
                  "care": "Keep facts accurate; label illustrations of things nobody has filmed."},
    "testimonial": {"name": "UGC / testimonial style", "job": "A real-feeling person, mid-thought, with a specific result.",
                    "stories": ["someone-else", "before-after", "mirror"], "formats": ["face-to-camera", "pov", "before-after-cut"],
                    "care": "AI people may act a scripted scene, but never present an AI person as a real customer giving a genuine review. Use the user's own customers' words with permission, or label it as a dramatisation."},
    "vlog": {"name": "Vlog / lifestyle", "job": "Drop the viewer into the most alive moment of the day.",
             "stories": ["mirror", "turning-point", "clock"], "formats": ["pov", "cinematic-cold-open", "pattern-interrupt"],
             "care": "If the user appears, build from their own photos; never generate a real person without consent."},
    "story": {"name": "Micro-drama / short film / storytime", "job": "Start in the middle of trouble and raise one question.",
              "stories": ["secret", "clock", "open-loop", "crossroads"], "formats": ["cinematic-cold-open", "mistake-freeze", "reveal-pull", "pattern-interrupt"],
              "care": "In fiction the hook is a scene, not a sentence to camera."},
    "commentary": {"name": "News / commentary / opinion", "job": "State the take in the first line and show what it is about.",
                   "stories": ["against-grain", "secret", "open-loop"], "formats": ["question-card", "face-to-camera", "comparison"],
                   "care": "Do not generate realistic footage of real events or real people; use symbolic or clearly illustrative pictures."},
    "launch": {"name": "Product or course launch", "job": "Reveal the thing with the energy of an event.",
               "stories": ["clock", "secret", "behind-curtain"], "formats": ["product-drop", "reveal-pull", "impossible", "countdown"],
               "care": "Keep the real product's look exact; show only features that exist."},
    "podcast": {"name": "Podcast / talking-head clip", "job": "Open on the most surprising sentence, with a picture that earns attention.",
                "stories": ["against-grain", "lesson", "secret"], "formats": ["face-to-camera", "question-card", "pattern-interrupt"],
                "care": "Use the user's real footage for the speaker; AI only for B-roll or the opening picture."},
    "promo": {"name": "Event / local business / real estate promo", "job": "Show the best moment of the place or event before anything else.",
              "stories": ["before-after", "behind-curtain", "clock"], "formats": ["reveal-pull", "cinematic-cold-open", "impossible", "countdown"],
              "care": "Places and products must look like the real ones; edit from the user's photos."},
}

# Visual hook formats: the picture-and-motion half of a hook.
FORMATS = [
    {"id": "result-first", "name": "Result First", "what": "Open on the finished outcome, then cut to the start.",
     "frame": "The finished result, perfectly lit, filling the frame.", "motion": "A slow push-in on the result from frame one; it ends on a beat ready to cut back.",
     "mode": "image-to-video", "dur": 4},
    {"id": "pattern-interrupt", "name": "Pattern Interrupt", "what": "An ordinary frame broken by one unexpected event in the first second.",
     "frame": "A calm, ordinary moment a split second before something happens.", "motion": "Within the first second the unexpected thing happens (a glass falls, a door bursts open); the camera reacts with a small jolt.",
     "mode": "image-to-video", "dur": 4},
    {"id": "impossible", "name": "Impossible Visual", "what": "Something that cannot happen, happening calmly and photorealistically.",
     "frame": "A real, believable place with one impossible element already starting.", "motion": "The impossible thing completes (a bottle grows to the size of a building, the room fills with water without spilling); one steady camera move.",
     "mode": "image-to-video", "dur": 5},
    {"id": "scale-shift", "name": "Scale Shift", "what": "Macro to giant, or a tiny world inside an everyday object.",
     "frame": "Extreme macro detail that reads as a landscape.", "motion": "The camera pulls back fast to reveal the real, ordinary scale.",
     "mode": "image-to-video", "dur": 4},
    {"id": "pov", "name": "Point of View", "what": "The viewer's own eyes in a moment they know.",
     "frame": "First-person view: hands, phone, steering wheel, desk, as the viewer would see them.", "motion": "Subtle head-motion handheld; one thing in front of us goes wrong or right.",
     "mode": "image-to-video", "dur": 4},
    {"id": "face-to-camera", "name": "Face to Camera", "what": "A person mid-sentence, eyes locked on the lens.",
     "frame": "Medium close-up, the person already talking, eyes into the lens, hard natural light.", "motion": "They deliver one short line with a gesture; slight handheld; lips sync to the line.",
     "mode": "image-to-video", "dur": 5},
    {"id": "hands-demo", "name": "Hands Demo", "what": "Top-down or over-the-shoulder hands doing the key step.",
     "frame": "Top-down view of hands and the object, clean surface, one hard light source.", "motion": "The hands perform the single most satisfying step; static camera.",
     "mode": "image-to-video", "dur": 4},
    {"id": "before-after-cut", "name": "Before / After Cut", "what": "Same framing, two states, a hard cut or a wipe.",
     "frame": "The 'before' state; a second still makes the 'after' by editing the first.", "motion": "Start and end frames: the camera holds while the state changes, or a fast wipe passes across.",
     "mode": "first-and-last-frame", "dur": 4},
    {"id": "reveal-pull", "name": "Reveal Pull-Back", "what": "Tight on a puzzling detail, pull back to reveal what it is.",
     "frame": "A tight detail that cannot be identified yet.", "motion": "Camera pulls back steadily to reveal the full scene; ends on the reveal.",
     "mode": "image-to-video", "dur": 5},
    {"id": "question-card", "name": "Question Card", "what": "One bold question as text over a moody, moving picture.",
     "frame": "A clean, atmospheric picture with empty space where the text will sit.", "motion": "Slow drift or push-in; nothing busy behind the words.",
     "mode": "image-to-video", "dur": 4},
    {"id": "countdown", "name": "Countdown", "what": "A visible timer or number that creates urgency.",
     "frame": "A clock, phone timer or number in frame beside the subject.", "motion": "The countdown ticks while the subject acts fast; handheld energy.",
     "mode": "image-to-video", "dur": 5},
    {"id": "product-drop", "name": "Product Drop", "what": "The product falls or slides into frame and lands with impact.",
     "frame": "An empty hero surface with the product's exact look supplied as a reference.", "motion": "The product drops into frame, lands with a small bounce, dust or water reacts, camera settles on the hero angle.",
     "mode": "reference-to-video or first-and-last-frame", "dur": 4},
    {"id": "transformation", "name": "One-Take Transformation", "what": "A person, object or place changes in one unbroken move.",
     "frame": "The starting state; the end state is an edited copy of it.", "motion": "Start and end frames with an orbit or push; the change rides the camera move.",
     "mode": "first-and-last-frame", "dur": 5},
    {"id": "mistake-freeze", "name": "Mistake Freeze", "what": "The exact instant something goes wrong, held.",
     "frame": "The split second before the mistake.", "motion": "The mistake happens and the action slows almost to a stop at the worst moment (add the freeze in the edit if the model doesn't hold).",
     "mode": "image-to-video", "dur": 4},
    {"id": "comparison", "name": "Side by Side", "what": "Two options or two results at once.",
     "frame": "A split frame or two objects side by side on one surface, evenly lit.", "motion": "Both react to the same action at the same time; static camera.",
     "mode": "image-to-video", "dur": 4},
    {"id": "cinematic-cold-open", "name": "Cinematic Cold Open", "what": "A film-like first shot already inside the tension.",
     "frame": "A composed film frame with one source of light and one figure in trouble.", "motion": "One deliberate camera move toward the threat or the face; ambient sound only.",
     "mode": "image-to-video", "dur": 5},
]


def fmt(fid):
    for f in FORMATS:
        if f["id"] == fid:
            return f
    return None


# ---------- guided brief ----------
# Looks the user can pick in the guided brief. "fits" orders them per video type.
LOOKS = {
    "natural": {"name": "Natural / UGC", "look": "Natural daylight, true-to-life colour, a phone-camera feel held by hand; real home or street setting.",
                "fits": ["testimonial", "vlog", "affiliate", "review", "podcast"]},
    "clean": {"name": "Clean commercial", "look": "Bright, soft high-key light, clean set, crisp product detail on an 85 mm lens, neutral colour.",
              "fits": ["ads", "launch", "affiliate", "promo"]},
    "editorial": {"name": "Fashion editorial", "look": "Soft window light, editorial framing, muted neutral palette, fabric texture visible, calm confident model.",
                  "fits": ["ads", "affiliate", "vlog", "launch"]},
    "film": {"name": "Cinematic drama", "look": "Motivated window or practical light, gentle contrast, 50 mm lens, quiet and intimate like a film still.",
             "fits": ["story", "explainer", "commentary", "tutorial"]},
    "golden": {"name": "Golden hour", "look": "Low warm sun, long soft shadows, warm amber colour, light haze.", "fits": ["vlog", "promo", "story"]},
    "night": {"name": "Moody night / neon", "look": "Night, low-key light from neon signs and practicals, deep shadows, cool cyan and magenta accents.",
              "fits": ["story", "commentary", "launch"]},
    "studio": {"name": "Studio desk / tech", "look": "Modern desk setup, soft key light with a cool monitor glow, shallow depth of field.",
               "fits": ["tutorial", "explainer", "review", "podcast"]},
    "bold": {"name": "Bold energy", "look": "Hard daylight, saturated colour, low angle, 24–35 mm lens, high energy.", "fits": ["ads", "launch", "promo"]},
}

TEXT_STYLES = {"box": "white box, dark text", "outline": "white text, dark outline", "none": "no on-screen text"}
SOUNDS = {
    "spoken": "Kling 4.0 speaks the hook line in the clip, with ambience",
    "voiceover": "Artlist voice-over for the line (cleanest; lips will not match a face on camera)",
    "music": "no spoken line: ambience plus an Artlist music sting",
    "silent": "ambience only; the text carries the hook",
}
PLANS = {
    "draft-final": "Kling 4.0 Flash draft (cheap), then a Kling 4.0 1080p final after you approve",
    "draft-only": "Kling 4.0 Flash 720p only (cheapest)",
    "final-only": "straight to Kling 4.0 1080p (fewer credits overall, no preview)",
}


def looks_for(vtype):
    return sorted(LOOKS, key=lambda k: vtype not in LOOKS[k]["fits"])


# ---------- target market ----------
# Filled in automatically from where the user is (their device's region), shown in the recap,
# changeable with `set market=XX`. It shapes the audience wording, the model options and the
# default language; the chat language never does.
MARKETS = {
    "ID": {"name": "Indonesia", "language": "Indonesian", "shop": "TikTok Shop, Shopee",
           "female": [("indonesian", "Indonesian", "warm tan skin, long black hair"),
                      ("chinese-indonesian", "Chinese-Indonesian", "fair skin, long straight black hair"),
                      ("hijab", "Indonesian, hijab", "modest styling, soft neutral hijab"),
                      ("korean", "Korean", "K-fashion casual styling")],
           "male": [("indonesian", "Indonesian", "warm tan skin, short black hair"),
                    ("chinese-indonesian", "Chinese-Indonesian", "fair skin, short textured black hair"),
                    ("javanese-smart", "Indonesian, clean-cut", "neat short hair, smart casual"),
                    ("korean", "Korean", "K-fashion casual styling")]},
    "MY": {"name": "Malaysia", "language": "Malay", "shop": "TikTok Shop, Shopee",
           "female": [("malay", "Malay", ""), ("malay-hijab", "Malay, hijab", ""), ("chinese-malaysian", "Chinese-Malaysian", ""), ("indian-malaysian", "Indian-Malaysian", "")],
           "male": [("malay", "Malay", ""), ("chinese-malaysian", "Chinese-Malaysian", ""), ("indian-malaysian", "Indian-Malaysian", ""), ("korean", "Korean", "")]},
    "SG": {"name": "Singapore", "language": "English", "shop": "Shopee, Lazada",
           "female": [("chinese-singaporean", "Chinese-Singaporean", ""), ("malay", "Malay", ""), ("indian", "Indian-Singaporean", ""), ("eurasian", "Eurasian", "")],
           "male": [("chinese-singaporean", "Chinese-Singaporean", ""), ("malay", "Malay", ""), ("indian", "Indian-Singaporean", ""), ("eurasian", "Eurasian", "")]},
    "PH": {"name": "Philippines", "language": "English", "shop": "TikTok Shop, Shopee",
           "female": [("filipina", "Filipina", ""), ("filipino-chinese", "Filipino-Chinese", ""), ("mestiza", "Filipino mixed heritage", ""), ("korean", "Korean", "")],
           "male": [("filipino", "Filipino", ""), ("filipino-chinese", "Filipino-Chinese", ""), ("mestizo", "Filipino mixed heritage", ""), ("korean", "Korean", "")]},
    "TH": {"name": "Thailand", "language": "Thai", "shop": "TikTok Shop, Shopee",
           "female": [("thai", "Thai", ""), ("thai-chinese", "Thai-Chinese", ""), ("korean", "Korean", ""), ("japanese", "Japanese", "")],
           "male": [("thai", "Thai", ""), ("thai-chinese", "Thai-Chinese", ""), ("korean", "Korean", ""), ("japanese", "Japanese", "")]},
    "VN": {"name": "Vietnam", "language": "Vietnamese", "shop": "TikTok Shop, Shopee",
           "female": [("vietnamese", "Vietnamese", ""), ("korean", "Korean", ""), ("chinese", "Chinese", ""), ("japanese", "Japanese", "")],
           "male": [("vietnamese", "Vietnamese", ""), ("korean", "Korean", ""), ("chinese", "Chinese", ""), ("japanese", "Japanese", "")]},
    "JP": {"name": "Japan", "language": "Japanese", "shop": "Rakuten, Instagram",
           "female": [("japanese", "Japanese", ""), ("korean", "Korean", ""), ("japanese-mixed", "Japanese mixed heritage", ""), ("chinese", "Chinese", "")],
           "male": [("japanese", "Japanese", ""), ("korean", "Korean", ""), ("japanese-mixed", "Japanese mixed heritage", ""), ("chinese", "Chinese", "")]},
    "KR": {"name": "South Korea", "language": "Korean", "shop": "Musinsa, Instagram",
           "female": [("korean", "Korean", ""), ("japanese", "Japanese", ""), ("chinese", "Chinese", ""), ("korean-mixed", "Korean mixed heritage", "")],
           "male": [("korean", "Korean", ""), ("japanese", "Japanese", ""), ("chinese", "Chinese", ""), ("korean-mixed", "Korean mixed heritage", "")]},
    "IN": {"name": "India", "language": "Hindi", "shop": "Instagram, Myntra",
           "female": [("north-indian", "North Indian", ""), ("south-indian", "South Indian", ""), ("punjabi", "Punjabi", ""), ("bengali", "Bengali", "")],
           "male": [("north-indian", "North Indian", ""), ("south-indian", "South Indian", ""), ("punjabi", "Punjabi", ""), ("bengali", "Bengali", "")]},
    "US": {"name": "United States", "language": "English", "shop": "TikTok Shop, Amazon",
           "female": [("white-american", "White American", ""), ("black-american", "Black American", ""), ("latina", "Latina", ""), ("asian-american", "Asian American", "")],
           "male": [("white-american", "White American", ""), ("black-american", "Black American", ""), ("latino", "Latino", ""), ("asian-american", "Asian American", "")]},
    "GB": {"name": "United Kingdom", "language": "English", "shop": "TikTok Shop, ASOS",
           "female": [("white-british", "White British", ""), ("black-british", "Black British", ""), ("british-south-asian", "British South Asian", ""), ("mixed-british", "Mixed British", "")],
           "male": [("white-british", "White British", ""), ("black-british", "Black British", ""), ("british-south-asian", "British South Asian", ""), ("mixed-british", "Mixed British", "")]},
    "AU": {"name": "Australia", "language": "English", "shop": "TikTok Shop, Instagram",
           "female": [("white-australian", "White Australian", ""), ("asian-australian", "Asian Australian", ""), ("mixed-australian", "Mixed Australian", ""), ("south-asian-australian", "South Asian Australian", "")],
           "male": [("white-australian", "White Australian", ""), ("asian-australian", "Asian Australian", ""), ("mixed-australian", "Mixed Australian", ""), ("south-asian-australian", "South Asian Australian", "")]},
    "GLOBAL": {"name": "Global (English)", "language": "English", "shop": "TikTok, Instagram, YouTube",
               "female": [("east-asian", "East Asian", ""), ("white", "White", ""), ("black", "Black", ""), ("latina", "Latina", "")],
               "male": [("east-asian", "East Asian", ""), ("white", "White", ""), ("black", "Black", ""), ("latino", "Latino", "")]},
}
# Time zones that point to a country when the locale has no region.
TZ_MARKET = {"Asia/Jakarta": "ID", "Asia/Makassar": "ID", "Asia/Jayapura": "ID", "Asia/Pontianak": "ID",
             "Asia/Kuala_Lumpur": "MY", "Asia/Singapore": "SG", "Asia/Manila": "PH", "Asia/Bangkok": "TH",
             "Asia/Ho_Chi_Minh": "VN", "Asia/Tokyo": "JP", "Asia/Seoul": "KR", "Asia/Kolkata": "IN",
             "Europe/London": "GB", "Australia/Sydney": "AU", "Australia/Melbourne": "AU"}
AGES = [("18-24", "18–24"), ("25-34", "25–34"), ("35-44", "35–44"), ("45+", "45+")]
GENDERS = [("female", "Female"), ("male", "Male"), ("all", "All genders")]


def market(code):
    return MARKETS.get((code or "").upper()) or MARKETS["GLOBAL"]


# ---------- model looks (one list for every market) ----------
# id: (name, extra detail). The market only changes the ORDER, never what is available.
RACES = {
    "indonesian": ("Indonesian", "warm tan skin, black hair"),
    "chinese-indonesian": ("Chinese-Indonesian", "fair skin, straight black hair"),
    "hijab": ("Indonesian / Malay, hijab", "modest styling, soft neutral hijab (women)"),
    "malay": ("Malay", ""),
    "filipino": ("Filipino", ""),
    "thai": ("Thai", ""),
    "vietnamese": ("Vietnamese", ""),
    "japanese": ("Japanese", ""),
    "korean": ("Korean", ""),
    "chinese": ("Chinese", ""),
    "indian": ("Indian / South Asian", ""),
    "middle-eastern": ("Middle Eastern", ""),
    "white-american": ("White American", ""),
    "black": ("Black / African American", ""),
    "latin": ("Latina / Latino", ""),
    "brazilian": ("Brazilian", ""),
    "western-european": ("Western European (French, Italian, Spanish)", ""),
    "northern-european": ("Northern European / Scandinavian", "fair skin, light hair"),
    "eastern-european": ("Eastern European / Slavic", ""),
    "mixed": ("Mixed heritage", ""),
}
# Language of the hook -> default market, and the market's preferred order of looks.
LANG_MARKET = {"indonesian": "ID", "english": "US", "japanese": "JP", "korean": "KR", "malay": "MY", "thai": "TH",
               "vietnamese": "VN", "filipino": "PH", "tagalog": "PH", "hindi": "IN", "spanish": "LATAM",
               "portuguese": "BR", "french": "EU", "german": "EU", "italian": "EU", "chinese": "CN", "mandarin": "CN", "arabic": "ME"}
RACE_ORDER = {
    "ID": ["indonesian", "chinese-indonesian", "hijab", "korean", "japanese"],
    "MY": ["malay", "hijab", "chinese", "indian"], "SG": ["chinese", "malay", "indian", "mixed"],
    "PH": ["filipino", "mixed", "korean"], "TH": ["thai", "chinese", "korean"], "VN": ["vietnamese", "korean"],
    "JP": ["japanese", "korean", "mixed"], "KR": ["korean", "japanese"], "CN": ["chinese", "korean", "japanese"],
    "IN": ["indian"], "ME": ["middle-eastern", "indian"],
    "US": ["white-american", "black", "latin", "korean", "japanese", "mixed"],
    "GB": ["northern-european", "black", "indian", "mixed"], "AU": ["white-american", "mixed", "chinese"],
    "LATAM": ["latin", "brazilian", "white-american"], "BR": ["brazilian", "latin"],
    "EU": ["western-european", "northern-european", "eastern-european", "black"],
    "GLOBAL": ["white-american", "korean", "latin", "black", "japanese"],
}
for _code, _name, _lang in (("CN", "China", "Chinese"), ("ME", "Middle East", "Arabic"), ("LATAM", "Latin America", "Spanish"),
                            ("BR", "Brazil", "Portuguese"), ("EU", "Europe", "English")):
    MARKETS.setdefault(_code, {"name": _name, "language": _lang, "shop": "", "female": [], "male": []})


def races_for(code):
    first = RACE_ORDER.get((code or "").upper(), RACE_ORDER["GLOBAL"])
    return first + [r for r in RACES if r not in first]


def market_for_language(lang):
    return LANG_MARKET.get((lang or "").strip().lower())

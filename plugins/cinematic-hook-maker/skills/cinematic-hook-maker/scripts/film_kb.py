"""Film-language library for the Cinematic Hook Maker.

One source for the vocabulary used by `studio.py vocab`, `direct` and `compose`,
and for references/film-language.md (regenerate it with `studio.py vocab --write`).

Every entry: id, name, use (when to choose it), words (what goes into the prompt).
Atmosphere entries also carry `still` (a frozen instant, for image prompts) and
`motion` (how it behaves over time, for video prompts), because a still cannot
show a flicker and a video should not restate what the first frame already shows.
"""

def e(id, name, use, words, **kw):
    d = {"id": id, "name": name, "use": use, "words": words}
    d.update(kw)
    return d


LIBRARY = {
    "style": ("Style (the world the picture belongs to)", [
        e("photoreal", "Photoreal Cinema", "Believable people, grounded stories", "frame grab from a digital cinema camera, believable people with natural skin texture, real materials"),
        e("blockbuster", "Blockbuster", "Scale and spectacle", "large-scale feature-film production, purposeful spectacle, clear readable action"),
        e("indie", "Indie Film", "Intimate, personal, unpolished", "independent-film naturalism, observed detail, restrained art direction"),
        e("documentary", "Documentary", "Observed, unstaged reality", "observational documentary footage, unforced framing, available light"),
        e("noir", "Neo-Noir", "Crime, secrets, intrigue", "modern neo-noir, sculpted shadows, strong silhouettes"),
        e("darkfantasy", "Dark Fantasy", "Mythic worlds and dread", "grounded dark fantasy, tactile weathered surfaces, uncanny scale"),
        e("scifi", "Grounded Sci-Fi", "Believable future worlds", "grounded science fiction, plausible worn technology, practical lights in the set"),
        e("anime", "Cinematic Anime", "Stylised 2D drama and action", "high-quality cinematic 2D anime, expressive character design, disciplined composition, not photorealistic"),
        e("stopmotion", "Stop Motion", "Handmade, tactile animation", "handcrafted stop-motion, visible material texture, miniature sets, not photorealistic"),
        e("vintage", "Vintage Film", "Period stories, memory", "period motion-picture look, gentle film grain, authentic period production design"),
        e("dreamreal", "Dream Realism", "Surreal but coherent", "photographic realism with one impossible element, spatially coherent"),
        e("foundfootage", "Found Footage", "Raw, subjective terror", "consumer-camera found footage, imperfect handheld framing, available light, sensor noise"),
        e("commercial", "Premium Commercial", "Products and materials", "premium commercial photography, precise material detail, controlled highlights"),
        e("western", "Modern Western", "Landscape, dust, grit", "modern western, weathered materials, wide natural landscapes"),
    ]),
    "colour": ("Colour (palette through light and set first, grade second)", [
        e("neutral", "Natural Neutral", "Everyday realism; the realism default", "neutral true-to-life colour, accurate skin tones, no colour grading"),
        e("cold", "Cold Blue", "Mystery, isolation, horror", "cool blue-grey palette from the light sources, controlled saturation, neutral skin"),
        e("tealorange", "Teal and Orange", "Action, subject against background", "warm practical light on skin against cool ambient shadows, restrained, natural skin"),
        e("amber", "Warm Amber", "Hope, nostalgia, romance", "warm golden light, rich natural midtones, soft highlights"),
        e("desat", "Desaturated", "Bleak drama, dystopia", "muted low-saturation palette, grey midtones, firm blacks"),
        e("mono", "Black and White", "Noir, graphic contrast", "black-and-white photograph, rich blacks, luminous grey highlights"),
        e("sickly", "Sickly Green", "Institutions, decay", "faint green-cyan cast from fluorescent tubes, muted skin"),
        e("pastel", "Soft Pastel", "Dreams, gentle fantasy", "airy pastel set colours: peach, lavender, muted mint"),
        e("crimson", "Crimson Accent", "Danger, obsession", "one crimson accent against charcoal neutrals"),
        e("steelcyan", "Steel and Cyan", "High-tech tension", "steel-blue palette with small cyan practical lights"),
        e("earth", "Earthy", "Rural life, history", "ochre, olive and warm stone tones"),
        e("highcon", "High Contrast", "Silhouette, graphic drama", "deep blacks, firm contrast, few bright highlights"),
        e("bleach", "Bleach Bypass", "Gritty action, war", "low saturation with strong contrast, silvery highlights"),
        e("sunwashed", "Sun-Washed", "Summer memory, coming of age", "sun-washed highlights, slightly lifted blacks, warm pastel midtones"),
    ]),
    "size": ("Shot size and composition", [
        e("xwide", "Extreme Wide", "Geography and scale", "extreme wide establishing frame, the environment dominates"),
        e("wide", "Wide", "Whole action in its space", "wide shot, subject and surroundings clearly visible"),
        e("full", "Full Body", "Gesture, body language", "full-body framing, head to feet in frame"),
        e("cowboy", "Cowboy", "Stance, readiness", "medium-full framing from mid-thigh up"),
        e("medium", "Medium", "Behaviour and exchange", "medium shot from the waist up"),
        e("mcu", "Medium Close-Up", "Conversation, emotion with context", "medium close-up, face and shoulders"),
        e("cu", "Close-Up", "Emotion, reaction, decision", "close-up on the face"),
        e("ecu", "Extreme Close-Up", "Eyes, a clue, fine detail", "extreme close-up on the one detail that carries the story"),
        e("pov", "POV", "Inside a character", "point of view from the character's eye line"),
        e("ots", "Over the Shoulder", "Confrontation, dialogue", "over-the-shoulder, a soft foreground shoulder, the other person sharp"),
        e("two", "Two-Shot", "A relationship or conflict", "two-shot, both people readable"),
        e("insert", "Insert", "Plant or pay off an object", "insert of one meaningful object"),
        e("silhouette", "Silhouette", "Mystery, threat", "subject as a readable silhouette against a brighter background"),
        e("negspace", "Negative Space", "Isolation, anticipation", "subject small and off-centre, deliberate empty space"),
        e("symmetry", "Centred Symmetry", "Control, ritual, unease", "precisely centred symmetrical frame, clean leading lines"),
        e("macro", "Macro", "Material detail", "macro detail, precise separation from the background"),
    ]),
    "angle": ("Camera angle", [
        e("eye", "Eye Level", "Neutral, personal", "eye-level camera"),
        e("low", "Low Angle", "Power, menace", "low angle looking up, the subject imposing"),
        e("high", "High Angle", "Fragility, isolation", "high angle looking down, the subject small"),
        e("dutch", "Dutch Tilt", "Instability; use once", "slight Dutch tilt"),
        e("overhead", "Overhead", "Pattern, layout", "top-down overhead view"),
        e("ground", "Ground Level", "Footsteps, danger, scale", "camera near the floor"),
        e("worm", "Worm's Eye", "Towering scale", "near-vertical view up from the ground"),
        e("profile", "Profile", "Silhouette, facial line", "clean side profile"),
        e("threequarter", "Three-Quarter", "Natural portrait volume", "three-quarter view"),
        e("rear", "Rear", "Following, anonymity", "from behind the subject, toward where they are going"),
    ]),
    "move": ("Camera movement (one per shot)", [
        e("static", "Locked-Off", "Dread, dialogue, precision", "locked-off static camera"),
        e("pushin", "Slow Push-In", "Realisation, pressure", "slow push-in toward the subject"),
        e("pullout", "Pull-Back", "Reveal, isolation", "slow pull-back revealing the surroundings"),
        e("track", "Tracking Follow", "Travel with someone", "camera tracks with the subject at a constant distance"),
        e("lateral", "Lateral Track", "Reveal space with parallax", "sideways tracking with foreground parallax"),
        e("panleft", "Pan Left", "Reveal or follow left", "steady pan to the left"),
        e("panright", "Pan Right", "Reveal or follow right", "steady pan to the right"),
        e("tiltup", "Tilt Up", "Height, a looming threat", "slow tilt up"),
        e("tiltdown", "Tilt Down", "Reveal below", "slow tilt down"),
        e("orbit", "Orbit", "Hero moment, turning point", "camera arcs around the subject, keeping orientation"),
        e("craneup", "Crane Up", "Open out, end a sequence", "camera rises to reveal the wider world"),
        e("cranedown", "Crane Down", "Enter the scene", "camera descends toward the subject"),
        e("handheld", "Handheld", "Panic, immediacy, realism", "handheld camera with slight natural shake"),
        e("float", "Floating Follow", "Dreamlike glide", "smooth stabilised floating camera"),
        e("rack", "Rack Focus", "Redirect attention", "static camera, focus shifts from foreground to background"),
        e("zoom", "Slow Zoom", "Uneasy attention", "slow optical zoom in, camera position fixed"),
        e("aerial", "Aerial Drift", "Landscape, scope", "slow aerial drift over the landscape"),
        e("povwalk", "POV Walk", "Immersion, discovery", "first-person forward walk with gentle step motion"),
        e("whip", "Whip Pan", "Energy, a hidden cut", "fast whip pan"),
        e("dollyzoom", "Dolly Zoom", "Vertigo, shock", "dolly zoom: background stretches while the subject stays the same size"),
    ]),
    "light": ("Light (always a named source)", [
        e("motivated", "Scene-Motivated", "Use the light already in the scene", "light motivated by the sources in the scene, consistent direction"),
        e("daylight", "Daylight", "Exterior realism", "natural daylight with consistent shadow direction"),
        e("hardsun", "Hard Sun", "Real, graphic, summer", "hard direct sun from one side, sharp shadows, face in bounced open shade"),
        e("window", "Soft Window", "Intimacy, faces", "soft directional window light with gentle falloff"),
        e("golden", "Golden Hour", "Hope, nostalgia", "low golden-hour sun, long shadows"),
        e("bluehour", "Blue Hour", "Quiet melancholy", "dim blue-hour ambient light, last glow in the sky"),
        e("fluorescent", "Cold Fluorescent", "Hospital, institution", "cold overhead fluorescent tubes, clinical falloff"),
        e("lowkey", "Low-Key", "Threat, mystery", "low-key light, small pools of motivated light, deep shadow"),
        e("moon", "Moonlight", "Night suspense", "soft moonlight, subdued exposure"),
        e("neon", "Neon Practicals", "City noir, sci-fi", "light from neon signs and fixtures in the scene"),
        e("candle", "Candlelight", "Period, dread", "flickering warm candlelight, fast falloff"),
        e("overcast", "Overcast", "Bleak outdoor realism", "diffused overcast light, soft shadows"),
        e("rim", "Rim Backlight", "Silhouette, separation", "motivated backlight tracing the subject's edges"),
        e("highkey", "High-Key", "Clean, commercial, sterile", "bright high-key light, soft controlled shadows"),
        e("hardside", "Hard Side Light", "Stark conflict", "hard side light carving the face"),
        e("flashlight", "Flashlight", "Exploration, dread", "a single handheld flashlight as the key light"),
        e("screen", "Screen Glow", "Isolation, night, secrets", "a phone or monitor screen as the only light, lighting the nearest face or surface from below"),
        e("fire", "Firelight", "Danger, survival", "warm flickering firelight on the nearest surfaces"),
        e("underwater", "Underwater", "Surreal, submerged", "filtered light from above with moving caustic patterns"),
    ]),
    "atmo": ("Atmosphere and texture (one per shot, physically motivated)", [
        e("clean", "None Added", "Keep the scene's own conditions", "", still="", motion=""),
        e("haze", "Light Haze", "Depth without hiding anything", "barely visible haze separating the layers", still="barely visible haze separating the layers", motion="the existing haze drifts slowly"),
        e("fog", "Ground Fog", "Mystery, low visibility", "thin fog lying low on the ground", still="thin fog lying low on the ground", motion="the low fog creeps slowly"),
        e("densefog", "Dense Fog", "Isolation, uncertainty", "dense layered fog hiding the distance", still="dense layered fog hiding the distance", motion="the fog keeps its density"),
        e("rain", "Rain", "Noir, tension, sadness", "light rain, wet reflective surfaces", still="visible light rain, wet reflective surfaces", motion="the rain keeps falling at the same rate"),
        e("downpour", "Heavy Rain", "Emergency, action", "heavy rain hitting clothes and ground", still="visible heavy rain, soaked surfaces", motion="heavy rain keeps striking clothes and ground"),
        e("dust", "Dust in the Light", "Abandoned interiors", "dust suspended in the light beams", still="dust suspended in the light beams", motion="dust drifts slowly through the beams"),
        e("flicker", "Light Flicker", "Electrical unease", "an existing practical light flickers", still="uneven light from a failing fixture at one instant", motion="the existing practical light flickers occasionally"),
        e("smoke", "Thin Smoke", "Industrial threat, aftermath", "thin smoke in the air", still="visible wisps of smoke", motion="wisps of smoke move naturally"),
        e("wind", "Wind", "Life in a still frame", "breeze moving hair and light fabric", still="hair and light fabric caught mid-gust", motion="a gentle breeze moves hair and light fabric"),
        e("snow", "Light Snow", "Stillness, cold", "light snow", still="snowflakes frozen mid-air", motion="light snow drifts down and settles"),
        e("mist", "Morning Mist", "Poetic outdoor depth", "fine mist receding into the distance", still="fine mist receding into the distance", motion="the mist thins slowly"),
        e("sparks", "Sparks", "Impact, machinery", "sparks at a point of contact", still="sparks frozen at the point of contact", motion="brief sparks burst from the point of contact"),
        e("embers", "Embers", "Fire, aftermath", "embers near a heat source", still="glowing embers near the heat source", motion="embers drift up from the heat source"),
        e("grain", "Film Grain", "Texture, period, realism", "fine film grain", still="fine film grain", motion="fine film grain"),
        e("noise", "Sensor Noise", "Night realism, found footage", "visible sensor noise in the shadows", still="visible sensor noise in the shadows", motion="sensor noise in the dark areas"),
    ]),
    "lens": ("Lens", [
        e("auto", "Director's Choice", "Match the shot size", ""),
        e("18", "18 mm Ultra Wide", "Architecture, big spaces, unease", "18 mm ultra-wide lens, strong perspective"),
        e("24", "24 mm Wide", "Environment and character", "24 mm wide lens"),
        e("28", "28 mm Environmental", "Streets, interiors, handheld", "28 mm lens"),
        e("35", "35 mm Storytelling", "Balanced cinema perspective", "35 mm lens"),
        e("50", "50 mm Natural", "Neutral, intimate", "50 mm lens, natural perspective"),
        e("65", "65 mm Portrait", "Flattering isolation", "65 mm lens, gentle compression"),
        e("85", "85 mm Portrait", "Faces, background separation", "85 mm portrait lens, soft background"),
        e("macro100", "100 mm Macro", "Textures, clues, products", "100 mm macro lens"),
        e("anamorphic", "Anamorphic", "Widescreen drama", "anamorphic lens, oval out-of-focus highlights, gentle horizontal flares"),
        e("vintage", "Vintage Glass", "Softness, memory", "vintage lens, slight softness around highlights"),
        e("deep", "Deep Focus", "Keep every layer readable", "deep focus, foreground and background sharp"),
    ]),
    "pace": ("Pace (video only)", [
        e("measured", "Measured", "Natural progression", "measured, human-scale rhythm"),
        e("slowburn", "Slow-Burn", "Hold tension and silence", "slow-building, restrained timing, long held pauses"),
        e("urgent", "Urgent", "Action, escape", "urgent but physically plausible movement"),
        e("dream", "Dreamlike", "Eerie time", "slightly slowed, unhurried"),
        e("tender", "Tender", "Intimacy", "quiet, tender, unhurried"),
        e("energetic", "Energetic", "Commercial, social", "confident energetic tempo, one clear main action"),
        e("observational", "Observational", "Documentary", "unforced, observed"),
        e("ritual", "Ritual", "Eerie repetition", "deliberate, ceremonial"),
    ]),
    "intent": ("Intent (what the shot must deliver)", [
        e("establish", "Establish", "Introduce a place or mood", "keep the space and where things are clearly readable"),
        e("reveal", "Reveal", "Expose a clue or change", "guide the eye to the reveal at the end"),
        e("emotion", "Emotion", "Expression first", "hold on the face; small believable reactions"),
        e("tension", "Suspense", "Build expectation", "stretch the anticipation without changing the outcome"),
        e("action", "Action", "Physical motion", "keep cause and effect of every movement readable"),
        e("dialogue", "Dialogue", "A clear exchange", "keep eyelines and positions consistent"),
        e("discovery", "Discovery", "Follow the observer", "reveal the space in the order the character notices it"),
        e("product", "Product Hero", "Show the product", "show material, silhouette and the one useful detail"),
        e("transition", "Transition", "Bridge to the next shot", "end on a movement or shape the next shot can continue"),
        e("climax", "Climax", "The decisive moment", "give the decisive action the frame"),
    ]),
    "transition": ("Transition into the next shot", [
        e("cut", "Straight Cut", "Default", "cut"),
        e("cutmove", "Cut on Movement", "Hide the cut inside action", "cut on movement"),
        e("match", "Match Cut", "Link two shapes or actions", "match cut on shape or action"),
        e("handoff", "Hand-off Frame", "Same action continues", "the last frame becomes the next shot's first frame"),
        e("whip", "Whip Pan", "Energy, a hidden join", "whip pan into the next shot"),
        e("smash", "Smash Cut", "Shock, comic contrast", "smash cut"),
        e("jcut", "J-Cut", "Sound leads the picture", "next shot's sound starts early"),
        e("lcut", "L-Cut", "Sound lingers", "this shot's sound carries over"),
        e("dissolve", "Dissolve", "Time passing, memory", "dissolve"),
        e("black", "Cut to Black", "End, cliffhanger", "cut to black"),
    ]),
}

# Quick Director: a starting point per genre. Everything is a suggestion to review.
GENRES = {
    "horror":      {"name": "Horror",      "style": "photoreal",  "colour": "cold",      "size": "wide",   "angle": "eye",          "move": "pushin",   "light": "lowkey",     "atmo": "haze",   "lens": "35", "pace": "slowburn",      "intent": "tension"},
    "thriller":    {"name": "Thriller",    "style": "noir",       "colour": "desat",     "size": "medium", "angle": "eye",          "move": "track",    "light": "lowkey",     "atmo": "clean",  "lens": "35", "pace": "urgent",        "intent": "tension"},
    "mystery":     {"name": "Mystery",     "style": "noir",       "colour": "cold",      "size": "insert", "angle": "eye",          "move": "rack",     "light": "lowkey",     "atmo": "haze",   "lens": "50", "pace": "slowburn",      "intent": "reveal"},
    "drama":       {"name": "Drama",       "style": "indie",      "colour": "neutral",   "size": "mcu",    "angle": "eye",          "move": "static",   "light": "window",     "atmo": "clean",  "lens": "50", "pace": "tender",        "intent": "emotion"},
    "romance":     {"name": "Romance",     "style": "photoreal",  "colour": "amber",     "size": "medium", "angle": "eye",          "move": "pushin",   "light": "golden",     "atmo": "clean",  "lens": "50", "pace": "tender",        "intent": "emotion"},
    "action":      {"name": "Action",      "style": "blockbuster","colour": "tealorange","size": "wide",   "angle": "low",          "move": "track",    "light": "daylight",   "atmo": "clean",  "lens": "35", "pace": "urgent",        "intent": "action"},
    "scifi":       {"name": "Sci-Fi",      "style": "scifi",      "colour": "steelcyan", "size": "wide",   "angle": "eye",          "move": "pullout",  "light": "neon",       "atmo": "haze",   "lens": "24", "pace": "measured",      "intent": "establish"},
    "fantasy":     {"name": "Fantasy",     "style": "darkfantasy","colour": "earth",     "size": "wide",   "angle": "low",          "move": "craneup",  "light": "golden",     "atmo": "mist",   "lens": "24", "pace": "dream",         "intent": "reveal"},
    "dream":       {"name": "Dream / Surreal", "style": "dreamreal", "colour": "pastel", "size": "wide",   "angle": "eye",          "move": "float",    "light": "highkey",    "atmo": "haze",   "lens": "35", "pace": "dream",         "intent": "discovery"},
    "documentary": {"name": "Documentary", "style": "documentary","colour": "neutral",   "size": "medium", "angle": "eye",          "move": "handheld", "light": "daylight",   "atmo": "clean",  "lens": "35", "pace": "observational", "intent": "establish"},
    "product":     {"name": "Product / Ad","style": "commercial", "colour": "neutral",   "size": "cu",     "angle": "threequarter", "move": "orbit",    "light": "highkey",    "atmo": "clean",  "lens": "85", "pace": "energetic",     "intent": "product"},
    "western":     {"name": "Western",     "style": "western",    "colour": "earth",     "size": "wide",   "angle": "low",          "move": "lateral",  "light": "golden",     "atmo": "dust",   "lens": "35", "pace": "measured",      "intent": "establish"},
    "anime":       {"name": "Anime",       "style": "anime",      "colour": "pastel",    "size": "medium", "angle": "eye",          "move": "track",    "light": "daylight",   "atmo": "clean",  "lens": "35", "pace": "energetic",     "intent": "action"},
    "invasion":    {"name": "Sci-Fi Horror / Invasion", "style": "photoreal", "colour": "cold", "size": "wide", "angle": "eye",     "move": "handheld", "light": "lowkey",     "atmo": "noise",  "lens": "35", "pace": "slowburn",      "intent": "tension"},
}

# Settings that Style Lock holds across every shot; camera choices stay per shot.
LOCK_KEYS = ["style", "colour", "light", "atmo", "lens"]
SHOT_KEYS = ["size", "angle", "move", "lens", "light", "atmo", "pace", "intent", "transition"]

# Starter scenes per genre, for "give me an idea" or a quick demo.
RECIPES = [
    ("horror", "Doorway", "A nervous woman stands before a half-open metal door; a shadow shifts behind the gap."),
    ("horror", "Silent Corridor", "A lone figure walks a deserted hospital corridor while one fluorescent tube flickers far ahead."),
    ("horror", "Reflection", "A man looks into a bathroom mirror and sees a shape standing behind him that is not in the room."),
    ("horror", "Forest Presence", "A lost hiker hears a branch snap and turns toward a dark clearing."),
    ("mystery", "The Hidden Note", "A detective finds a handwritten note under a loose floorboard in an empty apartment."),
    ("mystery", "Empty Platform", "A woman waits alone on a night platform; an unclaimed suitcase sits beside her bench."),
    ("mystery", "The Photograph", "Someone studies an old family photo and finds their own face in the background crowd."),
    ("thriller", "Stairwell", "A man runs down an emergency stairwell as heavy footsteps echo above him."),
    ("thriller", "Rooftop Standoff", "Two people face each other on a rain-soaked rooftop at night."),
    ("thriller", "The Passenger", "A commuter notices the same silent stranger following her through several train cars."),
    ("drama", "Kitchen Table", "A mother and daughter sit in silence at a kitchen table after an argument."),
    ("drama", "Outside Room 12", "A man hesitates outside a hospital room, gripping a folded letter."),
    ("drama", "Rain Window", "An old woman watches city rain from her window, a photograph in her lap."),
    ("romance", "Platform Reunion", "Two childhood friends recognise each other across a station platform at sunset."),
    ("romance", "Rooftop Confession", "A couple stands close under string lights above a night city."),
    ("action", "Market Chase", "A courier sprints through a crowded market while two pursuers push through the stalls behind."),
    ("action", "Bridge Rescue", "A firefighter edges along a storm-damaged bridge toward a stranded driver."),
    ("action", "Warehouse", "Two fighters face off in an empty warehouse, dust drifting through shafts of light."),
    ("scifi", "Ship Awakens", "A pilot enters a dormant cockpit as the instruments flicker on one by one."),
    ("scifi", "City Balcony", "A traveller stands on a balcony above a dense future city at night."),
    ("scifi", "The Memory", "A scientist studies a glowing holographic memory in a dark lab."),
    ("invasion", "The Knock", "During an invasion, a sister hides with her brother; their father's voice asks them to open the door."),
    ("invasion", "Last Broadcast", "A radio host alone in her studio reads evacuation orders as the ships descend over the city."),
    ("invasion", "Wave", "Stuck in gridlock as ships descend, a child waves at one, and it stops."),
    ("fantasy", "Forest Portal", "A traveller finds a glowing doorway between ancient trees in the mist."),
    ("fantasy", "Mountain Citadel", "A lone rider reaches the gates of a vast mountain fortress under storm clouds."),
    ("dream", "Gravity Shift", "A woman steps into a room where the furniture hangs still in mid-air."),
    ("dream", "Endless Hallway", "Someone walks a white hallway that stretches beyond sight."),
    ("documentary", "City Morning", "A street vendor sets up a food stall as the city wakes."),
    ("documentary", "Craftsmanship", "A watchmaker adjusts a tiny gear at a cluttered bench."),
    ("product", "Perfume Reveal", "A glass perfume bottle on polished stone; reflections slide across its surface."),
    ("product", "Sneaker Detail", "A running shoe on a plain plinth, its textures catching a hard side light."),
    ("western", "Arrival", "A lone rider approaches a weathered frontier town through sunlit dust."),
    ("anime", "Rainy Farewell", "A girl under an umbrella waits at a railway crossing in the rain."),
]


def find(cat, key):
    for item in LIBRARY[cat][1]:
        if item["id"] == key:
            return item
    return None


def count():
    return sum(len(v[1]) for v in LIBRARY.values())

# Visual formats, platforms and video types

The picture-and-motion half of a hook, where it is posted, and what the hook must do for each kind of video.
Generated from `scripts/hook_data.py` by `hookmaker.py write-refs`.

## Contents

1. Visual formats
2. Platforms
3. Video types

## 1. Visual formats

| id | Format | What it is | First frame | Motion | Mode, length |
|---|---|---|---|---|---|
| `result-first` | Result First | Open on the finished outcome, then cut to the start. | The finished result, perfectly lit, filling the frame. | A slow push-in on the result from frame one; it ends on a beat ready to cut back. | image-to-video, ~4 s |
| `pattern-interrupt` | Pattern Interrupt | An ordinary frame broken by one unexpected event in the first second. | A calm, ordinary moment a split second before something happens. | Within the first second the unexpected thing happens (a glass falls, a door bursts open); the camera reacts with a small jolt. | image-to-video, ~4 s |
| `impossible` | Impossible Visual | Something that cannot happen, happening calmly and photorealistically. | A real, believable place with one impossible element already starting. | The impossible thing completes (a bottle grows to the size of a building, the room fills with water without spilling); one steady camera move. | image-to-video, ~5 s |
| `scale-shift` | Scale Shift | Macro to giant, or a tiny world inside an everyday object. | Extreme macro detail that reads as a landscape. | The camera pulls back fast to reveal the real, ordinary scale. | image-to-video, ~4 s |
| `pov` | Point of View | The viewer's own eyes in a moment they know. | First-person view: hands, phone, steering wheel, desk, as the viewer would see them. | Subtle head-motion handheld; one thing in front of us goes wrong or right. | image-to-video, ~4 s |
| `face-to-camera` | Face to Camera | A person mid-sentence, eyes locked on the lens. | Medium close-up, the person already talking, eyes into the lens, hard natural light. | They deliver one short line with a gesture; slight handheld; lips sync to the line. | image-to-video, ~5 s |
| `hands-demo` | Hands Demo | Top-down or over-the-shoulder hands doing the key step. | Top-down view of hands and the object, clean surface, one hard light source. | The hands perform the single most satisfying step; static camera. | image-to-video, ~4 s |
| `before-after-cut` | Before / After Cut | Same framing, two states, a hard cut or a wipe. | The 'before' state; a second still makes the 'after' by editing the first. | Start and end frames: the camera holds while the state changes, or a fast wipe passes across. | first-and-last-frame, ~4 s |
| `reveal-pull` | Reveal Pull-Back | Tight on a puzzling detail, pull back to reveal what it is. | A tight detail that cannot be identified yet. | Camera pulls back steadily to reveal the full scene; ends on the reveal. | image-to-video, ~5 s |
| `question-card` | Question Card | One bold question as text over a moody, moving picture. | A clean, atmospheric picture with empty space where the text will sit. | Slow drift or push-in; nothing busy behind the words. | image-to-video, ~4 s |
| `countdown` | Countdown | A visible timer or number that creates urgency. | A clock, phone timer or number in frame beside the subject. | The countdown ticks while the subject acts fast; handheld energy. | image-to-video, ~5 s |
| `product-drop` | Product Drop | The product falls or slides into frame and lands with impact. | An empty hero surface with the product's exact look supplied as a reference. | The product drops into frame, lands with a small bounce, dust or water reacts, camera settles on the hero angle. | reference-to-video or first-and-last-frame, ~4 s |
| `transformation` | One-Take Transformation | A person, object or place changes in one unbroken move. | The starting state; the end state is an edited copy of it. | Start and end frames with an orbit or push; the change rides the camera move. | first-and-last-frame, ~5 s |
| `mistake-freeze` | Mistake Freeze | The exact instant something goes wrong, held. | The split second before the mistake. | The mistake happens and the action slows almost to a stop at the worst moment (add the freeze in the edit if the model doesn't hold). | image-to-video, ~4 s |
| `comparison` | Side by Side | Two options or two results at once. | A split frame or two objects side by side on one surface, evenly lit. | Both react to the same action at the same time; static camera. | image-to-video, ~4 s |
| `cinematic-cold-open` | Cinematic Cold Open | A film-like first shot already inside the tension. | A composed film frame with one source of light and one figure in trouble. | One deliberate camera move toward the threat or the face; ambient sound only. | image-to-video, ~5 s |

## 2. Platforms

Safe zones are approximate fractions of the frame that buttons and captions cover. Interfaces change; treat them as margins.

| id | Platform | Render | Deliver | Hook window | Keep clear (top / bottom / left / right) | Sound | Cover |
|---|---|---|---|---|---|---|---|
| `tiktok` | TikTok | 9:16 | 9:16 | 1–2 s | 10% / 25% / 6% / 16% | Most people watch with sound on, but the first frame must work muted. | The first frame often becomes the cover. Make it readable as a still. Native, fast, slightly raw beats over-produced. Text in the upper-middle third. |
| `reels` | Instagram Reels | 9:16 | 9:16 | 1–2 s | 12% / 22% / 6% / 14% | Many watch muted in feed. Burn the key words in. | The profile grid crops covers toward a vertical rectangle around 3:4: keep the subject and title centred. Aesthetic matters more here. Good-looking, clean light, one clear subject. |
| `shorts` | YouTube Shorts | 9:16 | 9:16 | 1–2 s | 10% / 22% / 6% / 16% | Sound on is common. A spoken line works well. | The frame chosen as the Short's thumbnail should state the promise on its own. Loops count: an ending that flows back into the first frame helps rewatches. |
| `youtube` | YouTube (long-form) | 16:9 | 16:9 | first 5–15 s | 6% / 14% / 5% / 5% | Sound on. The spoken promise carries the hook; picture proves it. | The thumbnail is separate: make a 16:9 still from the same first frame with one face or object and three words at most. The hook must match the title and thumbnail promise, then preview the payoff. |
| `facebook` | Facebook feed | 9:16 | 4:5 | 1–3 s | 8% / 18% / 6% / 6% | Mostly muted autoplay. Burned-in text is essential. | Crop from the 9:16 render to 4:5; keep subject and text in the middle. Older, broader audience: clarity over cleverness. |
| `linkedin` | LinkedIn | 1:1 | 1:1 | 1–3 s | 8% / 14% / 6% / 6% | Muted autoplay. Text carries it. | Square first frame with a clear human face or result. Professional tone: lessons, results, behind the scenes. Avoid clickbait. |
| `x` | X | 16:9 | 16:9 | 1–2 s | 6% / 12% / 5% / 5% | Muted autoplay. | First frame shows in the timeline; make it a statement. Short, bold, opinion-led. Square (1:1) also works well. |

## 3. Video types

| id | Type | The hook's job | Story types to try | Formats to try | Take care |
|---|---|---|---|---|---|
| `ads` | Paid ad / brand ad | Stop the thumb, name the problem or desire, show the product within 3 s. | mirror, before-after, open-loop | pattern-interrupt, result-first, product-drop, impossible | Keep logos and packaging exactly as supplied (edit from the real product photo). Claims must be true; platform ad policies apply. |
| `affiliate` | Affiliate / product recommendation | Make the viewer feel the problem, then show the product solving it fast. | mistake, mirror, someone-else | mistake-freeze, hands-demo, before-after-cut, comparison | Disclose the affiliate relationship in the caption. Show the real product, not an invented one. |
| `review` | Product review / comparison | Promise a verdict and tease it. | against-grain, crossroads, open-loop | comparison, result-first, reveal-pull | A review must reflect real use. Never generate fake owners or fake results presented as real. |
| `tutorial` | Tutorial / how-to | Show the finished result first, then promise the steps. | before-after, behind-curtain, lesson | result-first, hands-demo, before-after-cut, countdown | The result shown must be reachable with the steps taught. |
| `explainer` | Education / explainer | Pose a question the viewer suddenly needs answered. | open-loop, against-grain, secret | question-card, scale-shift, impossible, reveal-pull | Keep facts accurate; label illustrations of things nobody has filmed. |
| `testimonial` | UGC / testimonial style | A real-feeling person, mid-thought, with a specific result. | someone-else, before-after, mirror | face-to-camera, pov, before-after-cut | AI people may act a scripted scene, but never present an AI person as a real customer giving a genuine review. Use the user's own customers' words with permission, or label it as a dramatisation. |
| `vlog` | Vlog / lifestyle | Drop the viewer into the most alive moment of the day. | mirror, turning-point, clock | pov, cinematic-cold-open, pattern-interrupt | If the user appears, build from their own photos; never generate a real person without consent. |
| `story` | Micro-drama / short film / storytime | Start in the middle of trouble and raise one question. | secret, clock, open-loop, crossroads | cinematic-cold-open, mistake-freeze, reveal-pull, pattern-interrupt | In fiction the hook is a scene, not a sentence to camera. |
| `commentary` | News / commentary / opinion | State the take in the first line and show what it is about. | against-grain, secret, open-loop | question-card, face-to-camera, comparison | Do not generate realistic footage of real events or real people; use symbolic or clearly illustrative pictures. |
| `launch` | Product or course launch | Reveal the thing with the energy of an event. | clock, secret, behind-curtain | product-drop, reveal-pull, impossible, countdown | Keep the real product's look exact; show only features that exist. |
| `podcast` | Podcast / talking-head clip | Open on the most surprising sentence, with a picture that earns attention. | against-grain, lesson, secret | face-to-camera, question-card, pattern-interrupt | Use the user's real footage for the speaker; AI only for B-roll or the opening picture. |
| `promo` | Event / local business / real estate promo | Show the best moment of the place or event before anything else. | before-after, behind-curtain, clock | reveal-pull, cinematic-cold-open, impossible, countdown | Places and products must look like the real ones; edit from the user's photos. |

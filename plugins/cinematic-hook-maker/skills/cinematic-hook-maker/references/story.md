# Story: from an idea to a shot list

A generated film fails at the story stage far more often than at the pixel stage. Use this to give every shot a reason to exist before it gets a prompt.

## Contents
1. Logline
1b. Story type and hook
2. Beats, then shots
3. Format blueprints
4. Writing a micro-drama that holds attention
5. Dialogue economy
6. The shot list
7. Series bible and episode continuity

## 1. Logline

One sentence: **someone** wants **something**, but **something stands in the way**, and **this is what it costs**. If the idea has no want and no obstacle, it is a mood, and a mood sustains about eight seconds. Ask the user one question to find the want, or propose one.

> A night-shift nurse finds her own name on tomorrow's patient list and has until morning to learn who put it there.

## 1b. Story type and hook

Before the beats, choose what kind of story this is. `references/lines.md` holds twelve story types (Before and After, The Costly Mistake, The Turning Point, Behind the Curtain, Against the Grain, The Mirror, Someone Else's Story, The Open Loop, The Lesson, The Crossroads, The Ticking Clock, The Secret). Each gives a beat shape, three opening pictures, a way to open a scripted scene, and eight or nine opening lines with [slots] — one hundred in all, numbered 1–100. A spoken hook is always one of these lines: fill only its slots, or translate it faithfully; never write a new one unless the user says yes.

- **Creator videos, tutorials, ads and testimonials:** the type's beats can be the shot list, and a hook line can be the first spoken or on-screen line.
- **Fiction (micro-drama, short film, trailer):** use the type's fiction opening and opening pictures for the first shot. A character rarely says a hook to camera; the line becomes narration, a title card, or a first line of dialogue rewritten in the character's voice.
- **Combine at most two types**, for example a Ticking Clock built on a Secret. More than two and the film has no spine.
- Offer the user two or three hooks filled in for their project, never the empty template, and say which picture opens the film with each.

`studio.py hooks` lists the types, `studio.py hooks <type>` shows one in full with the library numbers, and `studio.py set hook_no=<N> hook="<line as spoken>"` records the choice (it sets the story type too) so the board and the handoff carry it. `studio.py validate` fails a hook with no library number.

## 2. Beats, then shots

Work in three passes. Do not skip to shots.

**Pass 1 — beats.** A beat is a change: in what a character knows, wants or feels. List them as plain sentences. A thirty-second piece carries three or four beats; a two-minute piece eight to ten.

**Pass 2 — the job of each shot.** For every beat decide what the audience must receive: a fact, a feeling, a question. One job per shot. A shot with two jobs does neither.

**Pass 3 — the picture.** Only now choose size, angle, movement and length (see `directing.md`).

For each shot also choose **one concrete detail** that carries the feeling: the unopened letters, a thumb worrying a ring, breath on cold glass. Detail is what separates a scene from a description. If a shot has no specific detail, it will look like everyone else's.

## 3. Format blueprints

Timings are starting points. Total length divided by these gives the shot count.

### Micro-drama episode (9:16, 45–90 s)
| Part | Share | Purpose |
|---|---|---|
| Hook | first 3 s | The most arresting image or line. Start in the middle of trouble. |
| Situation | 15% | Who, where, what they want — shown, not told. |
| Complication | 30% | The obstacle arrives and gets worse once. |
| Turn | 30% | A reveal or reversal changes what we thought. |
| Cliffhanger | last 10% | End on an unanswered question, cut one beat early. |

### Short film (16:9 or 21:9, 1–3 min)
Setup (20%) → disturbance (10%) → struggle with one escalation (40%) → crisis and choice (20%) → new normal in a single closing image (10%). The closing image should answer the opening image.

### Trailer (16:9 or 21:9, 30–60 s)
Cold open on one striking shot → the world in three quick shots → the problem stated in one line → rising montage, shots getting shorter → a silent beat → title → one last sting. Never resolve anything.

### Music video (any ratio, 30–90 s)
Break the track into sections. One visual idea per section, with a strong change at each section boundary. Performance shots, story shots and texture shots in rotation. Movement should hit the downbeats; note the tempo and choose shot lengths in whole bars.

### Brand or product film (16:9 or 9:16, 15–45 s)
A human moment the product belongs in → the product enters naturally → one hero shot of the product → benefit shown, not said → end frame with name. One message only. Keep any supplied logo and packaging exactly as provided.

For a longer commercial (30–60 s, about eight shots), use eight beats, one per shot:

| # | Beat | Job |
|---|---|---|
| 1 | Hook | The most arresting image in the film, in the first two seconds |
| 2 | Subject | Who or what this is about, shown in use |
| 3 | Curiosity | A question or a tension the viewer wants resolved |
| 4 | Feature or transformation | The one thing it does, shown happening |
| 5 | Core message | The single idea, said once, in picture or one line |
| 6 | Payoff | The emotional or practical result for a person |
| 7 | Climax | The hero shot: the strongest frame of the product or person |
| 8 | End frame | Name and call to action, held long enough to read |

Write down the target audience and the music direction with the shot list (`studio.py set audience=… music=…`); both shape pace, casting and sound, and both appear on the storyboard.

### One-take (any ratio, up to 30 s)
A journey with a start, three or four discoveries and an arrival. See `onetake-keyframes.md`.

### VFX shot (follows the source)
Not a story structure: a plan of what stays and what changes. See `vfx-mode.md`.

## 4. Writing a micro-drama that holds attention

- **Open late.** Begin after the argument has started, after the door has been kicked in.
- **Give each character a secret or a need** the other does not know. Scenes run on the gap.
- **Reverse expectations once per episode.** The helper is the threat; the victim planned it.
- **Use reaction shots.** A face receiving news is stronger than the news. Plan one close reaction for every important line.
- **Cut on the question.** End the episode the moment a new question is raised, before anyone answers.
- **Keep the cast to two or three.** Every added face is one more identity to hold steady.
- **Reuse two locations.** Consistency improves and the world feels real.

## 5. Dialogue economy

Generated dialogue works best in short exchanges. Aim for lines of twelve words or fewer, one line per shot or a two-line exchange per shot. Let the picture carry the information and the line carry the attitude. If a line explains what we can see, cut it. Time each line at about two and a half words per second and make sure the shot is long enough (`kling-4.md`, section 4).

## 6. The shot list

Present it to the user as a compact table and store it with `studio.py add-shot`:

| ID | Sec | Beat (the shot's job) | Picture | Mode | Sound |
|---|---|---|---|---|---|
| S01 | 4 | Hook: she finds her own name | CU chart, her thumb stops on a line; rack to her eyes | i2v | monitor beeps, her breath |
| S02 | 6 | She checks she is alone | MS corridor, slow push; lights cut out behind her one by one | i2v | fluorescent hum dying |
| S03 | 8 | The complication: the name was added an hour ago | OTS at a terminal; "Who's on shift tonight?" | i2v | line, keyboard |

Modes: `t2v` words only, `i2v` first frame, `frames` first and last, `keys` middle keyframes, `r2v` image references, `v2v` video reference.

Before generating, read the list top to bottom and check: does each shot change something, do two neighbouring shots differ in size or angle, and does the total match the target length?

## 7. Series bible and episode continuity

For anything with a second episode, keep a bible in the project file:

- **World** in three sentences, including the rule that makes it this world.
- **Cast**: name, want, secret, the distinctive visible traits, and the Artlist reference for their sheet.
- **Locations** with their light.
- **Look** in five facts (see `gpt-image-2-5.md`, section 8).
- **Open threads**: questions the last episode left unanswered.
- **What has been shown**: one line per episode.

When the user asks for the next episode, begin from the open threads, reuse the saved sheets and style kit unchanged, and start the new episode on the image the last one ended on.

# Film language library

149 techniques. Each has a use (when to choose it) and the words that go into the prompt. Choose by the shot's job, not by taste. The ids work with `studio.py add-shot`, `lock`, `direct` and `compose`.

Generated from `scripts/film_kb.py` by `studio.py vocab --write`. Edit that file, not this one.

## Contents

1. Style (the world the picture belongs to)
2. Colour (palette through light and set first, grade second)
3. Shot size and composition
4. Camera angle
5. Camera movement (one per shot)
6. Light (always a named source)
7. Atmosphere and texture (one per shot, physically motivated)
8. Lens
9. Pace (video only)
10. Intent (what the shot must deliver)
11. Transition into the next shot
12. Quick Director presets
13. Scene starters

## Style (the world the picture belongs to)

Key: `style`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `photoreal` | Photoreal Cinema | Believable people, grounded stories | frame grab from a digital cinema camera, believable people with natural skin texture, real materials |
| `blockbuster` | Blockbuster | Scale and spectacle | large-scale feature-film production, purposeful spectacle, clear readable action |
| `indie` | Indie Film | Intimate, personal, unpolished | independent-film naturalism, observed detail, restrained art direction |
| `documentary` | Documentary | Observed, unstaged reality | observational documentary footage, unforced framing, available light |
| `noir` | Neo-Noir | Crime, secrets, intrigue | modern neo-noir, sculpted shadows, strong silhouettes |
| `darkfantasy` | Dark Fantasy | Mythic worlds and dread | grounded dark fantasy, tactile weathered surfaces, uncanny scale |
| `scifi` | Grounded Sci-Fi | Believable future worlds | grounded science fiction, plausible worn technology, practical lights in the set |
| `anime` | Cinematic Anime | Stylised 2D drama and action | high-quality cinematic 2D anime, expressive character design, disciplined composition, not photorealistic |
| `stopmotion` | Stop Motion | Handmade, tactile animation | handcrafted stop-motion, visible material texture, miniature sets, not photorealistic |
| `vintage` | Vintage Film | Period stories, memory | period motion-picture look, gentle film grain, authentic period production design |
| `dreamreal` | Dream Realism | Surreal but coherent | photographic realism with one impossible element, spatially coherent |
| `foundfootage` | Found Footage | Raw, subjective terror | consumer-camera found footage, imperfect handheld framing, available light, sensor noise |
| `commercial` | Premium Commercial | Products and materials | premium commercial photography, precise material detail, controlled highlights |
| `western` | Modern Western | Landscape, dust, grit | modern western, weathered materials, wide natural landscapes |

## Colour (palette through light and set first, grade second)

Key: `colour`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `neutral` | Natural Neutral | Everyday realism; the realism default | neutral true-to-life colour, accurate skin tones, no colour grading |
| `cold` | Cold Blue | Mystery, isolation, horror | cool blue-grey palette from the light sources, controlled saturation, neutral skin |
| `tealorange` | Teal and Orange | Action, subject against background | warm practical light on skin against cool ambient shadows, restrained, natural skin |
| `amber` | Warm Amber | Hope, nostalgia, romance | warm golden light, rich natural midtones, soft highlights |
| `desat` | Desaturated | Bleak drama, dystopia | muted low-saturation palette, grey midtones, firm blacks |
| `mono` | Black and White | Noir, graphic contrast | black-and-white photograph, rich blacks, luminous grey highlights |
| `sickly` | Sickly Green | Institutions, decay | faint green-cyan cast from fluorescent tubes, muted skin |
| `pastel` | Soft Pastel | Dreams, gentle fantasy | airy pastel set colours: peach, lavender, muted mint |
| `crimson` | Crimson Accent | Danger, obsession | one crimson accent against charcoal neutrals |
| `steelcyan` | Steel and Cyan | High-tech tension | steel-blue palette with small cyan practical lights |
| `earth` | Earthy | Rural life, history | ochre, olive and warm stone tones |
| `highcon` | High Contrast | Silhouette, graphic drama | deep blacks, firm contrast, few bright highlights |
| `bleach` | Bleach Bypass | Gritty action, war | low saturation with strong contrast, silvery highlights |
| `sunwashed` | Sun-Washed | Summer memory, coming of age | sun-washed highlights, slightly lifted blacks, warm pastel midtones |

## Shot size and composition

Key: `size`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `xwide` | Extreme Wide | Geography and scale | extreme wide establishing frame, the environment dominates |
| `wide` | Wide | Whole action in its space | wide shot, subject and surroundings clearly visible |
| `full` | Full Body | Gesture, body language | full-body framing, head to feet in frame |
| `cowboy` | Cowboy | Stance, readiness | medium-full framing from mid-thigh up |
| `medium` | Medium | Behaviour and exchange | medium shot from the waist up |
| `mcu` | Medium Close-Up | Conversation, emotion with context | medium close-up, face and shoulders |
| `cu` | Close-Up | Emotion, reaction, decision | close-up on the face |
| `ecu` | Extreme Close-Up | Eyes, a clue, fine detail | extreme close-up on the one detail that carries the story |
| `pov` | POV | Inside a character | point of view from the character's eye line |
| `ots` | Over the Shoulder | Confrontation, dialogue | over-the-shoulder, a soft foreground shoulder, the other person sharp |
| `two` | Two-Shot | A relationship or conflict | two-shot, both people readable |
| `insert` | Insert | Plant or pay off an object | insert of one meaningful object |
| `silhouette` | Silhouette | Mystery, threat | subject as a readable silhouette against a brighter background |
| `negspace` | Negative Space | Isolation, anticipation | subject small and off-centre, deliberate empty space |
| `symmetry` | Centred Symmetry | Control, ritual, unease | precisely centred symmetrical frame, clean leading lines |
| `macro` | Macro | Material detail | macro detail, precise separation from the background |

## Camera angle

Key: `angle`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `eye` | Eye Level | Neutral, personal | eye-level camera |
| `low` | Low Angle | Power, menace | low angle looking up, the subject imposing |
| `high` | High Angle | Fragility, isolation | high angle looking down, the subject small |
| `dutch` | Dutch Tilt | Instability; use once | slight Dutch tilt |
| `overhead` | Overhead | Pattern, layout | top-down overhead view |
| `ground` | Ground Level | Footsteps, danger, scale | camera near the floor |
| `worm` | Worm's Eye | Towering scale | near-vertical view up from the ground |
| `profile` | Profile | Silhouette, facial line | clean side profile |
| `threequarter` | Three-Quarter | Natural portrait volume | three-quarter view |
| `rear` | Rear | Following, anonymity | from behind the subject, toward where they are going |

## Camera movement (one per shot)

Key: `move`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `static` | Locked-Off | Dread, dialogue, precision | locked-off static camera |
| `pushin` | Slow Push-In | Realisation, pressure | slow push-in toward the subject |
| `pullout` | Pull-Back | Reveal, isolation | slow pull-back revealing the surroundings |
| `track` | Tracking Follow | Travel with someone | camera tracks with the subject at a constant distance |
| `lateral` | Lateral Track | Reveal space with parallax | sideways tracking with foreground parallax |
| `panleft` | Pan Left | Reveal or follow left | steady pan to the left |
| `panright` | Pan Right | Reveal or follow right | steady pan to the right |
| `tiltup` | Tilt Up | Height, a looming threat | slow tilt up |
| `tiltdown` | Tilt Down | Reveal below | slow tilt down |
| `orbit` | Orbit | Hero moment, turning point | camera arcs around the subject, keeping orientation |
| `craneup` | Crane Up | Open out, end a sequence | camera rises to reveal the wider world |
| `cranedown` | Crane Down | Enter the scene | camera descends toward the subject |
| `handheld` | Handheld | Panic, immediacy, realism | handheld camera with slight natural shake |
| `float` | Floating Follow | Dreamlike glide | smooth stabilised floating camera |
| `rack` | Rack Focus | Redirect attention | static camera, focus shifts from foreground to background |
| `zoom` | Slow Zoom | Uneasy attention | slow optical zoom in, camera position fixed |
| `aerial` | Aerial Drift | Landscape, scope | slow aerial drift over the landscape |
| `povwalk` | POV Walk | Immersion, discovery | first-person forward walk with gentle step motion |
| `whip` | Whip Pan | Energy, a hidden cut | fast whip pan |
| `dollyzoom` | Dolly Zoom | Vertigo, shock | dolly zoom: background stretches while the subject stays the same size |

## Light (always a named source)

Key: `light`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `motivated` | Scene-Motivated | Use the light already in the scene | light motivated by the sources in the scene, consistent direction |
| `daylight` | Daylight | Exterior realism | natural daylight with consistent shadow direction |
| `hardsun` | Hard Sun | Real, graphic, summer | hard direct sun from one side, sharp shadows, face in bounced open shade |
| `window` | Soft Window | Intimacy, faces | soft directional window light with gentle falloff |
| `golden` | Golden Hour | Hope, nostalgia | low golden-hour sun, long shadows |
| `bluehour` | Blue Hour | Quiet melancholy | dim blue-hour ambient light, last glow in the sky |
| `fluorescent` | Cold Fluorescent | Hospital, institution | cold overhead fluorescent tubes, clinical falloff |
| `lowkey` | Low-Key | Threat, mystery | low-key light, small pools of motivated light, deep shadow |
| `moon` | Moonlight | Night suspense | soft moonlight, subdued exposure |
| `neon` | Neon Practicals | City noir, sci-fi | light from neon signs and fixtures in the scene |
| `candle` | Candlelight | Period, dread | flickering warm candlelight, fast falloff |
| `overcast` | Overcast | Bleak outdoor realism | diffused overcast light, soft shadows |
| `rim` | Rim Backlight | Silhouette, separation | motivated backlight tracing the subject's edges |
| `highkey` | High-Key | Clean, commercial, sterile | bright high-key light, soft controlled shadows |
| `hardside` | Hard Side Light | Stark conflict | hard side light carving the face |
| `flashlight` | Flashlight | Exploration, dread | a single handheld flashlight as the key light |
| `screen` | Screen Glow | Isolation, night, secrets | a phone or monitor screen as the only light, lighting the nearest face or surface from below |
| `fire` | Firelight | Danger, survival | warm flickering firelight on the nearest surfaces |
| `underwater` | Underwater | Surreal, submerged | filtered light from above with moving caustic patterns |

## Atmosphere and texture (one per shot, physically motivated)

Key: `atmo`

| id | Name | Use it for | In a still | In a video |
|---|---|---|---|---|
| `clean` | None Added | Keep the scene's own conditions | - | - |
| `haze` | Light Haze | Depth without hiding anything | barely visible haze separating the layers | the existing haze drifts slowly |
| `fog` | Ground Fog | Mystery, low visibility | thin fog lying low on the ground | the low fog creeps slowly |
| `densefog` | Dense Fog | Isolation, uncertainty | dense layered fog hiding the distance | the fog keeps its density |
| `rain` | Rain | Noir, tension, sadness | visible light rain, wet reflective surfaces | the rain keeps falling at the same rate |
| `downpour` | Heavy Rain | Emergency, action | visible heavy rain, soaked surfaces | heavy rain keeps striking clothes and ground |
| `dust` | Dust in the Light | Abandoned interiors | dust suspended in the light beams | dust drifts slowly through the beams |
| `flicker` | Light Flicker | Electrical unease | uneven light from a failing fixture at one instant | the existing practical light flickers occasionally |
| `smoke` | Thin Smoke | Industrial threat, aftermath | visible wisps of smoke | wisps of smoke move naturally |
| `wind` | Wind | Life in a still frame | hair and light fabric caught mid-gust | a gentle breeze moves hair and light fabric |
| `snow` | Light Snow | Stillness, cold | snowflakes frozen mid-air | light snow drifts down and settles |
| `mist` | Morning Mist | Poetic outdoor depth | fine mist receding into the distance | the mist thins slowly |
| `sparks` | Sparks | Impact, machinery | sparks frozen at the point of contact | brief sparks burst from the point of contact |
| `embers` | Embers | Fire, aftermath | glowing embers near the heat source | embers drift up from the heat source |
| `grain` | Film Grain | Texture, period, realism | fine film grain | fine film grain |
| `noise` | Sensor Noise | Night realism, found footage | visible sensor noise in the shadows | sensor noise in the dark areas |

## Lens

Key: `lens`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `auto` | Director's Choice | Match the shot size | - |
| `18` | 18 mm Ultra Wide | Architecture, big spaces, unease | 18 mm ultra-wide lens, strong perspective |
| `24` | 24 mm Wide | Environment and character | 24 mm wide lens |
| `28` | 28 mm Environmental | Streets, interiors, handheld | 28 mm lens |
| `35` | 35 mm Storytelling | Balanced cinema perspective | 35 mm lens |
| `50` | 50 mm Natural | Neutral, intimate | 50 mm lens, natural perspective |
| `65` | 65 mm Portrait | Flattering isolation | 65 mm lens, gentle compression |
| `85` | 85 mm Portrait | Faces, background separation | 85 mm portrait lens, soft background |
| `macro100` | 100 mm Macro | Textures, clues, products | 100 mm macro lens |
| `anamorphic` | Anamorphic | Widescreen drama | anamorphic lens, oval out-of-focus highlights, gentle horizontal flares |
| `vintage` | Vintage Glass | Softness, memory | vintage lens, slight softness around highlights |
| `deep` | Deep Focus | Keep every layer readable | deep focus, foreground and background sharp |

## Pace (video only)

Key: `pace`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `measured` | Measured | Natural progression | measured, human-scale rhythm |
| `slowburn` | Slow-Burn | Hold tension and silence | slow-building, restrained timing, long held pauses |
| `urgent` | Urgent | Action, escape | urgent but physically plausible movement |
| `dream` | Dreamlike | Eerie time | slightly slowed, unhurried |
| `tender` | Tender | Intimacy | quiet, tender, unhurried |
| `energetic` | Energetic | Commercial, social | confident energetic tempo, one clear main action |
| `observational` | Observational | Documentary | unforced, observed |
| `ritual` | Ritual | Eerie repetition | deliberate, ceremonial |

## Intent (what the shot must deliver)

Key: `intent`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `establish` | Establish | Introduce a place or mood | keep the space and where things are clearly readable |
| `reveal` | Reveal | Expose a clue or change | guide the eye to the reveal at the end |
| `emotion` | Emotion | Expression first | hold on the face; small believable reactions |
| `tension` | Suspense | Build expectation | stretch the anticipation without changing the outcome |
| `action` | Action | Physical motion | keep cause and effect of every movement readable |
| `dialogue` | Dialogue | A clear exchange | keep eyelines and positions consistent |
| `discovery` | Discovery | Follow the observer | reveal the space in the order the character notices it |
| `product` | Product Hero | Show the product | show material, silhouette and the one useful detail |
| `transition` | Transition | Bridge to the next shot | end on a movement or shape the next shot can continue |
| `climax` | Climax | The decisive moment | give the decisive action the frame |

## Transition into the next shot

Key: `transition`

| id | Name | Use it for | Prompt words |
|---|---|---|---|
| `cut` | Straight Cut | Default | cut |
| `cutmove` | Cut on Movement | Hide the cut inside action | cut on movement |
| `match` | Match Cut | Link two shapes or actions | match cut on shape or action |
| `handoff` | Hand-off Frame | Same action continues | the last frame becomes the next shot's first frame |
| `whip` | Whip Pan | Energy, a hidden join | whip pan into the next shot |
| `smash` | Smash Cut | Shock, comic contrast | smash cut |
| `jcut` | J-Cut | Sound leads the picture | next shot's sound starts early |
| `lcut` | L-Cut | Sound lingers | this shot's sound carries over |
| `dissolve` | Dissolve | Time passing, memory | dissolve |
| `black` | Cut to Black | End, cliffhanger | cut to black |

## Quick Director presets

Starting points per genre (`studio.py direct --genre <id>`). Review every shot afterwards.

| genre | style | colour | size | angle | move | light | atmo | lens | pace | intent |
|---|---|---|---|---|---|---|---|---|---|---|
| `horror` Horror | photoreal | cold | wide | eye | pushin | lowkey | haze | 35 | slowburn | tension |
| `thriller` Thriller | noir | desat | medium | eye | track | lowkey | clean | 35 | urgent | tension |
| `mystery` Mystery | noir | cold | insert | eye | rack | lowkey | haze | 50 | slowburn | reveal |
| `drama` Drama | indie | neutral | mcu | eye | static | window | clean | 50 | tender | emotion |
| `romance` Romance | photoreal | amber | medium | eye | pushin | golden | clean | 50 | tender | emotion |
| `action` Action | blockbuster | tealorange | wide | low | track | daylight | clean | 35 | urgent | action |
| `scifi` Sci-Fi | scifi | steelcyan | wide | eye | pullout | neon | haze | 24 | measured | establish |
| `fantasy` Fantasy | darkfantasy | earth | wide | low | craneup | golden | mist | 24 | dream | reveal |
| `dream` Dream / Surreal | dreamreal | pastel | wide | eye | float | highkey | haze | 35 | dream | discovery |
| `documentary` Documentary | documentary | neutral | medium | eye | handheld | daylight | clean | 35 | observational | establish |
| `product` Product / Ad | commercial | neutral | cu | threequarter | orbit | highkey | clean | 85 | energetic | product |
| `western` Western | western | earth | wide | low | lateral | golden | dust | 35 | measured | establish |
| `anime` Anime | anime | pastel | medium | eye | track | daylight | clean | 35 | energetic | action |
| `invasion` Sci-Fi Horror / Invasion | photoreal | cold | wide | eye | handheld | lowkey | noise | 35 | slowburn | tension |

## Scene starters

One-line scenes for a quick demo, or when the user has no idea yet (`studio.py recipes`).

| Genre | Title | Scene |
|---|---|---|
| horror | Doorway | A nervous woman stands before a half-open metal door; a shadow shifts behind the gap. |
| horror | Silent Corridor | A lone figure walks a deserted hospital corridor while one fluorescent tube flickers far ahead. |
| horror | Reflection | A man looks into a bathroom mirror and sees a shape standing behind him that is not in the room. |
| horror | Forest Presence | A lost hiker hears a branch snap and turns toward a dark clearing. |
| mystery | The Hidden Note | A detective finds a handwritten note under a loose floorboard in an empty apartment. |
| mystery | Empty Platform | A woman waits alone on a night platform; an unclaimed suitcase sits beside her bench. |
| mystery | The Photograph | Someone studies an old family photo and finds their own face in the background crowd. |
| thriller | Stairwell | A man runs down an emergency stairwell as heavy footsteps echo above him. |
| thriller | Rooftop Standoff | Two people face each other on a rain-soaked rooftop at night. |
| thriller | The Passenger | A commuter notices the same silent stranger following her through several train cars. |
| drama | Kitchen Table | A mother and daughter sit in silence at a kitchen table after an argument. |
| drama | Outside Room 12 | A man hesitates outside a hospital room, gripping a folded letter. |
| drama | Rain Window | An old woman watches city rain from her window, a photograph in her lap. |
| romance | Platform Reunion | Two childhood friends recognise each other across a station platform at sunset. |
| romance | Rooftop Confession | A couple stands close under string lights above a night city. |
| action | Market Chase | A courier sprints through a crowded market while two pursuers push through the stalls behind. |
| action | Bridge Rescue | A firefighter edges along a storm-damaged bridge toward a stranded driver. |
| action | Warehouse | Two fighters face off in an empty warehouse, dust drifting through shafts of light. |
| scifi | Ship Awakens | A pilot enters a dormant cockpit as the instruments flicker on one by one. |
| scifi | City Balcony | A traveller stands on a balcony above a dense future city at night. |
| scifi | The Memory | A scientist studies a glowing holographic memory in a dark lab. |
| invasion | The Knock | During an invasion, a sister hides with her brother; their father's voice asks them to open the door. |
| invasion | Last Broadcast | A radio host alone in her studio reads evacuation orders as the ships descend over the city. |
| invasion | Wave | Stuck in gridlock as ships descend, a child waves at one, and it stops. |
| fantasy | Forest Portal | A traveller finds a glowing doorway between ancient trees in the mist. |
| fantasy | Mountain Citadel | A lone rider reaches the gates of a vast mountain fortress under storm clouds. |
| dream | Gravity Shift | A woman steps into a room where the furniture hangs still in mid-air. |
| dream | Endless Hallway | Someone walks a white hallway that stretches beyond sight. |
| documentary | City Morning | A street vendor sets up a food stall as the city wakes. |
| documentary | Craftsmanship | A watchmaker adjusts a tiny gear at a cluttered bench. |
| product | Perfume Reveal | A glass perfume bottle on polished stone; reflections slide across its surface. |
| product | Sneaker Detail | A running shoe on a plain plinth, its textures catching a hard side light. |
| western | Arrival | A lone rider approaches a weathered frontier town through sunlit dust. |
| anime | Rainy Farewell | A girl under an umbrella waits at a railway crossing in the rain. |

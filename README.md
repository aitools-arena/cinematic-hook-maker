# The Cinematic Hook Maker

The first three seconds decide whether anyone watches the rest. The Cinematic Hook Maker designs and renders that opening like a film crew would: the story, the line that makes people stay, the first frame that stops the scroll, the camera, light and motion, and the on-screen text that works with the sound off. It renders with Kling 4.0 and GPT Image 2.5 through your Artlist account. When you need more than a hook, the same studio makes the whole film.

## What it does

**Hooks**
- Guided brief: just say "make a hook for my video about X" and it walks you through twelve short steps, one question at a time with clickable options (format by aspect ratio, video type, what the video delivers, language, audience gender and age, who is on screen, the AI model (female or male, with looks for your market), look, hook direction, on-screen text, sound, length and render plan). Each choice shapes the next options, "default" skips a step, "back" changes the last one, your usual answers come first next time, the language you choose sets the target market, and the AI model can be any look (Japanese, Korean, American, Latina, European and more) from a dropdown
- Knows seven platforms (TikTok, Reels, Shorts, YouTube, Facebook, LinkedIn, X), their ratios, hook windows and safe zones
- Knows twelve video types and what a hook must do for each
- Writes three different concepts from twelve story types, one hundred numbered opening lines and sixteen visual formats, and scores each for stopping power, clarity and payoff
- Every spoken line comes from the library: only its slots are filled, or it is translated faithfully. The helper script refuses a concept whose line was made up
- Designs a real, good-looking first frame that also works as the cover
- Renders with action from the very first frame and an ending that cuts straight into your video
- Burns exact on-screen text inside the safe zone, crops for 4:5, makes text-only A/B variants, swaps in a voice-over and joins the hook to your video
- Hands you a hook pack with every concept, frame, line, text, score and prompt

**Cinematic studio**
- Casting: models and presenters for your product, from your real product photos, with casting photos and character sheets that keep the face consistent
- A full photographic realism recipe for stills: attractive people in real, unretouched photographs
- A film-language library: shot size, angle, camera move, lens, light, colour, atmosphere, pace and transitions, plus genre presets that lock one look across every shot
- Multi-shot hooks, short films, micro-drama episodes, trailers, music videos and brand films: story beats, shot cards, prompt packs, storyboard board and pitch board
- One continuous take up to thirty seconds with keyframes
- VFX on your own footage: swap the person, outfit, product or background, add an effect, copy a camera move
- Dialogue in several languages, voice-over, music and sound effects
- Review and fix catalogue, cost report, edit list, rough cut and an episode handoff so a series stays consistent
- Remembers your platform, language, look and characters for next time

## Install

The skill needs the **Artlist connector** for every image and video. Connect it first:
Claude Settings → Connectors → Add custom connector → name `Artlist`, URL `https://mcp.artlist.io/mcp` → Connect and sign in.

### Claude Code (plugin)

In Claude Code, run:

```
/plugin marketplace add aitools-arena/cinematic-hook-maker
/plugin install cinematic-hook-maker@cinematic-hook-maker
```

Update later with `/plugin marketplace update cinematic-hook-maker`.

### Claude Code (manual)

```bash
git clone https://github.com/aitools-arena/cinematic-hook-maker.git
cp -R cinematic-hook-maker/plugins/cinematic-hook-maker/skills/cinematic-hook-maker ~/.claude/skills/
```

### Claude desktop or claude.ai

1. Download `cinematic-hook-maker.skill` from the [latest release](https://github.com/aitools-arena/cinematic-hook-maker/releases/latest).
2. Settings → Capabilities → turn on code execution, then under Skills choose **Upload skill** and pick the file.

### Optional tools

Python 3 runs the helper scripts. `ffmpeg` and a Chrome-family browser are needed for burned-in text, crops and joining the hook to your video (`brew install ffmpeg` on macOS).

## Try it

- "Make a hook for my TikTok tutorial: how I made a sci-fi short with AI in one afternoon."
- "Three hook ideas for an Instagram ad for my handmade candles. Here's a photo of the candle."
- "Create a model for my fashion brand: Japanese, female, 20, wearing these clothes."
- "Swap the person in this product video for my model and keep the camera move."
- "A 15-second cold open for episode one of my micro-drama, three shots."

Generations use your own Artlist plan. Claude quotes the cost of each step before it renders anything.

## License

[CC BY-NC 4.0](LICENSE): free to use and adapt with credit, not for commercial resale.

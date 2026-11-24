# Deadhead Dale — daily Reel studio

Instagram: @deadhead.dale (Metricool brand/blogId 8301887). Owner: Bill. Post 2 Reels/day at 10:00 AM and 6:00 PM America/Chicago (since 2026-11-24).

## Format
- Deadpan absurd comedy, low-poly 3D, like @semigenius. Star: Dale (trucker, red DALE cap, mustache, plaid, belly).
- Mix trucking stories and totally random ones (Bill loves the geese / hardware-store episode). Lots of swearing is wanted (fuck, goddamn, shit, bitch, asshole).
- Script: 15–25 short sentences, escalating absurdity, last line loops into the first line.
- Swearing (Bill, 2026-11-24): more swears per script, but each must fit naturally where it sits (insults aimed at someone, "for shit", "pissed the fuck off") — never tacked on.
- Randomness (Bill, 2026-11-24): scripts must be MUCH more random — non-sequitur jumps (talking animals, objects with lives, surreal swerves), not a linear cause-and-effect plot. Aim 35–50 s after processing.
- Voice: ElevenLabs "Monotone Mike" voice_id aWSwMfJOK8iYZivczje6, model eleven_v4, prompt starts "[deadpan, flat, matter-of-fact]", 1 take.
- Caption: hook line + share prompt ("Tag/Send this to someone who...") + ~10 hashtags incl #deadheaddale. Mark isAiGenerated true.

## Workflow
- Ideas: every day 5 new full scripts are appended to IDEAS.md (dated batch, ids like 2026-11-23-A) and sent to Bill. Bill replies with the ones he wants (he may edit lines). Copy picked scripts into QUEUE.md with status `approved`, in his order.
- Production: the nightly run fills the next two free slots (10:00 / 18:00 CT) with the first `approved` items in QUEUE.md, in order. Never invent and post a script Bill didn't pick. If the queue is empty, schedule nothing.
- Episodes 1 and 2 are skipped; studio/ep1.py and ep2.py stay only as code examples.

## Pipeline (all paths absolute under /home/claude/deadhead-dale)
1. `pip install --break-system-packages bpy` (Blender as a module; Workbench renderer, ~1 s/frame on 2 CPUs).
2. Voice: generate via ElevenLabs connector, download content_url mp3 with curl, then
   `ffmpeg -i raw.mp3 -af "silenceremove=start_periods=1:start_threshold=-40dB,atempo=1.15,silenceremove=stop_periods=-1:stop_duration=0.28:stop_threshold=-40dB,apad=pad_dur=0.4" -ar 44100 -ac 1 voices/epN.wav`
3. Write `studio/epN.py` modelled on ep1/ep2/ep3.py: `S` (sentences exactly as voiced), `SHOTS` [(first sentence idx, name)], `SFX` {shot: [(fraction, libname, gain)]}, `build(name, N)`. Kit helpers in studio/kit.py (person, goose, semi, sets, props, camera, expr/talk/walk/arms).
4. Preview: `python3 preview.py epN k 48 0.6` for every shot, contact sheet with sheet.py; fix framing.
5. `python3 plan.py epN voices/epN.wav epN epN_plan.json`; render `./runall.sh epN epN_plan.json /home/claude/deadhead-dale/studio/epN` (2 workers). Keep the turn alive while rendering (background jobs die after the reply ends).
6. Compose: `python3 -c "import comp, epN; comp.compose('epN_plan.json','epN','../voices/epN.wav','../videos/epNNN_slug.mp4', epN.SFX)"`
7. Commit + push video to main. Public URL: https://raw.githubusercontent.com/legojacobs7-tech/deadhead-dale/main/videos/<file>.mp4
8. Schedule with Metricool createScheduledPost (instagram REEL, media=[raw URL], next 10:00 America/Chicago).
9. Log the episode in EPISODES.md (number, title, script gist, post time) so jokes don't repeat.

SFX library (sfx/*.wav): honk, flock, crash, cha, ding, buzz, whoosh, chomp, ring, burp, horn, siren, party, grind, picfall, sob.

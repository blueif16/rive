# keeper

**Fit:**

| question | score | why |
|---|---|---|
| One bold subject per beat, readable as a silhouette | 2 | tower, keeper in profile, lens, boat, buoy, whale, moon: every beat is one outline |
| Natural radial / concentric motifs | 2 | Fresnel lens rings, the beam wedge, sound arcs, ripples, moon halo, firework burst, dawn sun |
| Register warm, handmade, tender or wistful | 2 | a last night, a light handed over, a walk down a hill |
| Emotion by staging and rhythm, not facial acting | 2 | the keeper is a silhouette from first frame to last; the story is told by what lights up and when |
| Light and material as flat shapes and dot ramps | 2 | beam = knockout wedge + yellow dot ramp; sea = blue solid + paper hatching; no reflections anywhere |
| On-screen text limited to a title or signature | 2 | one word, "keeper", hand-lettered at the end |
| **Sum** | **12** | proceed, no fit adjustments |

**Format:** 720×720, 20 s, time-based, 120 BPM grid (0.25 s / 0.5 s units), Canvas 2D — one self-contained `index.html`, no libraries, no assets
**Defaults assumed:** none; all inputs were given. Two deliberate omissions, both from the fit table: the sea reflects nothing (a lit thing answers with its own light, never with a mirror image), and the keeper never has a face.

## The idea

A keeper climbs a tower and lights a lamp for the last time. The lamp is a small yellow disc pinned to the centre of the sheet, and the beam is a wedge of paper knocked out of the blue night, printed over in yellow, turning about that disc. Everything the beam touches through the night prints its own small light on exactly the same spot: a masthead lantern, a bell buoy, a cottage window, a whale's eye, a far lighthouse, portholes, a jellyfish, a firefly, a headlamp, a campfire, an owl's eye, an anglerfish lure, a firework, and finally the moon. The night is a montage of sheets, hard-cut on the beat, each sheet hand-registered a little differently, each with the same disc at the same place. At dawn the blue night plate starves away from the horizon up, the keeper's flame starves with it, and on the beat every plate snaps to perfect registration: the machine has the light now, a flawless ring, the only perfect circle in the film. The keeper walks down the hill on twos while the exact beam turns above. The word "keeper" is lettered by hand under the lamp, the pink plate lagging two frames behind, and dissolves to dots. The lamp stays.

## The spine

- **Motif:** the lamp — a disc 36 px across (5 % of frame width). Lit: yellow at 100 % with the pink plate offset +2 px so a pink crescent shows on its right edge (the fringe). Unlit: a 2 px indigo ring with paper inside. Out of it come the rings (ripples, lens rings, sound arcs, halos) and the beam (a wedge about the anchor, or a band crossing a distant sheet). It means the light the keeper tends, and every answer in the night is the same disc.
- **Anchor:** frame centre, (360, 360). Never drifts during Acts I–V. The only camera move in the piece is the dive at 2.0–2.35 s, and it is about the anchor. Every scene lands something meaningful there: the unlit lens, the hatch at the top of the stair, the flame, the masthead lantern, the eye, the lure, the moon, the machine's ring, the lamp above the word.
- **House inks:** indigo `#2E3192` = line (outlines, silhouettes, the unlit ring, lettering) · blue `#0078BF` = base (night sky, sea, deep water) · yellow `#FFE800` = overprint and accent (beam, lamp, every answer, dawn sun) · fluorescent pink `#FF48B0` = accent (the fringe, dawn, flame heart, the lettering's misregistered copy). Planned overprints: pink × blue → violet (hill, dusk glass, cloud, shadow side of things); yellow × pink → orange-red (flame heart, sun, fire); yellow × blue → green (only as the planned fringe where beam-edge dots interleave with night dots, and as sea shimmer near the sun at dawn). Paper `#F2EDE3`, static fibre grain. Misregistration budget 1–3 px per ink, a fixed vector per scene, written in every entry; the pink plate is always +2 px right of the yellow on the lamp so the fringe is on the right; from 15.0 to 17.0 every vector is (0, 0) — that is the machine.
- **Never-drifts rule:** the disc's centre on its own plate (yellow when lit, indigo ring when unlit) is (360, 360) before misregistration in every scene of every act. The builder asserts this in code at every act boundary, not by looking.

## Timeline

Every cut on the 0.25 s grid. Act boundaries: **I 0.0 · II 4.0 · III 7.0 · IV 13.0 · V 17.0 · end 20.0.** Breathe beats marked ◦.

| time (s) | act | what happens |
|---|---|---|
| 0.0–0.5 | I The climb | Blank cream paper. The unlit lens: a 2 px indigo ring, 36 px, at the anchor. Nothing else. |
| 0.5–1.0 | I | Plate-by-plate reveal of scene 1: yellow at 0.5, pink at 0.625, blue at 0.75, indigo line at 0.875. By 1.0 the tower stands on its hill, lamp room at the anchor, sea to the right, cottage at lower left. |
| 1.0–2.0 | I | Hold. The keeper (a 28 px indigo silhouette) walks from the cottage door to the tower door on twos. The cottage window goes dark at 1.5. Wave hatching cycles. |
| 2.0–2.35 | I | **Dive** through the lamp room: a disc opens on the anchor, the section view scales 0.55→1.0 as the mask grows past the corners. |
| 2.35–4.0 | I | Scene 2, the stair in section. The keeper climbs four flights with a hand lantern, 8 fps, from the bottom edge to the landing beside the unlit lens at the anchor. Arrives at 4.0. |
| 4.0–4.5 | II The lighting | **Hard cut** (new registration) to scene 3, the lamp room: the Fresnel rings around the anchor, keeper's profile at left. The keeper raises the hand lantern to the wick in two poses. |
| 4.5–5.1 | II | **Bloom**: the flame disc fills yellow, then the five lens rings light one by one outward, 40 ms stagger. |
| 5.0–5.5 | II | The beam appears: a 24° wedge from the anchor pointing right, and begins to turn clockwise. |
| 5.5–7.0 | II | **Hard cut** to scene 4, the tower from outside, lamp lit. The beam sweeps the sky from 200° to 340° over 1.5 s. A ripple leaves the anchor at 6.0 and at 6.5. At 7.0 the beam points at the sea. |
| 7.0–7.5 | III The sea answers | **Hard cut.** Scene 5, fishing boat: the beam band crosses, the masthead lantern answers at the anchor. |
| 7.5–8.0 | III | **Hard cut.** Scene 6, bell buoy: band crosses, lamp answers, sound arcs. |
| 8.0–8.5 | III ◦ | **Breathe B1.** Blank paper, one ripple from the anchor. |
| 8.5–9.0 | III | **Iris** open on the anchor: scene 8, cottage on the headland: band, window lamp answers. |
| 9.0–9.5 | III | **Hard cut.** Scene 9, whale: band through the water, the eye answers. |
| 9.5–10.0 | III | **Hard cut.** Scene 10, far lighthouse across the strait: band, its flash answers. |
| 10.0–10.5 | III ◦ | **Breathe B2.** Blank paper, one ripple. |
| 10.5–11.0 | III | **Iris** open: scene 11, steamer: band, bridge lamp answers, portholes follow. |
| 11.0–11.25 | III | **Hard cut.** Scene 12, jellyfish: bell glows. |
| 11.25–11.5 | III | **Hard cut.** Scene 13, heron in the reeds: a firefly answers. |
| 11.5–11.75 | III | **Hard cut.** Scene 14, night train head-on: headlamp answers. |
| 11.75–12.0 | III | **Hard cut.** Scene 15, campfire on the beach: the flame flares. |
| 12.0–12.25 | III | **Hard cut.** Scene 16, owl on the dune post: the eye answers. |
| 12.25–12.5 | III | **Hard cut.** Scene 17, anglerfish in the deep: the lure answers. |
| 12.5–12.75 | III | **Hard cut.** Scene 18, fireworks from the far town: a burst at the anchor. |
| 12.75–13.0 | III | **Hard cut.** Scene 19, the moon breaks cloud: the moon and its halo answer. The last and largest answer. |
| 13.0–13.5 | IV Dawn ◦ | **Breathe B3.** Blank paper, one last ripple with the pink fringe. |
| 13.5–14.5 | IV | **Iris** open on the anchor: scene 20, the tower from outside. The blue night plate **halftone-dissolves** from the horizon upward; a pink grain glow climbs the sky. |
| 14.0–15.5 | IV | The sun (90 px, yellow × pink) rises at the right horizon, clipped by the horizon line. |
| 14.5–15.0 | IV | The keeper's flame **halftone-dissolves**; the pink fringe goes with it; the indigo ring stays. |
| 15.0 | IV | **Registration drift as a cut**: every plate snaps to (0, 0). The machine's ring is on: a perfect 2 px indigo circle, paper inside. Scene 21. |
| 15.0–17.0 | IV | The machine's beam, an 8° wedge with straight edges, sweeps 200°→340° every 2 s exactly. The keeper walks down the hill path from the tower door to the lower-left corner, 8 fps, shrinking 40→32 px. |
| 17.0–17.5 | V Signature | **Hard cut** to cream paper. The lamp disc at the anchor, lit, pink fringe back. It sends one ripple. |
| 17.5–19.0 | V | **Stroke reveal**: "keeper" lettered below the lamp, one glyph per 0.25 s, indigo, pink copy two frames behind. |
| 19.0–19.5 | V | Hold. |
| 19.5–20.0 | V | **Halftone dissolve** of the lettering to shrinking dots. The lamp stays lit to the last frame. |

Beam period everywhere the tower is on screen: one sweep 200°→340° in 1.5 s then 0.5 s dark, period 2 s = 4 beats. In the montage the beam arrives from off-sheet as a band crossing left to right; the answer blooms at the anchor as the band's centre crosses x = 360.

## Scene library (in timeline order)

Two entry sizes, as the skill directs. **Full entries** (the fixed eight-field shape) for scenes 1–4, held 0.5 s or longer or dived through, and for scenes 20–22, the dawn, the machine and the last scene. **Compact entries** (five lines, at most 80 words, no pixel coordinates) for every montage sheet, scenes 5–19 and the surplus 23–25. Compact entries rely on these defaults, which the builder applies unless the entry says otherwise:

- **"blue base"** alone = night sky in grain touch (66–74 %) above a sea printed solid at 85 % with voids and paper wave hatching; where the entry says water, the whole field is solid 88–90 % with voids and a slight height ramp. **"yellow accent"** alone = the beam band, the lamp disc and the answer ring. **"indigo line"** carries every named silhouette as a fill on a paper knockout with a 1 px trap of the base running under it, plus the strokes named; indigo lines overprint anything, indigo fills never sit on a blue or pink solid.
- **"→ violet"** = pink over blue with one ink at or below 60 %; "→ orange-red" = pink over yellow; "→ dark violet" = pink 50 % over blue 60 %.
- **Knockouts always present**, not repeated per entry: the lamp disc from whatever base it sits in; the beam band from every base it crosses while it passes; stars are paper dots 3–5 px, seeded.
- **Tone defaults**: sky grain, sea and water solid, silhouettes solid indigo, glows and halos as yellow dot ramps at 0° falling to 0 with distance, overprint fields as dots at each ink's angle (§Visual system). The motif rhyme in every montage sheet is the answer ring plus the radial element named in the silhouette (sound arcs, light shafts, the flash bar, the smokebox, the halo, the rays).
- **"Answer 90"** = the beam band crosses left to right for the sheet's first half, the disc blooms at the anchor as the band's centre passes it, and a yellow answer ring grows to 90 px by the sheet's end (0.5 s sheets). **"Answer 60"** = the same in a 0.25 s sheet, ring to 60 px. **"Answer burst"** = the bloom, then rays extend from the disc over 0.15 s in place of the ring, yellow first, pink 40 ms behind. Anything written after the Answer on a live line is part of the same bloom key, not a second element.
- **Misreg** = the misregistration vector per ink in px, ink(dx,dy), fixed for the sheet; blue is always the (0,0) reference.

Full entries use these terms too. "Beam" in a full entry means a knockout from every base plate it crosses with a yellow dot-size ramp printed inside (100 % at the source edge → 35 % at the far edge, 0° screen); its 12 px soft edges are dot ramps, so blue and yellow dots interleave into a planned green fringe.

### 1. The tower on the hill   t = 0.0–2.0 s, blank paper then plate-by-plate reveal at 0.5
- Silhouette: a tapered tower rising from a hill crest at y = 600 to the gallery at y = 392, 70 px wide at the base and 50 px at the gallery; lamp room 50 px square centred on the anchor; a shallow conical cap to y = 318. Hill: one convex curve from the left edge at y = 700 up to the crest under the tower and down to the sea at x = 470, y = 570. Sea: flat horizon at y = 560 from x = 470 to the right edge. Cottage: a 60 × 44 px box with a pitched roof at (110, 640) on the hill. Sky above the horizon. Nothing else: no rocks, no clouds, no gulls.
- Anchor: the lamp room. From 0.0 to 2.0 the lens is unlit: the 2 px indigo ring at (360, 360) with paper inside. It is on paper alone for the first beat, then the tower prints around it.
- Inks: indigo = line (tower outline, gallery rail, cottage, door, the unlit ring, keeper silhouette, horizon line) · blue = base (sky 72 % grain touch; sea 85 % solid with paper wave hatching) · pink = overprint (hill: pink 55 % over blue 60 % → violet; two tower bands pink 100 %) · yellow = accent (cottage window, 12 px, lit until 1.5). Misregistration: indigo (−1, +1) · blue (0, 0) · yellow (+1, +1) · pink (+3, +1).
- Knockouts: tower body and cap from the blue sky (the tower is paper, its shadow side blue 35 % dots at 15°); the lens ring's interior from blue; 22 stars from the sky, 3–5 px paper dots, seeded; the cottage from the violet hill; the cottage window from the cottage (paper, then yellow inside); wave hatching, 14 paper strokes 20–40 px long, from the sea.
- Tone: sky = grain touch 72 %; sea = solid 85 % with voids; tower shadow = blue dot ramp 15° pitch 5 px, 35 %→0 across the right half; hill = both inks at 60 % dots (pink 75°, blue 15°); roller band on (indigo, top 10 %, 4 %).
- Motif rhyme: the unlit ring itself; the gallery rail is a second, wider ring (58 px) around it; the cap's finial sits on the vertical through the anchor.
- Live element: (a) the keeper, an indigo silhouette 28 px tall, walks from the cottage door (140, 640) to the tower door (330, 600) from 1.0 to 2.0 on twos — 12 poses, two leg keys alternating, a 2 px bob; (b) the cottage window's yellow fill and its paper knockout close at 1.5 (a hold key, no fade); (c) wave hatching cycles: the 14 strokes shift +6 px right over 1.0 s and reset on the beat. Three live elements in a held scene, all in the lower third, none touching the anchor.
- Don't: no reflection of the tower in the sea; no moon (it is cloud-hidden until scene 19); no outline on the pink bands; the keeper never has a face or hands, only a coat and legs.

### 2. The stair in section   t = 2.0–4.0 s, dive in from the anchor (2.0–2.35)
- Silhouette: the tower cut open like a stencil: two tapered walls (paper, indigo edges) from the bottom edge, 220 px apart at the bottom and 180 px at the top, ending at the gallery floor y = 400; the lamp room above it with the unlit lens at the anchor. Inside, four straight flights zigzag: landings at y = 700 (right), 620 (left), 540 (right), 460 (left), gallery floor 400 (right). Each flight is 10 steps drawn as an indigo sawtooth line. The interior field is night blue.
- Anchor: the unlit lens, indigo ring at (360, 360), seen through the lamp room's glass, the destination of the climb. The dive mask opens exactly on it.
- Inks: indigo = line (walls, steps, keeper) · blue = base (interior 78 % grain touch, darker toward the bottom: 78 % at y = 720 → 55 % at y = 400 as a height-driven dot ramp) · pink = overprint (a violet wedge of shadow under each flight: pink 50 % over blue) · yellow = accent (the hand lantern, a 12 px disc, and a 40 px yellow dot-ramp pool around it, 0°, that travels with the keeper). Misregistration: indigo (+1, −1) · blue (0, 0) · yellow (+2, 0) · pink (+4, +1).
- Knockouts: the walls from blue (paper); the lamp room's glass from blue; the lens ring's interior; the lantern and its pool from blue (paper inside, yellow ramp printed in); the keeper's silhouette from blue with a 1 px blue trap (indigo fill on paper).
- Tone: interior = grain touch, height ramp; the lantern pool = dots pitch 5 px 0° from 100 % at the lantern to 0 at 40 px; step shadows = pink dots 75 % 50 %; walls = paper with indigo line only.
- Motif rhyme: the lantern pool is a small halo (a ring of dots); the four landings step inward toward the anchor like a staircase of rings seen edge-on; the lens ring at the top is the target.
- Live element: the keeper, 56 px tall indigo silhouette with the lantern held ahead at hip height, climbs from off the bottom edge at (500, 740) at 2.35 to the gallery landing at (410, 400) at 4.0: 8 fps, 13 poses, two leg keys alternating every pose, translation along the zigzag path at constant speed, facing flips at each landing (mirror the silhouette). The lantern pool and its knockout move with the figure (seeded to it). At 4.0 the figure holds beside the lens.
- Don't: no perspective, no spiral seen from below; the stair is a flat zigzag; no light thrown on the walls except the 40 px pool; the lens stays unlit until the cut.

### 3. The lamp room   t = 4.0–5.5 s, hard cut at 4.0 (new registration)
- Silhouette: the Fresnel lens as five concentric rings around the anchor at radii 40, 80, 120, 160, 200 px, each a 3 px indigo line with 2 % radius wobble; the flame at the anchor (the 36 px disc). Around the lens, the lamp room's glass panes: six indigo mullions radiating from the lens rim (radius 200) to the frame edges every 60°, a violet dusk field between them; a sea band across the bottom sixth. The keeper's profile silhouette on the left: head, shoulders and one raised arm, from x = 40 to 250, head top at y = 260, the hand and lantern reaching to (322, 360).
- Anchor: the flame at (360, 360). Unlit indigo ring at 4.0; the lamp disc yellow from 4.5 with the pink fringe on its right.
- Inks: indigo = line (rings, mullions, keeper, unlit ring) · blue = base (dusk field: 55 % grain; sea band 85 % solid) · pink = overprint (dusk field pink 45 % over blue → violet; flame heart pink 100 % on a 12 px inner disc → orange-red over yellow) · yellow = accent (flame disc, lens rings lit, the beam). Misregistration: indigo (−2, 0) · blue (0, 0) · yellow (0, +1) · pink (+2, +1).
- Knockouts: the whole lens disc (radius 200) from both blue and pink (glass is paper); the keeper from blue and pink with a 1 px trap; the beam wedge from blue and pink where it crosses the dusk field; the hand lantern (12 px) from the keeper's own indigo (paper, then yellow).
- Tone: dusk field = grain touch; sea band = solid with voids; the lit rings = yellow dot ramps 0°, 40 % at each ring's line falling to 0 midway to the next ring; the beam = yellow ramp inside the knockout; the flame = 100 % solid, no dots.
- Motif rhyme: the five lens rings are the motif's rings at their largest; the six mullions are the beam's spokes before the beam exists.
- Live element: in sequence — (a) 4.0–4.5 the keeper's arm lifts the lantern to the wick in two held poses (4.0 low, 4.25 at the wick); (b) 4.5–5.1 Bloom: the flame disc scales 0→1.08→1.0 (easeOutBack, 0.2 s), then ring 1..5 light with 40 ms stagger, each 0.2 s; (c) 5.0–5.5 the beam wedge (24° wide, 100 % at 30 px from the anchor → 35 % at the frame edge) appears at 0° and turns clockwise to 90° by 5.5 (180°/s, linear). Never more than two moving at once.
- Don't: no glow gradient on the glass; no face on the keeper — the profile is a coat collar, a cap brim and a chin line, nothing inside; the rings never light all at once.

### 4. The beam over the sea   t = 5.5–7.0 s, hard cut at 5.5 (new registration)
- Silhouette: scene 1's plates exactly (same paths, same seeds) with the lamp lit and the beam wedge added; the cottage window dark; the keeper absent.
- Anchor: the lit lamp — yellow disc 36 px at (360, 360), pink fringe right, the beam's pivot.
- Inks: indigo = line · blue = base (sky 72 % grain, sea 85 % solid) · pink = overprint (hill violet, tower bands, lamp fringe) · yellow = accent (lamp, beam). Misregistration: indigo (+1, +1) · blue (0, 0) · yellow (−1, +1) · pink (+1, +1).
- Knockouts: all of scene 1's, plus the lamp disc from blue, and the beam wedge (24°, from 30 px out to past the frame corners) from the blue sky and the blue sea and the violet hill wherever it points; the tower below the lamp is never crossed (the wedge is masked to angles 200°–340°, measured clockwise from +x, i.e. the sky half).
- Tone: as scene 1; beam = yellow ramp 100 % → 35 % along its length, edges 12 px dot ramps; where the beam lies over the sea the sea's paper hatching stays visible inside it.
- Motif rhyme: the beam wedge; ripple rings from the anchor at 6.0 and 6.5; the gallery ring around the lamp.
- Live element: (a) the beam sweeps from 200° at 5.5 to 340° at 7.0, linear, 93°/s (this scene shows exactly one sweep of the 2 s period, the dark half is cut away); (b) a Ripple leaves the anchor at 6.0 and at 6.5: blue 35 % 2 px stroke thinning 6→1 px, easeOutCubic 0.6 s, radius to 520 px, 3 % wobble, two tick arcs at the rim for 0.15 s.
- Don't: no beam reflection on the sea; the wedge never crosses the tower; the ripples are blue, not yellow, so the answer discs' yellow rings in Act III read as different.

### 5. Fishing boat at anchor   t = 7.0–7.5 s, hard cut
- Silhouette: broad hull low in the frame; one mast from amidships to the masthead, a furled sail hugging it; horizon behind, sky above.
- Anchor: the masthead lantern is the lamp disc.
- Inks: indigo line (hull, mast, sail), blue base, yellow accent, pink accent (fringe). Misreg indigo(+2,+1) blue(0,0) yellow(0,0) pink(+2,+1).
- Knockouts: hull from sea; sail, lamp, 16 stars from sky; waterline hatching.
- Live element: Answer 90.

### 6. Bell buoy   t = 7.5–8.0 s, hard cut
- Silhouette: a conical buoy at the waterline, a four-post cage on it holding a bell, the lamp on top; horizon, sky.
- Anchor: the cage-top lamp is the lamp disc.
- Inks: indigo line (cage, bell, sound arcs), blue base, pink overprint (body solid; shadow over blue dots → violet), yellow accent. Misreg indigo(−1,+2) blue(0,0) yellow(+1,0) pink(+3,0).
- Knockouts: body from sea and sky; lamp; bell from body; foam hatching.
- Live element: Answer 90; sound arcs static.

### 7. Breathe   B1 8.0–8.5, B2 10.0–10.5, B3 13.0–13.5 s, hard cut in; next scene irises open
- Silhouette: none; cream paper, the lamp disc lit.
- Anchor: the lamp disc itself, pink fringe right; B3 is the fringe's last showing before the machine.
- Inks: yellow accent (disc), pink accent (fringe), blue line (ripple). Misreg yellow(0,0) pink(+2,+1); blue B1(−1,+1) B2(+1,−1) B3(−2,0).
- Knockouts: none.
- Live element: one blue Ripple, 0.5 s; nothing else.

### 8. Cottage on the headland   t = 8.5–9.0 s, iris open on the anchor
- Silhouette: a headland rising from the left to a flat top and a cliff; one gabled cottage, chimney, one square window; sea right.
- Anchor: the window lamp is the lamp disc.
- Inks: indigo line (roof, chimney, cliff), blue base, pink overprint (headland → violet; wall solid; roof: blue dots over pink), yellow accent. Misreg indigo(+1,−2) blue(0,0) yellow(+1,+1) pink(+3,+1).
- Knockouts: cottage from headland; window from wall; smoke lobes, 12 stars from sky.
- Live element: Answer 90.

### 9. Whale   t = 9.0–9.5 s, hard cut
- Silhouette: a whale facing right, wholly underwater, back arching, one fin, a mouth line; wavy surface line high, sky strip above.
- Anchor: the whale's eye is the lamp disc.
- Inks: blue base (water solid, sky strip grain), indigo line (outline, mouth, surface), pink overprint (body → violet), yellow accent (band 60 %, light shafts). Misreg indigo(−2,+1) blue(0,0) yellow(0,−1) pink(+2,−1).
- Knockouts: eye; four shafts from water, blue dots inside; belly hatching.
- Live element: Answer 90.

### 10. The far lighthouse   t = 9.5–10.0 s, hard cut
- Silhouette: open sea; on the horizon a tiny tower on a low island, its lamp room the disc's size.
- Anchor: the far tower's lamp is the lamp disc.
- Inks: blue base, indigo line (tower, island, horizon), pink overprint (cloud band → violet), yellow accent (flash bar). Misreg indigo(+2,0) blue(0,0) yellow(+1,+2) pink(+3,+2).
- Knockouts: tower from sky and cloud; 30 stars; flash bar through the anchor.
- Live element: Answer 90; flash bar 0.1 s at the bloom.

### 11. Steamer   t = 10.5–11.0 s, iris open on the anchor
- Silhouette: a steamer facing left: long hull, superstructure block, wide funnel with a plume, seven portholes; horizon, sky.
- Anchor: the bridge lamp is the lamp disc.
- Inks: indigo line (hull, funnel band), blue base, pink overprint (superstructure, funnel; plume → violet), yellow accent (portholes). Misreg indigo(+1,+2) blue(0,0) yellow(−1,0) pink(+1,0).
- Knockouts: hull from sea; superstructure, funnel, plume, 10 stars from sky; portholes from hull.
- Live element: Answer 90; portholes fill, 40 ms stagger, with the bloom.

### 12. Jellyfish   t = 11.0–11.25 s, hard cut
- Silhouette: one jellyfish dome centred high, eight wavy tentacles to the bottom edge, two thicker; deep water, no surface.
- Anchor: the bell's core is the lamp disc, under the crown.
- Inks: blue base (water solid, height ramp), indigo line (dome, tentacles), pink overprint (rim band → violet), yellow accent (band 50 %, dot-ramp glow inside the dome). Misreg indigo(−1,−2) blue(0,0) yellow(+1,0) pink(+3,0).
- Knockouts: dome from water, glow printed inside; core.
- Live element: Answer 60.

### 13. Heron in the reeds, a firefly   t = 11.25–11.5 s, hard cut
- Silhouette: a heron facing right, S-neck, dagger bill; fourteen reeds with bulrush heads; marsh water low, mist band on it.
- Anchor: the firefly is the lamp disc, before the bill.
- Inks: blue base, indigo line (heron, reeds), pink overprint (mist → pale violet), yellow accent (ten small fireflies). Misreg indigo(+2,−1) blue(0,0) yellow(0,+1) pink(+2,+1).
- Knockouts: heron from sky; ten paper dots in the reeds.
- Live element: Answer 60; the firefly rises into the anchor, then blooms.

### 14. Night train head-on   t = 11.5–11.75 s, hard cut
- Silhouette: a locomotive head-on: round smokebox, cab block, chimney stub, cowcatcher; two rails converging from the bottom corners; plume up-right.
- Anchor: the headlamp is the lamp disc.
- Inks: indigo line (locomotive, rails), blue base (sky grain, ground dots), pink overprint (plume → violet; buffer beam solid), yellow accent. Misreg indigo(0,+2) blue(0,0) yellow(+1,−1) pink(+3,−1).
- Knockouts: locomotive from sky and ground; a paper ring inside the smokebox fill; rail tops; plume.
- Live element: Answer 60.

### 15. Campfire on the beach   t = 11.75–12.0 s, hard cut
- Silhouette: a beach sloping right, sea beyond; three crossed logs, a leaf-shaped flame, one side lobe, six sparks.
- Anchor: the flame's heart is the lamp disc.
- Inks: blue base, indigo line (logs, flame outline), pink overprint (flame over yellow → orange-red; tip solid), yellow accent (coarse halo). Misreg indigo(−2,−1) blue(0,0) yellow(0,0) pink(+2,0).
- Knockouts: flame and halo from sky and sea; logs from sand; six sparks.
- Live element: Answer 60; flame scales 1.0→1.12→1.0 with the bloom.

### 16. Owl on the dune post   t = 12.0–12.25 s, hard cut
- Silhouette: an owl facing left on a fence post: upright egg, flat crown, one ear tuft, hooked beak, half-ring facial disc; dune low.
- Anchor: the owl's eye is the lamp disc.
- Inks: indigo line (owl, post, dune), blue base, pink overprint (breast dots on a paper knockout; cloud → violet), yellow accent. Misreg indigo(+1,+1) blue(0,0) yellow(0,+1) pink(+2,+1).
- Knockouts: owl and post from sky; breast from owl; paper facial ring; 8 stars.
- Live element: Answer 60.

### 17. Anglerfish in the deep   t = 12.25–12.5 s, hard cut
- Silhouette: an anglerfish facing left, a fat teardrop, jaw gaping, teeth; the stalk curling up to the lure; water everywhere.
- Anchor: the lure is the lamp disc.
- Inks: blue base (water at the ceiling), indigo line (outline, stalk), pink overprint (body → dark violet; mouth solid), yellow accent (band 30 %, glow pool). Misreg indigo(−1,0) blue(0,0) yellow(+1,+1) pink(+3,+1).
- Knockouts: pool from water; mouth from body; 14 paper teeth; a paper eye.
- Live element: Answer 60.

### 18. Fireworks from the far town   t = 12.5–12.75 s, hard cut
- Silhouette: a low far skyline, two spires, sea before it; a burst of 24 dot-tipped rays, long and short alternating; 12 outer dots.
- Anchor: the burst's heart is the lamp disc.
- Inks: blue base, indigo line (skyline), pink accent (12 rays, outer dots), yellow accent (12 rays). Misreg indigo(+2,+1) blue(0,0) yellow(0,0) pink(+2,−1).
- Knockouts: skyline from sea; 20 paper windows; heart, rays, dots from sky.
- Live element: Answer burst; outer dots on a hold key.

### 19. The moon breaks cloud   t = 12.75–13.0 s, hard cut
- Silhouette: night sky over sea; two cloud bands crossing, a central gap opening; in it the moon, its 22° halo.
- Anchor: the moon is the lamp disc.
- Inks: blue base, pink overprint (clouds → violet; lit lower edges on paper), yellow accent (halo dots), indigo line (horizon). Misreg indigo(+1,+2) blue(0,0) yellow(0,−1) pink(+2,−1).
- Knockouts: halo from sky; cloud lit edges; 24 stars outside the halo.
- Live element: Answer 60; ring reaches halfway to the halo.

### 20. Dawn drains the night   t = 13.5–15.0 s, iris open on the anchor (13.5–13.9)
- Silhouette: scene 1's plates exactly (same paths, same seeds): tower on its hill, cottage dark, sea to the right, the lamp lit at the anchor with the beam turning. Added: the sun, a 90 px disc rising at (600, y) on the right horizon, clipped to above y = 560.
- Anchor: the keeper's flame — the lit lamp disc at (360, 360) with its pink fringe, turning its last sweeps; by 15.0 the yellow has starved away and only the indigo ring remains.
- Inks: indigo = line · blue = base (night sky 72 % grain at 13.5, dissolving; sea 85 % solid, holding) · pink = overprint (hill violet; tower bands; a dawn glow: pink grain touch rising from the horizon, 45 % at y = 560 → 0 at y = 200, growing over the scene; sun heart pink 60 % over yellow → orange) · yellow = accent (lamp, beam, sun). Misregistration: indigo (−1, +1) · blue (0, 0) · yellow (+1, +1) · pink (+3, +1) — the same vectors as scene 1, the sheet has come round.
- Knockouts: all of scene 1's; the sun disc from the pink glow (paper, then yellow and pink); the beam wedge from the sky while it still exists; the lamp disc.
- Tone: the sky is the live plate here — see below; sea solid; glow grain touch; sun solid; hill dots.
- Motif rhyme: the sun is the motif's shape at 2.5× and off the anchor, the one time a second disc is allowed, to say that a bigger light has come; the beam sweeps until the flame goes; the last ripple was B3's.
- Live element: in sequence — (a) 13.5–14.5 Halftone dissolve of the blue sky plate, noise-staggered by height so the horizon starves first and the top last (easeInQuad on each dot's size, 1.0 s over the whole plate; each dot's start = 0.7 s × (1 − y/560) ± 0.1 s seeded), while the pink glow's coverage ramps 0 → its full ramp over the same 1.0 s; (b) 14.0–15.5 the sun rises from y = 605 (fully below the horizon) to y = 515 (its centre 45 px above), easeOutCubic, clipped at y = 560 on both plates; (c) 14.5–15.0 Halftone dissolve of the lamp's yellow disc and its pink fringe (0.5 s, easeInQuad, noise-staggered), the indigo ring holding; the beam wedge's ramp starves with it (the wedge's yellow coverage scales with the disc's). The beam keeps turning through (a) and (b) on its period: 13.5 at 200°, 15.0 at 340°.
- Don't: no colour ramp on the sky — it is dots starving, not a fade; no birds; no sun rays; the sea does not brighten except by the sun's own yellow 30 % dots (0°) within 120 px of the sun, over blue → green shimmer, planned.

### 21. The machine takes over   t = 15.0–17.0 s, registration drift as a cut at 15.0 (all plates jump to (0, 0))
- Silhouette: scene 20's plates in their dawn state: cream sky with pink glow, sea, hill, tower, cottage, the sun at y = 515 holding from 15.5; and the keeper's silhouette on the hill path. The path: an indigo dotted line from the tower door (330, 600) down the hill's curve to (40, 700).
- Anchor: the machine's ring — a 2 px indigo circle of radius 18 px at (360, 360), paper inside, perfectly round, zero wobble, zero misregistration: the only perfect circle in the film. No yellow, no fringe.
- Inks: indigo = line (tower, ring, keeper, path, the machine beam's edges) · blue = base (sea 85 % solid; a 60 px blue 20 % dot band 15° at the top of the sky, the last of the night) · pink = overprint (hill violet at 40/40 now the night is gone; glow grain 45 % → 0; sun heart) · yellow = accent (sun; the machine beam at 30 %). Misregistration: indigo (0, 0) · blue (0, 0) · yellow (0, 0) · pink (0, 0). This is the point of the scene.
- Knockouts: all of scene 1's that survive daylight (tower from the glow, cottage from the hill, wave hatching); the ring's interior; the machine beam from the glow and the sea.
- Tone: as scene 20's end state; the machine beam = yellow 30 % dots 0° at constant density along its length (no ramp — the machine's light does not fall off), 8° wide, straight edges 0 px soft.
- Motif rhyme: the ring at the anchor, exact; the machine beam turning; the sun.
- Live element: (a) the machine beam sweeps 200°→340° in 1.5 s then off 0.5 s, twice (15.0–17.0), linear, its edges hard, its density flat; (b) the keeper walks down the path from (330, 600) at 15.0 to (40, 700) at 17.0, 8 fps, 16 poses, two leg keys alternating, height 40 px shrinking linearly to 32 px, facing left, coat and legs only, never looking back. The sun holds from 15.5.
- Don't: nothing on this sheet wobbles except the keeper's hand-drawn line; the ring and the beam edges are geometric; no pink fringe anywhere; the keeper does not pause, wave or turn; no ripple leaves the anchor (the machine does not call).

### 22. keeper   t = 17.0–20.0 s, hard cut at 17.0 (new registration)
- Silhouette: cream paper. The lamp disc lit at the anchor. Under it, the word "keeper" in lowercase single-line hand lettering: x-height 60 px, baseline at y = 500, k's ascender to y = 400, p's descender to y = 540, total width 300 px centred on x = 360 (glyph origins at x = 214, 268, 318, 370, 420, 470); stroke 6 px indigo with 1 px width wobble and tapered ends; each glyph one or two polylines: k = down, then one stroke out-and-back; e = one loop; e; p = down, then the bowl; e; r = down, then the shoulder.
- Anchor: the lamp disc at (360, 360), yellow with the pink fringe restored: the keeper's light, remembered above the keeper's name.
- Inks: indigo = line (lettering) · pink = accent (fringe; the lettering's misregistered copy at 100 %) · yellow = accent (disc) · blue = line (one ripple). Misregistration: indigo (0, 0) · pink (+2, +1) · yellow (0, 0) · blue (−1, +1). The pink copy of the lettering is the misregistration made visible: the same paths, pink, offset (+2, +1), revealed two frames behind the indigo.
- Knockouts: none; everything prints on paper.
- Tone: nothing screened until the dissolve; the dissolve renders the strokes as dots pitch 5 px 45° that shrink.
- Motif rhyme: the ripple at 17.0; the disc above the word like a lamp over a door; the e's counters are three small rings.
- Live element: in sequence — (a) 17.0–17.5 one Ripple from the anchor (blue 35 %, 0.5 s); (b) 17.5–19.0 Stroke reveal, 0.25 s per glyph in order k, e, e, p, e, r, linear along each glyph's arc length, the pink copy lagging 2 frames (at 24 fps, 83 ms); (c) 19.5–20.0 Halftone dissolve of both lettering plates (easeInQuad, noise-staggered per dot, 0.5 s). The disc never dims.
- Don't: no font; no capital; no second line; no signature mark beyond the word; the disc does not dissolve with the word.

### Surplus scenes (for the builder to swap in; each names the slot it can replace)

### 23. Lightning over a squall   alternate for 18 or 19 (0.25 s)
- Silhouette: a flat-bottomed squall cloud upper right, rain hatching under it, a five-segment bolt to the sea.
- Anchor: the lightning's source is the lamp disc.
- Inks: blue base, pink overprint (cloud → violet, over the glow), yellow accent (glow grain under cloud), indigo line (rain, horizon). Misreg indigo(+2,0) blue(0,0) yellow(0,+1) pink(+2,+1).
- Knockouts: bolt as a paper zigzag from cloud and sea, yellow inside.
- Live element: Answer 60; bolt on for 0.1 s at the bloom.

### 24. Rowboat with a raised lantern   alternate for 5 or 11 (0.5 s)
- Silhouette: a rowboat low in the frame; a standing figure, one arm straight up holding the lantern; horizon. Low-fit: a human figure, faceless, staged like the keeper.
- Anchor: the raised lantern is the lamp disc.
- Inks: indigo line (boat, figure, oars), blue base, pink overprint (low cloud → violet), yellow accent. Misreg indigo(+1,+2) blue(0,0) yellow(−1,0) pink(+1,0).
- Knockouts: boat and figure from sea and sky; 12 stars; hatching.
- Live element: Answer 90; arm already up.

### 25. Harbour with masts   alternate for 8 (0.5 s)
- Silhouette: a stone mole from the left ending in a round pier with a small light tower; six masts behind; a town far left.
- Anchor: the harbour light is the lamp disc.
- Inks: indigo line (mole, masts), blue base, pink overprint (mole → violet; tower solid), yellow accent (windows). Misreg indigo(−2,+1) blue(0,0) yellow(0,0) pink(+2,+1).
- Knockouts: tower and town from sky; ten paper windows.
- Live element: Answer 90; windows fill, 40 ms stagger, with the bloom.

## Composition rules for every scene

1. **One bold subject** readable as a silhouette in 0.25 s at 120 px: a tower, a hull, a dome, an egg on a post, a teardrop with a gaping mouth. Forms are straights and curves with 8–13 control points, no interior modelling; depth comes only from overlap (the mole in front of the masts), size (the far lighthouse at 14 px) and value (violet whale in dark water). Count the wings, not the feathers: the owl has one tuft and one eye, the whale one fin.
2. **Value first, colour second.** In every night sheet the order is fixed: blue base is the dark field, indigo is line and silhouette on paper knockouts, pink is the mid supporting shape or the violet overprint, yellow is the single bright point. Decide the plate stack before hues; the entry's ink line is that stack.
3. **The anchor lands on meaning.** (360, 360) is the lens, the hatch at the top of the stair, the flame, and then the one thing in each sheet that has a light of its own: masthead, buoy lamp, window, eye, far lamp, bridge lamp, bell core, firefly, headlamp, flame heart, eye, lure, burst heart, moon, the machine's ring, the lamp above the word. Every entry names its landing.
4. **Rhyme with the motif.** Every sheet holds a concentric or radial element besides the answer ring: lens rings, gallery rail, mullions, sound arcs, light shafts, the flash bar, the smokebox, the halo, the firework spokes, the 22° halo, the sun. The rhyme is listed per entry.
5. **3–4 inks, roles assigned**, knockouts listed, one misregistration vector per ink per sheet. Indigo fills never sit on blue or pink solids; they are knockouts with a 1 px trap. Indigo lines overprint anything. The lamp disc is always knocked out of whatever base it sits in.
6. **Strong value contrast.** The night sheets carry a light subject only as a knockout (tower, dome, sail, pink buoy) and a dark subject only on paper or on a 20–50 % tint (hull on the knocked-out sea, owl on the knocked-out sky). Nothing dark on dark; nothing light on light except the machine's ring on cream, which is the point.
7. **Texture last.** Grain, voids, speckle, misregistration and the fringe are consequences of the plates. Every sheet must read with all texture switched off (the builder's texture toggle in §Architecture is the test).

## Visual system

- **Paper:** warm cream `#F2EDE3`, one static fibre-grain layer (seeded once, seed `paper`) plus 400 speckle flecks 1–2 px at 8 % darker than the paper. It never flickers, never scrolls, is drawn once and reused as the compositor's bottom layer.
- **Inks:** indigo `#2E3192` line · blue `#0078BF` base · yellow `#FFE800` overprint/accent · fluorescent pink `#FF48B0` accent. No black, no white, no other inks. Overprints are simulated with multiply; the builder may lighten each ink 4 % and add 2 % grain to the multiply result to mimic real ink sitting lighter than the screen preview.
- **Planned overprints:** pink × blue → violet (hill, dusk glass, clouds, whale, anglerfish body, plumes); yellow × pink → orange-red (flame body, sun heart, fringe crescent where it overlaps the disc); yellow × blue → green only as the beam-edge dot fringe and the dawn sea shimmer near the sun. Any other overlap is a bug.
- **Screening:** dot pitch 5 px on a fixed grid, tone as dot size only; angles indigo 45°, blue 15°, pink 75°, yellow 0° — never two inks on one angle. Retro coarse pitch 9 px only for the campfire halo (scene 15). Grain touch (stochastic, seeded per object) replaces dots in: every night sky, the stair interior, the lamp-room dusk glass, mist, steam and smoke plumes, cloud bands, the dawn glow, the sand. Everything else that is not 100 % is a dot ramp. Ramps are driven by one of: distance from the anchor (glows, halos), the beam's length (the wedge and band), height (stair interior, deep water, dawn glow), or a light direction (tower shadow, bell shading).
- **Coverage:** large solids (sky, sea, deep water, the locomotive) print at 78–85 %, never 100 %, and carry 20–50 ink-starved voids 3–8 px, seeded per plate, plus a faint density ramp of ±4 % across the field. 100 % is for small and medium shapes only (the disc, hulls, the buoy body, the flame, rays, lettering). Tints stay inside 15–85 %. Roller band on: the last-printed ink (indigo) leaves a horizontal smear band in the top 10 % of every exterior sheet at 4 %, static.
- **Misregistration:** 1–3 px per ink, a fixed (dx, dy) per sheet as written in each entry, changed only at cuts. Blue is the registration reference at (0, 0) in every sheet. The motif's fringe: pink is always +2 px right of yellow on the lamp (and +1 or +2 on x in all sheets where both print), so a pink crescent shows on the disc's right edge. From 15.0 to 17.0 every vector is (0, 0). Objects that must align internally (the eye in the owl, the portholes in the hull, the teeth in the jaw) live on one plate or are knockouts of one plate.
- **Print texture:** speckle flecks, ink-starved voids in solids, paper-coloured hatching for highlights (wave hatching, waterline gleams, belly gleam, foam). All three are seeded and locked to the object they sit on; the wave hatching moves with its cycle, everything else is still.
- **Line quality:** every stroke carries low-frequency wobble on position (1.5 px) and width (±1 px), tapered ends over the last 8 px, 8–13 control points per silhouette. Rings are never perfect: radius modulated by three slow sine terms at 2–3 % — with one exception, the machine's ring and the machine's beam edges from 15.0 to 17.0, which have zero wobble by design.
- **The motif:** 36 px across, 5 % of frame width. Lit: yellow 100 %, pink fringe. Unlit and machine: a 2 px indigo ring of radius 18 px. Its answer ring: yellow 40 % dots (scene 4's and the breathes' ripples are blue, so the tower's calls and the world's answers read as different inks).

## Motion vocabulary

Every move used, with its print origin. No other move appears in the timeline.

| move | used at | print origin | easing | duration | parameters |
|---|---|---|---|---|---|
| Hard cut | 4.0, 5.5, 7.0, 7.5, 8.0, 9.0, 9.5, 10.0, 11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0, 17.0 | next sheet | none | 0 | on the grid; every plate takes the new sheet's misregistration vector on the same frame |
| Plate-by-plate reveal | 0.5–1.0 | printing light to dark | hold keys | 0.125 s per plate | yellow at 0.5, pink at 0.625, blue at 0.75, indigo at 0.875; each plate appears whole with its offset |
| Dive | 2.0–2.35 | the lens pushing through the hole | easeInOutCubic | 0.35 s | disc mask on the anchor from 0 to past the corners (radius 0 → 520 px) while scene 2 scales 0.55 → 1.0 about the anchor; scene 1 stays printed outside the mask; anchor fixed |
| Bloom | 4.5–5.1 (lens); every Answer | petals printed one by one | easeOutBack as two keys (1.08 then 1.0), 40 ms stagger | 0.2 s per ring at 4.5; 0.1–0.2 s per Answer | at 4.5 the disc then rings 1–5 outward; in an Answer the disc alone, or the disc plus a stagger row (portholes, windows, fireflies, rays) |
| Ripple / ring | 6.0, 6.5, B1, B2, B3, 17.0; the answer ring in every montage scene | a stencil circle growing | easeOutCubic | 0.5–0.6 s (tower calls); scene remainder (answers) | tower calls: blue 35 %, stroke 6 → 1 px, radius 0 → 520 px, 3 % wobble, 2–3 tick arcs at the rim for 0.15 s. Answers: yellow 40 % dots, stroke 4 → 1 px, radius 18 → 90 px (0.5 s sheets) or 18 → 60 px (0.25 s sheets), 3 % wobble, no ticks |
| Beam sweep | 5.0–5.5, 5.5–7.0, 13.5–15.0, 15.0–17.0 | the yellow plate pinned at the anchor and turned between passes; each frame is that plate re-printed at the next angle | linear | 1.5 s per sweep, 0.5 s dark, period 2 s | wedge 24° (keeper) or 8° (machine); from 200° to 340° clockwise, +x = 0°; knockout of every base it crosses; yellow ramp 100 % → 35 % along its length (keeper) or flat 30 % (machine); soft edges 12 px (keeper) or 0 px (machine); masked to the sky half so it never crosses the tower |
| Beam pass | first half of every montage scene (5, 6, 8–19, 23–25) | the yellow plate slid across the sheet under the lens, printed at every position: the sheet-slide move applied to one plate | linear | 0.25 s (0.5 s sheets), 0.125 s (0.25 s sheets) | a band 160 px wide, full height, soft edges 12 px, travelling from x = −160 to x = 880 left to right; knockout of every base it crosses; yellow ramp 100 % at its centre line → 35 % at its edges; capped at 60 % (scene 9), 50 % (12), 30 % (17); the Answer's bloom fires when the band's centre crosses x = 360 |
| Iris / disc reveal | 8.5, 10.5, 13.5 | a punched hole | easeOutBack as two keys (1.08 then 1.0) | 0.4 s | disc on the anchor from radius 0 to 396 px (55 % of the frame's diagonal, past the corners at 1.08); opaque paper backing inside the disc so the breathe's ripple never shows through; the new sheet's misregistration is set at the start of the iris |
| Halftone dissolve | 13.5–14.5 (sky plate), 14.5–15.0 (flame), 19.5–20.0 (lettering) | ink starving | easeInQuad per dot, noise-staggered | 1.0 s (sky, height-ordered: start = 0.7 s × (1 − y/560) ± 0.1 s seeded), 0.5 s (flame, lettering) | the plate is rendered as dots at its screen pitch and angle and every dot's radius shrinks to zero on its own clock; for grain plates each grain fleck is the dot |
| Registration drift as a cut | 15.0 | re-registering the sheet | hold | 0 | all four plate offsets jump to (0, 0) on the beat; the wobble amplitude of the ring and the beam edges jumps to 0 on the same frame |
| Stroke reveal | 17.5–19.0 | the pen writing | linear along arc length | 0.25 s per glyph, 6 glyphs | single-line glyphs; the pink copy of each stroke lags 2 frames (83 ms at 24 fps) behind the indigo |
| Limited animation (twos/threes) | 1.0–2.0, 2.35–4.0, 4.0–4.5, 15.0–17.0 | a sheet per drawing | stepped, no easing | at 8 fps (12 poses/s for the walk in scene 1: 12 fps) | the keeper: 2 leg keys alternating each pose, 2 px bob, translation along a written path, mirrored at direction changes; the arm lift in scene 3: 2 held poses |

Camera: none, except the dive, which is about the anchor. No pans. No zooms. No parallax. No motion blur. Paper grain is static for the whole film; every object's texture is seeded from the object and moves with it; misregistration vectors change only at cuts; no line boil anywhere (the keeper is stepped, not boiled).

## Architecture

- **`render(t)` is pure.** One function of time in seconds returns the composited frame. No state survives between calls except caches keyed by immutable inputs. Calling `render(9.2)` after `render(3.0)` gives the same pixels as calling it cold; the builder asserts this (see §Verification).
- **Seeded randomness only.** One `mulberry32`-class PRNG, seeded by a string hash of `sceneId + ':' + elementName` (`'paper'`, `'s5:stars'`, `'s9:voids:blue'`, `'s22:dissolve:k'`). Every wobble, void, speckle, star position, dissolve stagger and grain fleck draws from such a stream, once, at plate build time. There is no `Math.random()` anywhere in the file. Per-frame values come only from `t` and the seeded tables.
- **Timeline as data.** A `cues` array, each `{ start, duration, kind, scene, transitionIn, params }` with `kind ∈ { scene, breathe, transition }`; scene starts are exactly the table in §Timeline. `render(t)` finds the active cue(s) by binary search: a transition cue names its from-scene and to-scene. Act markers are a second array `[0, 4, 7, 13, 17, 20]`.
- **Scene registry.** `scenes[id] = { build(seedBase) → { plates: { indigo, blue, yellow, pink }, knockouts, misreg: { indigo: [dx,dy], … } }, live(t, plates) }`. `build` returns static greyscale coverage plates (offscreen canvases, 720×720, one per ink) and is called once per scene and cached. `live` draws only the dynamic layer for time `t` (the keeper, the beam, the band, the bloom, the ring, the dissolve) into a small per-frame dynamic plate set, and returns the knockout mask the beam applies to the bases this frame.
- **Plate compositor.** For each frame: paper layer → for each ink in print order (yellow, pink, blue, indigo): take the scene's static coverage plate, subtract this frame's dynamic knockouts (`destination-out`), add this frame's dynamic coverage (`lighter` on the greyscale), screen it against the precomputed threshold tile for that ink's angle and pitch (or the grain tile for grain zones — the plate carries a per-region mode mask), tint to the ink's hex, and `multiply` onto the accumulator at the plate's misregistration offset. Trapping is drawn into the static plates. Overprint is nothing more than this multiply order; nothing else blends.
- **Caching.** Static plates per scene (four canvases each, ~25 scenes → 100 canvases, ~50 MB, built during a loading bar before playback with the paper layer first). Screened static plates cached too, so a held scene costs one dynamic pass. Threshold tiles per angle built once (a 60×60 px tile for 5 px pitch, rotated per angle). A `texture` flag (`?texture=0`) bypasses screening, grain, wobble, voids and misregistration for the rule-7 read test.
- **Controls.** Space play/pause; a scrubber with the six act markers; arrow keys step 1/24 s; `?t=9.25` opens paused at that time; `R` records via `captureStream` + `MediaRecorder` at 24 fps to a WebM download; `?texture=0` for the flat read test; optional muted WebAudio click at 120 BPM for scrubbing by ear (`M` toggles). Target 60 fps on a laptop with the caches warm; frames drop before they smear (no frame interpolation).

## Process

Staged build. Each stage ends at a stop point with stills the builder inspects (via `?t=` in headless Chrome) before going on. Nothing from a later stage starts before the earlier stop passes.

1. **Engine first (no scenes).** Paper layer, one blue plate with a solid, a dot ramp and a grain zone, screened at 15°, misregistered (+2, +1), multiplied onto the paper; the lamp disc at the anchor with its pink fringe; one ripple. Stop: stills at t = 0.0 and t = 0.6 of this test sheet, plus a 4× crop of 100×100 px at the anchor. Inspect: dots on a fixed grid, size not spacing; the fringe a pink crescent on the right; the ripple's stroke thinning; the paper grain identical in both stills.
2. **Scenes 1–4 and the breathe.** Stop: stills at t = 0.25, 1.0, 1.75, 2.2, 3.0, 4.0, 4.75, 5.25, 6.0, 6.9, 8.25. Inspect: the plate-by-plate order at 0.6/0.7/0.8/0.9 (four more stills); the dive's mask at 2.2 with scene 1 still printed outside it; the keeper's pose count on the stair; the bloom's ring order at 4.6–5.0 (stills every 0.1 s); the beam knocking the sky out, never crossing the tower; the ripple at 6.3.
3. **Montage scenes 5–19 in three batches** (5–10, 11–15, 16–19), then the surplus 23–25. Stop after each batch: a contact sheet of every scene at its midpoint and its last frame, at full size and at 120 px. Inspect: silhouette read at 120 px; the disc at (360, 360) on the last frame of every scene; the band's knockout edge with its green dot fringe; no indigo fill on a blue solid; the answer ring's radius at the last frame (90 or 60 px).
4. **Dawn, machine, title (20–22).** Stop: stills at t = 13.75, 14.25, 14.75, 14.95, 15.0, 15.05, 15.5, 16.5, 17.25, 18.0, 18.6, 19.0, 19.75, 20.0. Inspect: the sky dissolving bottom-first (14.25 has dots only in the top third); the flame's dots shrinking while the ring holds; 14.95 vs 15.05 shows the registration snap and the wobble vanishing; the keeper's descent path; the glyph order and the pink lag at 18.0 (a glyph mid-stroke, pink shorter than indigo); the lettering as shrinking dots at 19.75 with the disc intact at 20.0.
5. **Boundary inspection.** Stills every 0.25 s from 0.0 to 20.0 (81 stills) laid out as a contact sheet; the automated checks of §Verification run on the same pass. Inspect: every cut lands on a grid line; misregistration never changes inside a sheet; no frame shows two scenes at once except during the dive and the three irises.

## Verification checklist

Each check is answered by a measurement in code or by a named still. The builder runs all of them and records the result; a FAIL blocks delivery.

1. **Anchor at every act boundary (measured).** At t = 0.0, 4.0, 7.0, 13.0, 17.0 and 20.0 (and additionally at 15.0), compute the centroid of the motif's mask on its own plate before misregistration (the yellow disc when lit; the indigo ring's centre when unlit or machine). Pass: centroid within 1.0 px of (360, 360) at every one of the seven times. Also assert that after misregistration the disc's on-screen centre differs from (360, 360) by no more than that scene's written vector for that plate (≤ 3 px).
2. **Every montage sheet lands the answer (measured).** For scenes 5, 6, 8–19 (and any surplus used), sample the yellow coverage plate at (360, 360) on the scene's last frame. Pass: ≥ 95 % in every scene. Also assert the answer ring's radius at that frame = 90 ± 3 px (0.5 s sheets) or 60 ± 3 px (0.25 s sheets).
3. **No dark-on-dark (measured).** For every scene at its midpoint, count pixels where blue coverage ≥ 85 % and pink coverage ≥ 85 % (must be 0), and pixels where indigo ≥ 85 % and blue ≥ 85 % outside a 3 px-dilated mask of the scene's stroke paths (must be 0; lines may overprint, fills may not). Report both counts per scene.
4. **Grid and vectors (measured).** For every cue: `start mod 0.25 === 0` and `(start + duration) mod 0.25 === 0`. For every scene, hash the misregistration vectors at every frame of the scene at 24 fps: exactly one distinct hash per scene. For 15.0 ≤ t < 17.0: all vectors are (0, 0). For every sheet where the lamp is lit: pink.dx − yellow.dx ≥ 1.
5. **Screening (still + measured).** 4× crops of 100×100 px at (360, 360) and at (200, 200) at t = 6.0 and t = 9.25. Pass: dots lie on a 5 px grid, the yellow at 0°, blue at 15°, indigo at 45°, pink at 75° (measure the angle from the dot rows in the crop); no two inks share an angle; no dots inside a 100 % solid; no pixel of a gradient without dots or grain (scan for runs of ≥ 8 px with monotonic luminance change and no dot/grain structure: must be 0).
6. **Coverage caps (measured).** For every base plate (sky, sea, deep water, interior) at the scene's midpoint: mean coverage between 70 % and 86 %; void count 20–50; no tint between 1 % and 14 % or between 86 % and 99 % over an area larger than 64 px² except inside a ramp's transition band.
7. **Determinism (measured).** Hash the frame at t = 9.2 rendered cold, rendered after t = 3.0, and rendered after a full play-through: three identical hashes. Grep the source: zero occurrences of `Math.random`.
8. **Silhouette read (still).** The stage-3 contact sheet at 120 px: every montage scene identifiable by name by someone who has not read the spec, with `?texture=0` and with texture on. Record which scenes fail; fix the silhouette, never the texture.
9. **Frame rate (measured).** Over 7.0–13.0 with caches warm, the mean `requestAnimationFrame` interval ≤ 18 ms (≥ 55 fps) and no interval > 50 ms.
10. **Text (measured + still).** Exactly six glyph paths, all in indigo with one pink copy; still at 19.0 shows "keeper" in lowercase, nothing else lettered anywhere in the film (grep the source for any other text drawing call: 0).
11. **The machine (measured).** For 15.0 ≤ t < 17.0: the ring's radius sampled at 36 angles has variance 0; the beam wedge's edges are straight (max deviation from the fitted line 0 px); no yellow coverage inside the ring. For t < 15.0 and t ≥ 17.0: the ring's radius variance > 0 wherever the ring is drawn.
12. **The beam never crosses the tower (measured).** For every frame of scenes 4, 20, 21 at 24 fps: yellow coverage inside the tower's mask below the gallery (y > 392) is 0.

## Don'ts

- No gradients without a screen: every ramp is a dot-size ramp or grain touch.
- No black ink; the darkest dark is blue at 90 % under a violet overprint. No white ink: highlights are paper.
- No crossfades. The only plate fades are the three halftone dissolves (dots starving); the ink-drain crossfade is not used in this piece.
- No text beyond "keeper". No captions, no labels, no numbers, no signature mark.
- No facial acting: the keeper is a coat, a cap brim, a chin line and legs, from every angle, in every scene; the rowboat figure likewise.
- No per-frame random values; no line boil.
- No reflections on the sea, ever: not the lamp, not the moon, not the fire. A wet gleam is paper hatching.
- No beam over blue without a knockout; the green dot fringe at the beam's edges is the only place yellow meets blue at night.
- No camera moves except the dive; the anchor never drifts; no parallax, no 3D, no motion blur.
- No second disc at the motif's size anywhere but the anchor; the sun is 2.5× and off-anchor by design.
- No outline in an ink different from its fill; no gap between a fill and its outline.
- No perfect circles before 15.0 or after 17.0; no wobble on the machine's ring or beam between them.
- No moon before scene 19; no clouds in Act I; no birds anywhere.
- No motion on subjects in the montage other than the Answer: boats do not rock, whales do not swim, trains do not advance, flames do not flicker.
- Do not shorten Acts IV–V to make room for montage scenes; if the budget runs short, cut montage scenes (surplus first, then 13, then 16), never the dawn, the machine, or the word.

## Renderer appendix: Canvas 2D

- **Plates are offscreen canvases.** Four `OffscreenCanvas` (or hidden `<canvas>`) per scene, 720×720, drawn in greyscale where luminance = ink coverage. Threshold each against a precomputed screen tile for the ink's angle and pitch (5 px; 9 px for the campfire halo): for every pixel, `covered = coverage ≥ tileThreshold(x, y)`, giving dots whose size tracks coverage on a fixed grid — a true print simulation, rosettes and dot gain included. Grain zones use a second, stochastic tile (seeded blue-noise-like table) selected by a per-region mode mask drawn into the plate's alpha or a parallel mask canvas. Tint the thresholded plate to the ink hex with `source-in`, then `globalCompositeOperation = 'multiply'` onto the paper accumulator via `drawImage(plate, dx, dy)` with the plate's misregistration offset. Print order yellow, pink, blue, indigo.
- **Knockouts** are `destination-out` draws on the darker plate's greyscale before thresholding; the 1 px trap is the lighter plate's fill drawn 1 px larger. The beam and band are dynamic knockouts: each frame, copy the cached static base plate, `destination-out` the wedge/band mask, then draw the yellow ramp into the yellow dynamic plate; only the union of the two regions needs re-screening (track a dirty rectangle).
- **Pre-render static plates** once per scene during a loading bar (build order: paper, then scenes in timeline order). Screened static plates are cached; a held scene with no live element costs four `drawImage` calls. Animate only transforms (the keeper's stepped translation, the wedge's rotation, the band's x) and the one live element per montage sheet.
- **Time** is `render(t)`, a pure function. Easings are inline functions of normalised progress (`easeOutCubic`, `easeInOutCubic`, `easeInQuad`, and the two-key `easeOutBack` as a piecewise lerp 0→1.08→1.0). The cue array picks active scenes and transitions; a transition renders both scenes and composites through its mask (dive, iris) or draws only the new one (hard cut, registration drift).
- **Stroke reveal** samples each glyph path by arc length once at build (a table of 200 points per glyph) and draws the prefix for progress `p`; the pink copy draws the prefix for `p` delayed by 2 frames. Budget: six glyphs, twelve tables.
- **Halftone dissolve** is rendered by drawing the plate's dots individually from a per-plate dot list (built once from the thresholded plate: centre, radius, seeded start time), each with `radius × (1 − easeInQuad(local progress))`; for grain plates, the fleck list serves as the dot list.
- **Verify** with `?t=` stills in headless Chrome (`--screenshot` at 720×720, one command per still, driven by a list of times), and by the in-page assertions of §Verification, which run when `?verify=1` is set and print a PASS/FAIL table to the console and to a `<pre>` under the canvas.
- **Controls:** space play/pause; scrubber with act markers at 0, 4, 7, 13, 17, 20; arrow keys step 1/24 s; `R` records via `captureStream(24)` + `MediaRecorder` to WebM; `?texture=0` flat-read mode; `M` toggles the muted-by-default WebAudio click at 120 BPM.

## Self-check

Audited against every Required line of the skill's bar after the spec was complete.

| bar item | PASS/FAIL | evidence |
|---|---|---|
| Motif and anchor defined before the first scene and named in every scene entry | PASS | §The spine defines both; all 25 entries carry an "Anchor:" line naming the lamp disc (or the unlit ring, flame, machine ring) as the thing at the anchor; full entries give (360, 360), compact entries name the landing without coordinates as the skill directs |
| Every scene entry has ≤ 4 inks, each with a role | PASS | 25 "Inks:" lines; roles counted per line: 4 in entries 1–6 and 8–25, 3 in entry 7 (the breathe) |
| Every scene entry has a knockout list | PASS | 25 "Knockouts:" lines; entries 7 and 22 state "none" because everything prints on paper; compact entries list the scene-specific knockouts and the conventions paragraph carries the three always-present ones |
| Every scene entry has a misregistration direction | PASS | 25 "Inks:" lines each end in a per-ink vector; entry 21 is (0,0) on all four by design; the breathe entry gives one blue vector per occurrence |
| Every scene entry has one live element | PASS (interpreted) | 25 "Live element:" lines. Montage entries 5–19, 23–25 have exactly one (the Answer; anything after it is part of the same bloom key). Held entries 1, 3, 20, 21, 22 list two or three sequenced elements, as motion-vocabulary §5 allows for held scenes, never more than two concurrent |
| No overlap of two dark inks at full coverage; every light-on-dark shape is a knockout | PASS | Rule stated in the conventions paragraph and §Composition rule 5; every indigo fill on a base is a knockout with a 1 px trap (entries 5, 9, 11, 13, 14, 16, 18, 24, 25); every pink × blue overprint keeps one ink ≤ 60 %; verification check 3 measures it |
| Every timeline transition is a move in §Motion vocabulary, and every move carries easing and duration | PASS | Timeline uses hard cut, plate-by-plate reveal, dive, bloom, ripple, beam sweep, beam pass, iris, halftone dissolve, registration drift, stroke reveal, limited animation: 12 rows in the §Motion vocabulary table, each with easing and duration filled |
| Every cut on the beat grid; act boundaries listed with exact times | PASS | §Timeline: every start and end a multiple of 0.25 s; act boundaries 0.0 / 4.0 / 7.0 / 13.0 / 17.0 / 20.0 printed above the table; verification check 4 asserts it |
| §Visual system lists a distinct screen angle per ink, a dot pitch, where grain replaces dots, and the coverage cap | PASS | Screening bullet: pitch 5 px (9 px campfire halo), indigo 45° / blue 15° / pink 75° / yellow 0°, grain zones enumerated; Coverage bullet: large solids 78–85 %, voids 20–50, tints 15–85 % |
| §Verification has ≥ 6 checks, each a measurement or a still, one measuring the anchor at every act boundary | PASS | 12 checks; check 1 computes the motif centroid at 0.0, 4.0, 7.0, 13.0, 17.0, 20.0 (and 15.0) with a 1.0 px tolerance |
| Scene count meets the Step 2 enumeration plus surplus; no scene is a name only; every scene uses the entry size its hold time calls for | PASS (interpreted) | Enumeration: 14 montage slots × 1.2 = 16.8 → 17 montage entries written (14 in timeline + 3 surplus); 25 entries total. Entry sizes: full for 1–4 and 20–22 (held ≥ 0.5 s, dived through, first and last); compact for 5–19 and 23–25, each five lines and ≤ 80 words by count. Per team-lead's direction the 0.5 s montage sheets (5, 6, 8–11, 24, 25) are compact; the skill's "≥ 0.5 s → full" line read literally would make them full |
| Must not: gradients without a screen | PASS | §Don'ts line 1; every ramp is a dot ramp or grain touch; check 5 scans for unscreened gradients |
| Must not: black ink | PASS | four inks only (§Visual system); darkest dark is blue 90 % under violet (§Don'ts) |
| Must not: crossfades other than a single-ink drain | PASS | no crossfade in the timeline; the three halftone dissolves are per-plate dot starving; ink drain not used (§Don'ts) |
| Must not: text beyond a title or signature | PASS | one word, "keeper", entry 22; check 10 counts six glyph paths and greps for other text calls |
| Must not: facial acting | PASS | the keeper is a coat, cap brim, chin line and legs in entries 1, 2, 3, 21; the owl and whale have one eye each, which is the motif disc; §Don'ts line 5 |
| Must not: per-frame random values | PASS | §Architecture: seeded PRNG per scene and element, no `Math.random`; check 7 greps for it and hashes three renders of t = 9.2 |
| Must not: low-fit subjects without justification | PASS | the only low-fit subjects are human figures: the keeper (fit table, silhouette only) and the rowboat figure (entry 24 carries a written justification); no faces, crowds, glass, reflections or fine text |

Good-vs-minimal contrast on three entries chosen by a die (6, 13, 17), all compact: each gives the silhouette as a described outline, the anchor landing, the ink stack with roles and the overprint result, a scene-specific knockout list, the live element on the grid, and the vectors. None reads as a name plus adjectives. No FAIL rows. Edits made during the audit: entry 3's anchor coordinates added; entry 19's knockout wording cleaned; two 60/60 overprints lowered to 55/60 and the cottage roof to blue dots over pink; entries 5–19 and 23–25 rewritten from full to compact on team-lead's instruction, with the shared defaults moved into the conventions paragraph.

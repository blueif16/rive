# Medium rules — the physics of risograph, written as decisions

Risograph is a stencil duplicator: one translucent soy ink per drum, one greyscale
plate per ink, one pass per colour, hand-registered. Everything below follows from that.
Sources: print-shop file guides (Reprographix, Out of the Blueprint, Bang Bang Zine,
Kaki Press, Oxford GreenPrint, Possible Worlds, ECUAD COMD), Fontstand's riso primer,
halftone standards (ISO 12647-2 as summarised by PrinterArchive), and the lessons from
the `riso-call` build in this repo.

## 1. Everything is a plate

- Each ink is a greyscale layer. 100 % prints solid, 0 % is paper, anything between is a
  dot screen or grain. There is no "colour picture" until the plates overprint.
- Design each scene plate by plate: for every shape decide which plate it lives on and at
  what density. A scene entry that cannot be read as 3–4 greyscale plates is not finished.
- Shops cap 2–4 inks per print because registration gets worse with every pass. Hold the
  same cap per scene: **3–4 inks maximum**, 2 is often stronger.

## 2. Overprint is a designed third colour

Inks are translucent, so overlaps mix subtractively. Preview with multiply; real ink is
slightly lighter and grainier than the screen preview.

| overprint | result on cream paper | use |
|---|---|---|
| yellow × blue | green | foliage, water shade |
| yellow × pink | orange-red | warmth, fire, fruit |
| pink × blue | violet / deep purple | dusk, shadow on pink |
| blue × green | deep teal | sea depth |
| violet × blue | near-black indigo | the darkest dark in the palette |
| orange × blue | brown | wood, earth |
| pink × green | muddy olive | avoid |
| any dark × any dark at 100 % | mud | never |

Rules:
- Plan the overprint colour on purpose and name it in the scene entry ("sea = blue base
  × green ramp → teal"). Unplanned overlaps are the main source of mud.
- One of the two inks in any overlap should be light or below 60 % coverage.
- Fluorescent pink and orange are highly transparent: they work as a base that brightens
  what prints over them, or as the accent on top. They are too light to carry line or type.

## 3. Knockout or overprint — decide for every overlap

| situation | decision | why |
|---|---|---|
| light ink shape on a dark plate (yellow moon on violet night, pink bell on blue sea) | **knockout** the shape from the dark plate | multiply would print it black; a real print leaves paper under it |
| line work in the darkest ink over any solid | overprint | lines survive misregistration on top of blocks |
| two mid inks whose mix is the wanted colour | overprint at the planned densities | that is the third colour |
| fine detail split across two plates | avoid; put it on one plate | 1–3 px drift shreds it |
| text or signature | one ink, the darkest, never overprinted, never white-out | misregistration halves legibility |
| an outline in a different ink from its fill | avoid; same-ink outline or no outline | drift shows a gap on one side |

Trapping: where two plates must meet edge to edge, let the lighter one run 1–2 px under
the darker one. Every knockout must be listed in the scene entry.

## 4. Misregistration is a constraint you design with

- Real drift is 1–3 mm on A3, about 1–3 px at 720 px. Treat it as a fixed vector per
  plate per scene, not as noise. Write it as "(dx, dy) per ink" in the entry.
- The vector changes only at a cut (a new sheet). It never changes per frame.
- The motif carries a deliberate fringe: one plate offset so a thin colour edge shows on
  one side. That fringe is the style's signature at small scale.
- Keep anything that must align (an eye in a head, a dial on a phone) on one plate.

## 5. Coverage limits make the texture

- Large solids print unevenly and jam the drum, so shops ask for 75–85 % on big areas.
  Translate: large fills carry small ink-starved voids and a faint density ramp; 100 %
  is for small and medium shapes only.
- Heavy ink near the top edge leaves roller marks on the next pass. Optional texture: a
  faint horizontal smear band in the top 10 % on the last-printed ink.
- Tints below 15–20 % vanish; tints above 85 % read as solid. Keep ramps inside that band.

## 6. Screening: dots or grain, one angle per ink

- Two screening modes exist on the machine. **Screen covered** is a dot screen: use it
  for graphic tone, shading ramps, glows. **Grain touch** is stochastic: use it for skies,
  fog, soft gradients, anything a visible dot grid would fight.
- Dot pitch at 720 px: 4–6 px (a 71 lpi default on A4 lands in that range; go coarser,
  7–9 px, for a deliberately retro glow).
- Each ink gets its own angle or the overlaps moiré. Convention: darkest or dominant ink
  at 45°, the other strong inks at 15° and 75°, yellow at 0°. Never two inks on one angle.
- Tone is dot **size** on a fixed grid, never dot spacing. Gradients are dot-size ramps
  driven by a light direction, a distance from a source, or a height.
- Solids at 100 % have no dots. A scene that is dots everywhere reads as a photo filter,
  not a print.

## 7. Paper is a colour; there is no white

- Default paper: warm cream `#F2EDE3`, static fibre grain and speckle. It never flickers.
- Highlights are unprinted paper: gleams on a bell, water rings, an eye. Draw them as
  knockouts or as paper-coloured marks, never as a white ink.
- Coloured stock shifts every ink (pink on yellow stock reads orange). If the story wants
  a night piece, keep the paper cream and print a dark plate with knockouts; do not
  switch to black paper.

## 8. Ink roles (three-ink logic)

| role | typical inks | carries |
|---|---|---|
| line | indigo `#2E3192`, blue `#0078BF`, violet `#765BA7` | outlines, type, the motif, shadows |
| base | blue, green `#00A95C`, violet | big fields: sea, night, ridge |
| overprint | yellow `#FFE800`, green, orange `#FF6C2F` | ramps and mixes over the base |
| accent | fluorescent pink `#FF48B0`, orange, yellow | the focal point, glows, the answer |

The seven house inks above are riso standards with common screen hex values. Extended
inks exist (bright red, teal, aqua, sunflower, federal blue, fluorescent orange, mint,
metallic gold) and a shop's list at stencil.wiki is the reference; hex values are always
approximations. Black exists but this style forbids it: darks come from overprint.

## 9. Line quality and texture

- Lines wobble: low-frequency noise on position and width, tapered ends, 8–13 control
  points per silhouette, never more.
- Rings are never perfect circles: radius modulated by two or three slow sine terms.
- Speckle flecks, small voids in solids, and paper-coloured hatching for highlights are the
  three allowed textures. All are seeded and locked to the object they sit on.

## 10. Type

- Only a title or signature, hand-lettered as single-line stroke paths, in the line ink,
  with the pink plate offset 2 px as misregistration. No fonts, no body text.

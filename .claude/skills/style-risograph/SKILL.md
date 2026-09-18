---
name: style-risograph
description: >-
  Turn a story, theme or brief into a complete PRODUCTION SPEC for a short animation
  in the RISOGRAPH print style (limited spot inks, halftone dot screens, overprint,
  misregistration, cream paper, hard cuts, motif-anchored composition). The output is
  the detailed prompt a build agent (Canvas 2D, Rive, After Effects...) executes; this
  skill never builds. It is the first of a family of art-style skills that a router
  picks by topic. ROUTE HERE when the story is about: call and response, resonance,
  echoes, signals and answers; memory, nostalgia, things fading and returning; small
  wonders and quiet loneliness resolved by connection; nature's rhythms (tides, moons,
  seasons, migrations); sound, music, radio, bells, voices; folk tales, fables,
  bedtime stories, children's-book warmth; zine, indie-music, poster and civic-campaign
  energy; one-bold-concept science or public-service explainers; seasonal, festival and
  greeting pieces. Formats that fit: 10-60 s poetic shorts, title sequences, loops,
  music visualisers, animated posters. ROUTE ELSEWHERE when the story needs facial
  acting or dialogue-driven character drama, photoreal light and materials, gritty or
  horror realism, dense text or UI precision, fast 3D camera action, or true black.
  Triggers: "riso", "risograph", "print style", "zine style", "screen-print look",
  "halftone animation", "spot-colour animation", or any request to design an animation
  in a handmade print aesthetic.
---

# Risograph animation — story to production spec

You produce the **production spec**, not the animation. A build agent reads your spec and
makes every pixel from it, so the spec is a contract: every scene fully planned as ink
plates, every transition drawn from the print process, every check measurable.

Read `references/medium-rules.md` before writing anything. The look is not a filter on top
of a picture; it is what happens when a picture is forced through the physics of the
medium. Get the plates, the anchor and the cuts right and the grain is optional.

## Inputs

- **story**: a theme, logline, poem, lyric, or beat list. Required.
- **duration** in seconds, **frame** (default 720×720), **beat grid** (default 120 BPM, so
  0.25 s and 0.5 s are the units), **renderer** (Canvas 2D | Rive | AE | unspecified).
- Optional: a signature or title to letter at the end; a palette preference; a hard
  scene-count budget.

If duration or frame is missing, state the default you chose in the spec header. If the
story is missing, HALT and ask. Never invent a story.

## Step 0 — fit check (also used by the router)

Score the story 0–2 on each line, sum it, and print the table at the top of the spec.

| question | 2 | 0 |
|---|---|---|
| Can each beat be told with ONE bold subject readable as a silhouette? | yes | needs crowds, faces, clutter |
| Does the story contain natural radial or concentric motifs (rings, waves, arcs, suns, dials)? | several | none |
| Is the register warm, handmade, playful, tender or wistful? | yes | gritty, clinical, corporate |
| Can emotion be carried by staging and rhythm rather than facial acting? | yes | needs close-up acting |
| Can light and material be flat shapes and dot ramps? | yes | needs reflections, glass, realistic light |
| Is on-screen text limited to a title or signature? | yes | needs captions, labels, UI |

Sum ≥ 8: proceed. 5–7: proceed and list the adjustments you made to the story in a
"Fit adjustments" paragraph. ≤ 4: stop and emit `STYLE_MISMATCH` with the failing rows
and the traits a better-suited style would need. Do not force it.

## Step 1 — motif and anchor before scenes

Extract, in this order, and write them at the top of the spec:

1. **Motif**: one geometric figure that recurs in every scene and carries the theme
   (a dot and its ripples; a bell and its arcs; a moon and its phases).
2. **Anchor**: one fixed frame position the motif occupies. Every scene must land
   something meaningful on it. Cuts feel continuous only because the anchor never moves.
3. **Plate logic**: the 3–4 house inks and the role of each (see medium-rules
   §ink-roles), the paper colour, the misregistration budget.
4. **Rhythm**: the act structure on the beat grid, where the montage accelerates, where it
   breathes back to blank paper.

## Step 2 — enumerate, then write everything in full

First list every scene, every transition and every act boundary the duration needs
(montage at one scene per beat; plus a 20 % surplus of scenes so the builder can cut).
Then write each item in full using the section shapes in `references/spec-template.md`.

A **minimal** spec names scenes ("wolf on a ridge, kettle, Ferris wheel") and stops.
That FAILS. A **good** spec gives every scene its silhouette, its anchor landing, its ink
plan with knockouts, its tone plan, its motif rhyme and its one live element. Pick
subjects with `references/subjects-and-composition.md`; pick moves with
`references/motion-vocabulary.md`.

## Output shape

One Markdown document with exactly these sections, in this order. Use the templates in
`references/spec-template.md`; that file also holds a canonical exemplar.

1. Header: title, fit table, duration, frame, beat grid, renderer, defaults assumed
2. The idea (one paragraph) and the spine: motif + anchor + never-drifts rule
3. Timeline table: time range · act · what happens, every cut on the grid
4. Scene library: one entry per scene in the fixed entry shape (silhouette, anchor,
   inks with roles, knockouts, tone, motif rhyme, live element, don't)
5. Composition rules for every scene
6. Visual system: paper, palette with hex, screening (pitch, angle per ink, grain
   zones), coverage rule, misregistration rule, texture rules, line quality, the motif's size
7. Motion vocabulary: each move with its print origin, easing, duration, parameters
8. Architecture: determinism, seeded randomness, plate compositor, caching, timeline data
9. Process: staged build with stop points and what to inspect at each
10. Verification checklist: measurable checks the builder must run
11. Don'ts
12. Renderer appendix (only for the named renderer; see `references/renderer-notes.md`)

## The bar

Required. If any Required item fails, revise before returning.

- Motif and anchor are defined before the first scene and named in every scene entry.
- Every scene entry has ≤ 4 inks, each with a role (line | base | overprint | accent), a
  knockout list, a misregistration direction, and one live element.
- No overlap of two dark inks at full coverage anywhere; every light-on-dark shape is
  listed as a knockout.
- Every transition in the timeline is one of the moves in section 7, and every move in
  section 7 carries an easing and a duration.
- Every cut sits on the beat grid; act boundaries are listed with exact times.
- Section 6 lists a distinct screen angle per ink, a dot pitch, where grain replaces dots,
  and the coverage cap for large solids.
- Section 10 has at least six checks, each answerable by a measurement or a still, and
  one of them measures the anchor position at every act boundary.
- Scene count meets the enumeration from Step 2 plus surplus; no scene is a name only.

Must not: gradients without a screen; black ink; crossfades other than a single-ink
drain; text beyond a title or signature; facial acting; per-frame random values; subjects
from the low-fit list without a written justification in the entry.

## Self-check (mandatory, printed at the end of the spec)

Audit against every Required line above. Print a table: item · PASS/FAIL · one line of
evidence (a section name, a count, a scene id). Revise every FAIL and re-audit. Then run
the good-vs-minimal contrast on three random scene entries: if any reads as a name plus
adjectives, rewrite it.

## Scope fence

Do NOT write code, RML, shader, or After Effects setups. Do NOT render. Do NOT choose a
renderer the inputs did not name; if unspecified, write the appendix for Canvas 2D and say
so. If the story cannot pass the fit check, emit `STYLE_MISMATCH` rather than a weak spec.

# Figure — A taxonomy of world models

Read `HOUSE-STYLE.md` first; it carries the palette, motion grammar, embed
contract, and quality bar.

## Knowledge point

A world model can serve three different functions. Each takes the same underlying
world and emits a different *kind* of output:

| Function | Emits | The nature of that output |
|---|---|---|
| **Renderer** | observations | a stream of **pictures** — what the world looks like |
| **Simulator** | state | a **continuous signal** — how a quantity evolves over time |
| **Planner** | actions | a sequence of **discrete choices** from a finite set |

After watching once, a reader should be able to name the three functions and say
what each produces. **The design must make the three output types feel different
in kind** — pictorial vs continuous vs discrete. That contrast is the whole
lesson; it has to live in the motion, not just in the labels.

## Structure

Three horizontal lanes stacked vertically, one per function. Each lane: a pinned
label card on the left naming the function (`renders → OBSERVATIONS`,
`simulates → STATE`, `plans → ACTIONS`), with that function's output streaming
continuously behind it.

Four beats, looping: **all three lanes together**, then each lane alone in turn
with a title card naming it (`Renderer` / `OUTPUTS OBSERVATIONS`, and so on).
Roughly 3s per beat. The other lanes fade out in place — see the motion grammar.

## Design direction

The reference implementation in `reference/` solved it this way:

- **Renderer** — a film strip of frames scrolling past, each frame a small
  landscape whose sun has advanced slightly, so the strip reads as one continuous
  shot sampled into pictures
- **Simulator** — a pendulum labelled `SYSTEM` beside a live `x(t)` plot, its
  trace scrolling left with a dot riding the curve at the plot's right edge
- **Planner** — a row of action chips (`scan`, `grasp`, `lift`, `rotate`, `move`,
  `place`) scrolling past with one highlighted at a time

`reference/teaching.mov` is the full original; the PNGs are the four beats plus
detail crops. ffmpeg is available if you want more frames.

**You are not required to reproduce it.** Reproducing it faithfully is a valid
choice. So is a different visual answer to the same knowledge point, if it teaches
the contrast at least as clearly. Either way the result must meet the house
quality bar. What is not optional is the knowledge point, the three-lane
structure, the four-beat loop, and the embed contract.

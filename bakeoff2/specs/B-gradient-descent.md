# Figure B — Gradient descent finds a minimum

Read `HOUSE-STYLE.md` first.

## Knowledge point

Optimisation follows the **local slope downhill**. It has no view of the whole
landscape — only the ground under its feet. So where you start decides where you
land, and a landscape with more than one valley can strand you in the wrong one.

After watching once, a reader should understand: the descent is purely local,
and the same procedure on the same landscape gives different answers from
different starting points.

## Structure

A **loss curve** drawn across the figure — a smooth one-dimensional landscape
with two valleys, one clearly deeper than the other, separated by a ridge.

A **marble** is released onto the curve and rolls downhill, staying exactly on
the surface, moving fast on steep sections and slowing as the ground flattens,
then settling into whichever valley it reached. It leaves a **trace** showing the
path it took, and a marker rests where it stopped.

Four beats, looping:

1. **The landscape** — the curve alone, slowly breathing between two slightly
   different shapes, so it reads as a surface rather than a drawing
2. **Stuck** — a marble released on the right descends into the *shallow* valley
   and settles there, well above the true minimum
3. **Found** — a marble released on the left descends past the ridge into the
   *deep* valley and settles at the global minimum, with the first run's marker
   still faintly visible for comparison
4. **The landscape changes** — the curve morphs into a different shape, and a
   marble from the same starting point as beat 2 now ends somewhere else entirely

Roughly 3s per beat.

## Design direction

Everything hinges on the marble looking like it is **obeying the curve** rather
than being placed along it. Its vertical position must come from the curve's
shape, and its speed must come from the local slope — fast where steep, slow
where flat, with a settle at the bottom rather than a stop.

The morph in beats 1 and 4 should deform the curve continuously, not cut between
two drawings.

Label the axis or the minima only as much as the point needs. This figure should
carry its meaning through motion, with very little text.

# Figure A — What a context window holds

Read `HOUSE-STYLE.md` first.

## Knowledge point

A context window is a **fixed budget**, not a memory. New turns push in from one
end; when the budget is full, the oldest content has to leave — either dropped
or compacted into a much smaller summary. What the model knows at any moment is
only what currently fits inside the budget.

After watching once, a reader should understand: the capacity never grows, the
history does, and something has to give.

## Structure

A single horizontal **budget bar** spanning the figure — the window — with its
capacity labelled. Conversation turns enter as **blocks** that occupy space
proportional to their size, each labelled with its kind (`system`, `user`,
`tool result`, `assistant`) and a token count. A running **used / total** counter
sits alongside.

Four beats, looping:

1. **Empty** — the bar mostly free, a few blocks in it, counter low
2. **Filling** — blocks continue entering, the bar approaches capacity, counter climbing toward the limit
3. **Pressure** — the bar is full; the oldest blocks at the far end dim and collapse into one narrow `summary` block, and the reclaimed space is immediately taken by new arrivals
4. **Steady state** — the same bar, the same capacity, but now with a long compacted history behind it and only recent turns held in full

Roughly 3s per beat.

## Design direction

The tension to dramatise is that the bar's **width never changes** while the
history behind it keeps growing. Whatever you do, do not let the bar itself grow
— the whole point is that it can't.

The counter is worth animating honestly: it should visibly approach the limit and
then drop when compaction happens. That number doing the right thing is much of
the teaching.

Block labels are real words of differing lengths; the figure should handle that
gracefully.

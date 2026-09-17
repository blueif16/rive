# cnn-convolution

A 52-second Rive lesson that builds the convolution operation from zero — no
prior knowledge assumed, every multiplication shown.

```
INPUT 5x5   x   FILTER 3x3   =   PRODUCTS 3x3   ->   FEATURE MAP 3x3
```

## The arc

| | Beat | The idea |
|---|---|---|
| S1 | numbers fade into the image | an image *is* a grid of numbers |
| S2 | the filter appears | a filter is a grid of numbers too — only nine |
| S3 | one position, worked in full | nine products appear one at a time, then sum |
| S4 | the sweep | the same nine weights at every position; the map is smaller |
| S5 | back and forth | output -> its patch, and one pixel -> every output it fed |
| S6 | swap the filter | change the nine numbers, it detects something else |

Design notes, including the research the structure is based on (Mayer's
coherence / spatial-contiguity / segmenting principles, and CNN Explainer's
finding that the hard part is linking the low-level math to the structure), are
in the conversation that produced this. Two rules drive the visual design:

- **Numbers only where attention is.** The image and feature map carry colour;
  exact values appear under the kernel and in the products column.
- **Nothing on screen is ever wrong.** The products column always shows the
  arithmetic for the currently highlighted position, or is hidden.

## Build

```bash
python3 generate.py          # writes scene.rml (layout + content + keyframes)
rive . --verify              # compile check
rive .                       # live preview window
```

`generate.py` holds layout, colour and content; `timeline.py` holds the
keyframes. The scene is ~720 objects with computed convolution values, so it is
emitted rather than typed by hand.

Change `IMG` or `FILTERS` at the top of `generate.py` and everything — cell
colours, products, feature maps, the travelling values — recomputes.

## Export

```bash
../.claude/skills/rive-animation/scripts/rive-export . --format=mp4,html,png --fps=30
```

Outputs land in `build/` (gitignored, regenerate any time):

| File | Notes |
|---|---|
| `cnn-convolution.mp4` | 1200x675, 52.5s — the one to share |
| `cnn-convolution.html` | self-contained, double-click to open; keeps it live |
| `cnn-convolution.png` | opening still |
| `cnn-one-step.gif` | the S3 worked example only, cut from the mp4 |

## Fonts

`Inter.ttf` and `JetBrainsMono-Regular.ttf` are both SIL Open Font License 1.1,
so they are safe to embed and redistribute in the built `.riv`. Prose is Inter,
every number is JetBrains Mono. They account for ~1.1 MB of the `.riv`.
